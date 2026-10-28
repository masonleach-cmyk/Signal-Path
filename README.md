# Signal Path

A synth learning lab for the phone: a small mono synth, a live oscilloscope / spectrum / envelope view, and guided lessons from the basics up to the Moog ladder and FM.

Everything is in `index.html`. The other files make it installable on the iPhone home screen and usable offline.

## Publish with GitHub Pages

1. Create a new repository and upload every file in this folder to its top level (no subfolders).
2. In the repo, go to **Settings → Pages**. Under *Build and deployment*, choose **Deploy from a branch**, pick `main` and `/ (root)`, and save.
3. After a minute the site is live at `https://<your-username>.github.io/<repo-name>/`.

## Add to the iPhone home screen

Open that URL in **Safari**, tap **Share → Add to Home Screen**. It launches full screen with its own icon and works offline after the first visit.

## Updating

Edit `index.html`, then bump `VERSION` in `sw.js` (for example `sp-v3` → `sp-v4`) so phones fetch the new version. Close and reopen the home-screen app once to load it.

| File | Purpose |
|---|---|
| `index.html` | The whole app: synth engine, scope, lessons, UI |
| `manifest.webmanifest` | App name, colours and icons for installing |
| `sw.js` | Offline cache |
| `apple-touch-icon.png` | iPhone home-screen icon (180×180) |
| `icon-192.png`, `icon-512.png`, `icon-maskable-512.png` | Icons for other platforms |
| `favicon-32.png` | Browser tab icon |
| `.nojekyll` | Tells GitHub Pages to serve files as-is |
