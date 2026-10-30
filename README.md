# Signal Path

**A synth lab for the iPhone.** Signal Path is a playable synthesizer with a live oscilloscope, and every lesson happens on the instrument itself. Turn a knob and you hear the change, see it on the scope, and learn why it sounds that way. Then you can try the same idea on a real synth.

It runs as a single web page, installs to the home screen like a native app, and works offline.

---

## The synth

A two-oscillator subtractive synth, laid out as a row of stomp-box pedals. Tap a pedal to open its knobs, or stomp its footswitch to turn that section on or off. A section that's off passes the signal straight through.

| Section | What's in it |
|---|---|
| **Osc 1** | Sine, triangle, saw, pulse (with width), **wavetable** (8-frame morph) and **formant** (vowel) waves · octave · unison / super-wave with up to 7 detuned voices · glide · band-limiting on/off, so you can hear aliasing |
| **Osc 2** | Sine, triangle, saw, pulse · octave, semitone and fine tune · **hard sync**, **FM** and **ring mod** against Osc 1 |
| **Mix** | Oscillator levels, noise, master volume, and the **Mono / Poly** switch (8 voices) |
| **Filter** | LP24, LP12, HP, BP and LP+BP modes · cutoff, resonance, drive, key tracking and envelope amount |
| **Env** | Amp and filter ADSR envelopes · the filter envelope doubles as a mod envelope, routable to cutoff, pitch, FM amount and wave shape |
| **LFO** | Triangle, square, ramp down, ramp up and sample & hold · free rate or tempo-synced divisions · routes to pitch, cutoff and pulse width |
| **FX** | Six pedals in signal order, each with its own on/off: **Trem / Pan / Wah** → **Amp + cab** (small, combo, clean) → **3-band EQ** → **Chorus / Flanger / Phaser** → **Delay** (free or synced, ping-pong) → **Reverb** |
| **Arp** | Up, down, up/down and random · 1–4 octaves · gate length · rate divisions synced to a shared tempo |

The one-octave keyboard (C to C) has octave shift and **Hold**. In Poly or Arp mode, Hold makes each key a toggle, so you can build up a chord or an arp pattern one note at a time. On a computer, the `A W S E D F T G Y H U J K` keys play too.

## Seeing the sound

The **Scope** page is a bench instrument for the signal:

- **Wave**: a rock-steady oscilloscope trace that locks to the note's pitch
- **Spectrum**: a live FFT with log or linear frequency scale
- **Spectro**: a scrolling spectrogram, about 8 seconds wide, that you can scrub through
- **Env**: a chart recorder for the control signals (amp and filter envelopes, LFO, cutoff) over the last 4 seconds

You can probe three **test points** in the signal chain: the raw oscillators, the filter output, or the final output. Touch and hold the screen for a **measuring cursor** that reads time, level, frequency and harmonic number. **Run / Stop** freezes the picture like a real scope, a **ghost** trace shows the signal before the filter so you can see what it removed, and the **?** key explains what every chart is plotting.

The Patch page has its own mini scope, so the graph stays in view while you turn knobs. While a knob moves, the coach panel turns into a live readout of that one parameter, with its own small graphic.

## Lessons

**104 interactive lessons in 12 chapters**, written to take a few minutes each:

| Chapter | Covers |
|---|---|
| Tools | Using the app, its pages and knobs, and what every chart shows |
| Foundations | Waves, pitch, harmonics, tuning, phase, loudness, filters and noise |
| Envelopes & LFO | Shaping notes over time, modulation, and how it all connects |
| Filters & drive | Filter types and classic filters, tracking, saturation and gain staging |
| Oscillators | Detune, subs, unison, drift, sync, FM, ring mod, additive, wavetables and formants |
| Effects | The effects chain pedal by pedal, delay time scales, stereo and space |
| Performance | Polyphony, voicing, glide, the arpeggiator, tempo sync, velocity and controllers |
| Sound design craft | A patching routine, analysing sounds, making things bigger, mixing |
| Recipes: basses & leads | Sub, acid, Reese, wobble, sync and supersaw leads, chiptune |
| Recipes: pads, keys & FX | Brass, strings, pads, choir, organ, keys, bells, drums and effects |
| Synth history | From modular and the first polysynths to digital, virtual analog and software |
| Deep dives | The engineering underneath: sampling, filters, FFTs, physical models |

How the lessons work:

- **They happen on the synth.** Each step loads the sound it needs, points at the knob to turn, and opens the right scope view.
- **Steps are checked, but you move on yourself.** The app notices when you've done a step and marks it complete. It only advances when you press Next.
- **Learn more** opens the deeper explanation behind a step, with diagrams and the math, when you want it.
- **Real-synth tips** show how the same idea works on hardware such as a Nord.
- **Progress is saved**, and a Continue card takes you back to where you stopped. You can minimise a lesson to a slim bar and keep playing, or exit at any time.
- **Free play** gives you the whole synth with no lesson running.

## Patch memory

Patch memory is laid out like a hardware synth's: **8 banks × 8 tracks**, all visible at once.

- Factory sounds to start from, plus empty banks for your own patches
- **Write** saves the current sound to any track, and tracks can be renamed
- **Compare** flips between your edited sound and the stored version
- **Tape** backs up every bank to a file and loads it back
- The sound you were last playing is restored when you reopen the app

## Built for the phone

- Black OLED look with line-traced graphics and knobs that are easy to turn with a thumb
- Installs to the iPhone home screen and runs full screen
- Works fully offline after the first visit
- Audio runs in an AudioWorklet: 8-voice polyphony, band-limited oscillators and a Moog-style ladder filter
- Goes quiet automatically when you leave the app, so nothing keeps droning in the background

---

## Running it

Everything lives in `index.html`. The other files make it installable and let it work offline. To publish, put all the files at the top level of a GitHub repo and turn on **Settings → Pages** (deploy from `main`, root folder). Then open the site in Safari and choose **Share → Add to Home Screen**.

When you change `index.html`, also bump `VERSION` in `sw.js` (for example `sp-v27` → `sp-v28`) so installed copies pick up the update. Close and reopen the app once to load it.
