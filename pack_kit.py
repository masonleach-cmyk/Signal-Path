#!/usr/bin/env python3
"""Pack drum samples into one Signal Path factory kit.

    python3 pack_kit.py --id acoustic --name "acoustic kit" --by "Freesound: user1, user2" kick.wav snare.wav hat-closed.wav ...

Writes, in the current folder:
    kit-<id>.wav   every sound end to end: mono, 16-bit, 44.1 kHz
    kit-<id>.json  where each sound starts and ends, its name, the licence and credits
    kits.json      the list of kits the app offers (this kit is added or updated)

Upload all three to the top level of the GitHub repo, next to index.html. Only use sounds marked CC0 (public domain).

Each sound is named after its file ("Kick_01.wav" becomes "kick 01"); rename the files first for nicer names. Names the app
recognises for placing sounds on pads: kick, snare, closed hat, open hat, clap, rim, shaker, low tom, mid tom, high tom,
crash, ride, cowbell, perc, clave, fx. Silence at either end is trimmed and every sound is normalised to -1 dBFS.
Needs only Python 3 (numpy is used if it is installed, for faster resampling).
"""
import argparse, json, math, os, re, struct, sys, wave

SR = 44100
GAP = int(0.01 * SR)          # 10 ms of silence between sounds
MAX_SECS = 6.0                # longest single sound kept


def read_wav(path):
    """Mono float samples and the sample rate. Handles 8/16/24/32-bit PCM and 32-bit float WAV."""
    with open(path, 'rb') as f:
        data = f.read()
    if data[:4] != b'RIFF' or data[8:12] != b'WAVE':
        sys.exit(f'{path}: not a WAV file (convert it to WAV first)')
    o, fmt, pcm = 12, None, None
    while o + 8 <= len(data):
        cid, size = data[o:o + 4], struct.unpack('<I', data[o + 4:o + 8])[0]
        if cid == b'fmt ':
            tag, ch, sr = struct.unpack('<HHI', data[o + 8:o + 16])
            bits = struct.unpack('<H', data[o + 22:o + 24])[0]
            if tag == 0xFFFE:   # WAVE_FORMAT_EXTENSIBLE: the real format is in the sub-format GUID
                tag = struct.unpack('<H', data[o + 32:o + 34])[0]
            fmt = (tag, ch, sr, bits)
        elif cid == b'data':
            pcm = data[o + 8:o + 8 + size]
        o += 8 + size + (size & 1)
    if not fmt or pcm is None:
        sys.exit(f'{path}: could not find the audio in this WAV')
    tag, ch, sr, bits = fmt
    bw = bits // 8
    n = len(pcm) // (bw * ch)
    out = [0.0] * n
    for i in range(n):
        s = 0.0
        for c in range(ch):
            p = (i * ch + c) * bw
            b = pcm[p:p + bw]
            if tag == 3 and bits == 32:
                v = struct.unpack('<f', b)[0]
            elif bits == 8:
                v = (b[0] - 128) / 128
            elif bits == 16:
                v = struct.unpack('<h', b)[0] / 32768
            elif bits == 24:
                v = int.from_bytes(b, 'little', signed=True) / 8388608
            elif bits == 32:
                v = struct.unpack('<i', b)[0] / 2147483648
            else:
                sys.exit(f'{path}: {bits}-bit audio is not supported')
            s += v
        out[i] = s / ch
    return out, sr


def resample(x, sr):
    if sr == SR:
        return x
    n = int(len(x) * SR / sr)
    try:
        import numpy as np
        t = np.arange(n) * (sr / SR)
        return list(np.interp(t, np.arange(len(x)), np.asarray(x)))
    except ImportError:
        r = sr / SR
        out = []
        for i in range(n):
            p = i * r
            j = int(p)
            f = p - j
            a = x[j] if j < len(x) else 0.0
            b = x[j + 1] if j + 1 < len(x) else a
            out.append(a + (b - a) * f)
        return out


def tidy(x):
    """Trim silence at both ends (keeping 3 ms before the attack), cap the length, normalise to -1 dBFS."""
    pk = max((abs(v) for v in x), default=0.0)
    if pk < 1e-5:
        return []
    thr = pk * 0.01
    a = next(i for i, v in enumerate(x) if abs(v) >= thr)
    b = len(x) - next(i for i, v in enumerate(reversed(x)) if abs(v) >= thr * 0.5)
    a = max(0, a - int(0.003 * SR))
    b = min(len(x), b + int(0.03 * SR), a + int(MAX_SECS * SR))
    x = x[a:b]
    g = 0.891 / pk
    x = [v * g for v in x]
    fade = min(len(x) // 4, int(0.005 * SR))     # a few ms fade at the end so nothing clicks
    for i in range(fade):
        x[len(x) - 1 - i] *= i / fade
    return x


def name_of(path):
    n = os.path.splitext(os.path.basename(path))[0].lower()
    n = re.sub(r'[_\-.]+', ' ', n)
    n = re.sub(r'\s+', ' ', n).strip()
    return n[:14] or 'sound'


def main():
    ap = argparse.ArgumentParser(description='Pack WAV files into a Signal Path factory kit.')
    ap.add_argument('--id', required=True, help='short id: lowercase letters, digits and dashes, e.g. acoustic')
    ap.add_argument('--name', help='name shown in the app, e.g. "acoustic kit"')
    ap.add_argument('--by', default='', help='credits, e.g. "Freesound: user1, user2"')
    ap.add_argument('files', nargs='+')
    a = ap.parse_args()
    if not re.fullmatch(r'[a-z0-9-]+', a.id):
        sys.exit('--id must be lowercase letters, digits and dashes')
    out, sounds, seen = [], [], set()
    for path in a.files:
        x, sr = read_wav(path)
        x = tidy(resample(x, sr))
        if not x:
            print(f'skipped {path}: silent')
            continue
        nm = name_of(path)
        k = 2
        while nm in seen:
            nm = f'{name_of(path)[:11]} {k}'
            k += 1
        seen.add(nm)
        start = len(out)
        out.extend(x)
        sounds.append({'n': nm, 'a': start, 'b': len(out)})
        out.extend([0.0] * GAP)
        print(f'{nm:16s} {len(x) / SR:5.2f} s')
    if not sounds:
        sys.exit('no sounds to pack')
    wav_name, json_name = f'kit-{a.id}.wav', f'kit-{a.id}.json'
    with wave.open(wav_name, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<h', max(-32767, min(32767, int(round(v * 32767))))) for v in out))
    name = a.name or a.id + ' kit'
    with open(json_name, 'w') as f:
        json.dump({'id': a.id, 'name': name, 'sr': SR, 'license': 'CC0 1.0', 'by': a.by, 'sounds': sounds}, f, indent=1)
    mb = round(os.path.getsize(wav_name) / 1e6, 1)
    kits = {'kits': []}
    if os.path.exists('kits.json'):
        with open('kits.json') as f:
            kits = json.load(f)
    kits['kits'] = [k for k in kits.get('kits', []) if k.get('id') != a.id]
    kits['kits'].append({'id': a.id, 'name': name, 'n': len(sounds), 'mb': mb, 'by': a.by})
    with open('kits.json', 'w') as f:
        json.dump(kits, f, indent=1)
    print(f'\nwrote {wav_name} ({mb} MB), {json_name} and kits.json: {len(sounds)} sounds')
    if mb > 3:
        print('note: over 3 MB; consider fewer or shorter sounds')


if __name__ == '__main__':
    main()
