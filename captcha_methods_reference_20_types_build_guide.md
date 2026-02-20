# CAPTCHA Methods Reference (20 Types) — Build Guide

This document is a **build-oriented** reference for creating a **CAPTCHA demo/testing website** (education + UI testing). For each method, you’ll get:
- **How it looks** (UI layout)
- **How it works** (verification flow, high-level)
- **What the user does**
- **How to build it (front-end + mock back-end)** — concrete steps, data structures
- **Where to source assets** (public-domain / free-to-use images, icons, audio)
- **SVG / Canvas / CSS notes**

> Safety note: This guide helps you **implement demos**, not bypass CAPTCHAs.

---

## Global Build Setup (applies to all 20)

### Recommended project structure (for your Antigravity site)
- `/pages` or routes:
  - `/captchas` (gallery)
  - `/captchas/<type>` (one page per type)
- `/components/captcha/` shared components:
  - `CaptchaFrame` (title, instructions, widget, logs)
  - `AttemptCounter`
  - `RefreshButton`
  - `TokenBadge` (shows “verified token issued”)
  - `EventLogPanel` (captures interactions)
- `/assets/`
  - `/images/` (tile sets, puzzle images)
  - `/icons/` (SVGs)
  - `/audio/` (audio captcha samples)

### Mock back-end (for a local demo)
Even if you host static, simulate a server with:
- In-memory store (or localStorage) for:
  - `challengeId`
  - `expectedAnswer` (or expected region/angle/etc.)
  - `expiresAt`
  - `attemptsRemaining`
- “Issue token” function that returns something like:
  - `captchaToken = base64(challengeId + timestamp + result)`

### Asset sourcing (safe defaults)
Use free/public sources and keep attribution if required:
- **Images**:
  - Unsplash (free license), Pexels, Pixabay
  - Wikimedia Commons (watch license per file)
  - Openverse (filter by license)
- **Icons (SVG)**:
  - Heroicons, Lucide, Feather icons
  - Font Awesome Free (SVG)
- **Audio**:
  - Public domain number recordings (or generate your own recording)
  - Freesound (license-dependent)
- **Noise textures**:
  - Create your own with canvas (recommended)

### Accessibility baseline
Every CAPTCHA demo page should include:
- Keyboard navigation support
- High-contrast mode toggle
- “Try another challenge” option
- Alternative method (ex: audio option for text/image tasks)

---

## 1) Distorted Text (OCR CAPTCHA)

### What it looks like
Image with warped characters + noise, a text field, Refresh, (optional) Audio.

### How it works
Server generates random string; client renders an image; user types string; verify.

### What the user does
Read characters → type → submit.

### How to build it
**Front-end**
- Render text CAPTCHA using `<canvas>`:
  1. Generate `solution` string (e.g., `A7K9Q`)
  2. Draw background gradient/noise
  3. Draw text with rotation per character
  4. Add noise lines + dots
  5. Export `canvas.toDataURL()` into `<img>`
- Input field validates length and triggers verify.

**Mock back-end logic**
- Store `solution` + `expiresAt` in memory/localStorage keyed by `challengeId`.
- Verify compares normalized input:
  - `trim`, optional `toUpperCase`, ignore spaces.

### Where to source assets
- No external images needed: generate everything in canvas.
- Optional font: use a Google Font (ensure license). For realism use a standard sans.

### SVG / Canvas notes
- Use canvas for distortion and noise.
- Keep distortion moderate; too much becomes unusable.

### Useful extras
- Expire after 2 minutes.
- 3 attempts then force refresh.

---

## 2) Image Grid Object Selection (Tile CAPTCHA)

### What it looks like
Prompt text + 3×3 or 4×4 image tiles, selection highlight, Verify, Refresh.

### How it works
User picks tiles containing a target class; system compares to ground truth.

### What the user does
Click all matching tiles → Verify.

### How to build it
**Front-end**
- `tiles = [{src, hasTarget:boolean}, ...]` for each round.
- Grid component:
  - On click, toggle `selected` state
  - Verify checks: all `hasTarget` tiles selected AND no non-target selected
- Optional multi-round:
  - If correct, load next `round`

**Mock back-end logic**
- Store per-round answer set (indexes of target tiles).

### Where to source public images
- Search free photos for targets (traffic lights, buses, stairs, bridges):
  - Unsplash/Pexels/Pixabay
- Recommended approach:
  - Build your own small dataset (20–50 images), categorize manually.

### SVG / UI elements
- Use SVG check overlay on selected tiles.
- Add a subtle border highlight.

### Useful extras
- Include “edge case” tiles where object is partial.
- Provide Refresh.

---

## 3) Single Image “Click the Object/Area”

### What it looks like
One image + instruction + click marker + Verify.

### How it works
System checks whether click coordinate falls in valid region.

### What the user does
Click the requested object/area → Verify.

### How to build it
**Front-end**
- Render image in a fixed container.
- On click, compute click coordinates relative to image.
- Show marker (SVG circle) at click point.

**Answer model**
- Store target region as:
  - Bounding box: `{x,y,w,h}` in normalized 0..1 coordinates, OR
  - Polygon array `[{x,y}, ...]` normalized.

**Verification**
- If click point inside region (bbox or polygon) → pass.

### Where to source images
- Use simple photos with clear single object:
  - bicycle, car, cat, flower
- Unsplash/Pexels are perfect.

### SVG / Canvas notes
- Use SVG overlay for marker and region debug (optional dev mode).

---

## 4) Checkbox “I’m not a robot” (Challenge-Gated)

### What it looks like
Checkbox widget with spinner; may escalate to another challenge modal.

### How it works
Risk scoring determines pass or step-up.

### What the user does
Click checkbox → if prompted, solve next challenge.

### How to build it
**Front-end**
- Widget states:
  - `idle` → `checking` → `passed` OR `challengeRequired`
- If `challengeRequired`, open modal (use your tile or puzzle components).

**Mock risk engine**
- Compute a simple score from:
  - Time on page
  - Number of pointer moves
  - Whether user scrolled
- If score below threshold → require step-up.

### Assets
- Checkbox + spinner can be SVG.

---

## 5) Invisible / Background CAPTCHA

### What it looks like
No visible widget; user submits form normally.

### How it works
Client collects interaction metrics; server issues token if low risk.

### What the user does
Nothing special.

### How to build it
**Front-end**
- Add an invisible script module that captures:
  - `timeOnPage`, `keydownCount`, `pointerMoveCount`, `scrollDistance`
- On form submit, compute a score and show either:
  - “Verified silently” (token issued)
  - Or “Step-up required” (open a challenge)

### Assets
- None.

### Useful extras
- Add an educational debug panel showing which signals triggered step-up.

---

## 6) Passive Widget (Score-based, rarely puzzles)

### What it looks like
A small verification card that usually auto-verifies.

### How it works
Like invisible scoring but with a visible container.

### What the user does
Usually waits; sometimes clicks continue.

### How to build it
- Render widget with status text:
  - “Verifying…” then “Verified”
- Behind the scenes reuse scoring from #5.

### Assets
- SVG badge icon (“shield”, “check”).

---

## 7) Audio CAPTCHA

### What it looks like
Audio player + input field + Replay + New audio.

### How it works
User types spoken digits/words; validate against expected.

### What the user does
Play → type → submit.

### How to build it
**Front-end**
- Use `<audio controls>` or custom play button.
- Input and verify.

**Mock back-end**
- Randomly pick one of your audio files with known transcript.

### Where to source audio
Best: record your own digits (0–9) and concatenate.
- Or use public-domain recordings (verify license).
- Add noise in browser by layering a low-volume noise track (optional).

### Accessibility note
Audio is already an alternative; provide a non-audio fallback for hearing impaired.

---

## 8) Simple Math / Logic Question

### What it looks like
Text question + input.

### How it works
Compare answer.

### What the user does
Answer → submit.

### How to build it
- Question bank array:
  - `{prompt:"7 + 4", answer:"11"}`
- Random select and validate.

### Assets
- None.

### Useful extras
- Include words variant (“seven plus four”).

---

## 9) Slider “Drag to Complete”

### What it looks like
Track + draggable thumb + success state.

### How it works
Validates continuous drag interaction.

### What the user does
Drag thumb to end.

### How to build it
**Front-end**
- Use pointer events:
  - `pointerdown` start
  - `pointermove` update thumb x
  - `pointerup` finalize
- Require:
  - Minimum drag duration (e.g., > 400ms)
  - Smooth movement (no single jump)
  - End position >= 95%

### Assets
- Thumb and track can be pure CSS or SVG.

---

## 10) Jigsaw “Missing Piece” Slider Puzzle

### What it looks like
Image with cut-out hole + puzzle piece + slider.

### How it works
User aligns piece to hole; verify alignment within tolerance.

### What the user does
Drag slider until piece fits.

### How to build it
**Canvas approach (recommended)**
1. Choose a background image.
2. Randomize hole x position.
3. Draw background.
4. Create a jigsaw-shaped mask path.
5. Cut out hole region.
6. Extract the piece image from original and render it as draggable layer.
7. Slider moves piece horizontally.
8. Verify if `abs(pieceX - holeX) <= tolerance`.

### Where to source images
- Use high-contrast scenery photos from Unsplash/Pexels.
- Avoid faces/logos.

### SVG notes
- Jigsaw shape can be an SVG path used as a mask.

---

## 11) Rotate-to-Upright Puzzle

### What it looks like
Object image rotated + rotate buttons/dial.

### How it works
Pass if final angle near target.

### What the user does
Rotate until upright → submit.

### How to build it
**Front-end**
- Store `angle` state.
- Buttons adjust angle by ±15°.
- Optional drag dial for fine control.
- Verify `min(|angle - target|, 360-|...|) <= tolerance`.

### Where to source images
- Use simple icons or photos:
  - umbrellas, animals, tools
- Best approach: use SVG icons (clean + easy) from Lucide/Heroicons.

### SVG notes
- Rotating SVG is crisp at all sizes.

---

## 12) Shape/Pattern Matching

### What it looks like
Target card + 6–12 option cards.

### How it works
Choose exact match (shape, icon, orientation, color).

### What the user does
Select matching card.

### How to build it
- Build a dataset:
  - `target: {icon:"chair", rotation:90, color:"blue"}`
  - options array with one exact match and decoys.
- Use SVG icons and apply transforms.

### Asset sourcing
- SVG icon libraries (Lucide/Heroicons) or your own custom SVG set.

---

## 13) Gamified 3D Seat/Arrow Puzzle (FunCaptcha-style)

### What it looks like
Left “Match This!” clue + right isometric seat grid + arrow buttons + multi-round.

### How it works
Each round maps clue to target seat coordinate; verify final position + interactions.

### What the user does
Use arrows to move avatar to seat matching the clue.

### How to build it (demo version)
**Build choice A: 2D grid (fastest)**
- Represent seats in a 5×5 grid.
- Each seat has labels (numbers/icons).
- Avatar is a highlighted marker.
- Arrows move avatar (x/y).

**Build choice B: Isometric “3D look” (still simple)**
- Use CSS transforms to skew the grid (`transform: rotateX(60deg) rotateZ(45deg)`).
- Seat tiles are divs with pseudo-3D shadows.

**Clue system**
- Left panel shows:
  - A number + an icon (SVG)
- Seats have both printed.
- Target seat is the unique seat matching both.

**Verification**
- Pass if avatar coordinate equals target coordinate.
- Add interaction realism for demo:
  - Require at least N arrow presses (e.g., 3)
  - Require time spent >= 1s

### Where to source assets
- Seats: draw as SVG or simple 3D-ish rectangles.
- Icons: Lucide/Heroicons.
- Background: gradient or subtle noise.

### Notes
- Multi-round: prepare 10 clue/target pairs.

---

## 14) Behavioral Biometrics (Interaction-Based)

### What it looks like
Usually nothing; optionally “Analyzing interaction…”

### How it works
Collects behavior features and scores them.

### What the user does
Just uses the page.

### How to build it
**Front-end capture**
- Collect features:
  - Pointer speed average
  - Number of stops/starts
  - Scroll events count
  - Typing intervals variance
- Compute a simple score (heuristic, not invasive).

**Demo UI**
- Show a live graph (optional): pointer speed over time.

### Assets
- None.

---

## 15) Device/Browser Fingerprinting Signals (Educational Demo)

### What it looks like
Invisible; for your demo, show a “device summary” panel.

### How it works
Combines browser properties to form a stable-ish signature and risk flags.

### What the user does
Nothing.

### How to build it
- Read safe, non-sensitive properties:
  - timezone, language, screen size, platform, touch support
- Hash them (for demo only) into `fingerprintId`.
- Simulate risk rules:
  - “Headless detected” (only in demo if you toggle)
  - “Too many changes between refreshes”

### Assets
- None.

---

## 16) Proof-of-Work CAPTCHA (Client Computation)

### What it looks like
Spinner/progress bar; sometimes no UI.

### How it works
Client solves a small CPU puzzle; server verifies quickly.

### What the user does
Waits.

### How to build it
- Server issues token + difficulty `d`.
- Client finds nonce such that `sha256(token+nonce)` starts with `d` zeros.
- Show progress:
  - attempts count
  - elapsed time
- Keep difficulty low for phones.

### Assets
- None.

---

## 17) JavaScript “Browser Integrity” Interstitial

### What it looks like
“Checking your browser…” page, then redirect.

### How it works
Requires JS execution to compute/set cookies and pass.

### What the user does
Wait.

### How to build it
- Create an interstitial route:
  1. On load, run JS to compute a value (simple hash)
  2. Store it in cookie/localStorage
  3. Redirect to target page
- Verify on the target page that the cookie exists.

### Assets
- Spinner SVG.

---

## 18) Progressive Step-Up (Escalation Ladder)

### What it looks like
Starts with no CAPTCHA → then checkbox → then harder game/puzzle.

### How it works
Risk engine escalates based on attempt frequency and signals.

### What the user does
Completes whatever step-up appears.

### How to build it
- Build a state machine:
  - `level 0: none`
  - `level 1: checkbox`
  - `level 2: tiles`
  - `level 3: seat puzzle`
  - `level 4: OTP`
- Escalate when:
  - too many submits
  - too fast
  - too many failures

### Assets
- Reuse existing widgets.

---

## 19) Honeypot Fields + Timing Trap

### What it looks like
Nothing (hidden field).

### How it works
Bots fill hidden field; humans don’t. Timing trap flags too-fast submits.

### What the user does
Nothing.

### How to build it
- Add hidden input:
  - `name="company_website"` hidden via CSS but not display:none for some bots.
- On submit:
  - If value present → fail
  - If time between page load and submit < 2 seconds → fail (demo)

### Assets
- None.

---

## 20) Step-Up Verification via OTP (Email/SMS-style)

### What it looks like
6-digit input boxes + resend timer.

### How it works
Server issues OTP; user enters it; verify within expiry.

### What the user does
Get code → enter → submit.

### How to build it (demo)
- Generate 6-digit code.
- Display it in a fake “inbox” panel on the page (demo-only).
- Input UI:
  - 6 boxes with auto-advance
  - paste support
- Verify:
  - expiry (e.g., 2 minutes)
  - resend cooldown (e.g., 30 seconds)

### Assets
- Numeric keypad SVG icon (optional).

---

# Asset Pack Plan (so Antigravity can generate everything cleanly)

## Images (recommended categories)
Create `/assets/images/tiles/` with subfolders:
- `traffic_lights/` (10–20 images)
- `bridges/` (10–20)
- `stairs/` (10–20)
- `buses/` (10–20)
- `crosswalks/` (10–20)
Also:
- `/assets/images/single/` for single-click CAPTCHAs (bicycle, cat, flower)
- `/assets/images/jigsaw/` for jigsaw backgrounds (landscapes)

## Icons (SVG)
Create `/assets/icons/`:
- `chair.svg`, `shield-check.svg`, `arrow-left.svg`, `arrow-right.svg`
- plus a small set of category icons used in puzzles

## Audio
Create `/assets/audio/`:
- `digits_0.mp3 ... digits_9.mp3` (your own recordings)
- optional `noise.mp3`

---

# How to make the demo feel “real” without copying any vendor

- Use **your own UI design** (don’t clone Google/Microsoft widgets)
- Use **generic labels**: “Human check” instead of brand phrases
- Make challenges **configurable**:
  - number of rounds
  - tolerance thresholds
  - timeouts
- Add a **developer mode**:
  - show expected answers and regions (toggle)

---

When you’re ready, we’ll convert this into an Antigravity build prompt that:
- generates the full site
- creates reusable components for each CAPTCHA type
- bundles a starter asset pack plan
- includes a logging panel for testing UX and interaction flows

