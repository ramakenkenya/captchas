# CAPTCHA Methods Reference (20 Types)

Purpose of this document: a practical, implementation-oriented reference describing **20 common CAPTCHA / human verification methods**. For each method, you get:
- **What it looks like** (UI elements and typical screens)
- **How it works** (high-level verification logic and signals)
- **What the user does** (step-by-step)
- **Implementation notes** (what to reproduce on a demo/testing webpage)
- **Failure modes & UX notes** (common mistakes, accessibility, and friction)

> Scope note: This is written for building a **demo/testing webpage** and for understanding **how these methods behave**. It does **not** provide instructions to bypass CAPTCHAs.

---

## 1) Distorted Text (OCR CAPTCHA)

### Description
A classic CAPTCHA where the user types characters displayed in a distorted image.

### How it looks
- A small image with warped/curved letters and numbers
- Background noise (lines, dots, squiggles)
- A text input field below the image
- Often includes a “refresh” icon and sometimes an “audio” icon

### How it works
- Server generates a random token (e.g., 5–8 chars)
- Server renders the token into an image with distortion + noise
- User input is compared to the original token stored server-side (or encrypted in the session)
- Anti-abuse additions may include rate limits, IP reputation, device fingerprints

### What the user does
1. Read the characters in the image.
2. Type them into the input.
3. Submit.

### Implementation notes for your demo page
- Build a component that:
  - Displays an image with distorted text
  - Provides “refresh” to regenerate a new image
  - Has an input and submit button
- For a realistic demo, simulate:
  - Case insensitivity
  - Expiry timer (e.g., 2 minutes)
  - 3-attempt limit before refresh required

### Failure modes & UX notes
- Hard for visually impaired users; always offer audio or an alternative
- Too much distortion increases user drop-off

---

## 2) Image Grid Object Selection (Tile CAPTCHA)

### Description
User selects all tiles that contain a target object (traffic lights, bridges, stairs, buses, crosswalks).

### How it looks
- Prompt: “Select all images with **traffic lights**”
- 3×3 or 4×4 grid of photos
- Tiles are clickable; selected tiles highlight
- “Verify” button
- Sometimes “Click verify once there are none left” and grid updates

### How it works
- User selections are evaluated against labeled regions (pre-annotated or model-based)
- System may consider:
  - Accuracy of selected tiles
  - Response timing
  - Pointer movement patterns
  - Risk score from other signals

### What the user does
1. Read prompt.
2. Click tiles that match the object.
3. Click Verify.

### Implementation notes
- Create a grid component with:
  - Prompt text
  - Image tile array (with ground-truth flags)
  - Multi-step rounds (optional) where correct selections load a new grid
- Add small “partial tile” edge cases (object spans tiles)

### UX notes
- Users get frustrated when objects partially appear on edges
- Provide “skip/refresh” option

---

## 3) Single Image “Click the Object/Area”

### Description
Instead of a grid, the user clicks a specific object or point within one image.

### How it looks
- One photo with instruction: “Click the bicycle” or “Click the center of the flower”
- Cursor click marks may appear
- “Verify” button

### How it works
- System checks if click coordinate falls within a target polygon/region
- Often combined with risk scoring and behavioral signals

### What the user does
1. Read the instruction.
2. Click the specified object/area.
3. Submit.

### Implementation notes
- Use an image with an overlay map of “valid regions”
- Store regions as polygons or bounding boxes
- Show a small marker where user clicked

### UX notes
- On mobile, precision is harder; allow tolerance radius

---

## 4) Checkbox “I’m not a robot” (Challenge-Gated)

### Description
A checkbox that may instantly pass low-risk users or escalate to a challenge (image puzzles, etc.).

### How it looks
- Widget area with checkbox
- “I’m not a robot” label
- Spinner while verifying
- If suspicious: transitions to image puzzle

### How it works
- Client collects interaction signals (focus, mouse/touch patterns)
- Server returns a risk score
- If score is low: issue a verification token
- If score is high: require a secondary challenge

### What the user does
1. Click checkbox.
2. If prompted, solve an additional puzzle.

### Implementation notes
- For demo: simulate risk levels:
  - “Low risk” instantly passes
  - “High risk” triggers a follow-on challenge modal

### UX notes
- Avoid repeated challenges for legitimate users

---

## 5) Invisible / Background CAPTCHA (No UI)

### Description
No puzzle shown. Verification happens in the background based on risk scoring.

### How it looks
- Nothing visible, or a small badge/logo in corner
- User just submits a form normally

### How it works
- Client runs a script that:
  - Collects browser/device signals
  - Observes interaction (scroll, typing cadence)
  - Requests a token from server
- Server evaluates and returns allow/deny or “step-up” requirement

### What the user does
- Nothing special; they just use the site.

### Implementation notes
- For demo:
  - Display a “risk meter” for educational purposes
  - Show what signals you’re simulating (time on page, typing events)

### UX notes
- Best UX when it works; must have a fallback for false positives

---

## 6) “Passive” Widget (Score-based, rarely puzzles)

### Description
A widget is present, but in many cases it issues a token without puzzles.

### How it looks
- A small verification panel (similar to checkbox style)
- Brief “verifying” animation

### How it works
- Similar to invisible/background methods but with explicit widget integration
- May run periodic checks and refresh tokens

### What the user does
- Usually nothing; occasionally clicks “Continue”

### Implementation notes
- Build a widget component that:
  - Animates “verifying”
  - Returns a token after simulated checks

---

## 7) Audio CAPTCHA (Spoken Digits/Words)

### Description
Accessibility alternative: listen to audio and type what you hear.

### How it looks
- Audio player controls
- A text input
- “Replay” and “New audio” buttons

### How it works
- Server generates a random phrase or digits
- Audio is synthesized or recorded with noise overlay
- User input compared to expected phrase

### What the user does
1. Play audio.
2. Type the spoken content.
3. Submit.

### Implementation notes
- For demo:
  - Use pre-recorded audio files
  - Include background noise simulation
  - Implement replay limits

### UX notes
- Provide captions? (Usually no, to preserve purpose)
- Consider hearing-impaired alternatives

---

## 8) Simple Math / Logic Question CAPTCHA

### Description
User answers a simple question: arithmetic or basic logic.

### How it looks
- Text prompt: “What is 7 + 4?”
- Input field and submit button

### How it works
- Server generates a question + expected answer
- May randomize phrasing (“seven plus four”)
- Validates answer on submit

### What the user does
1. Read question.
2. Enter answer.
3. Submit.

### Implementation notes
- Include a question bank with:
  - Addition/subtraction
  - “Type the third word in this phrase”
  - “Select the color blue” (simple UI)

### UX notes
- Weak against sophisticated bots; best for low-risk contexts

---

## 9) Slider “Drag to Complete”

### Description
User drags a slider handle from left to right to confirm they can interact.

### How it looks
- Horizontal track
- Slider thumb
- Instruction: “Slide to verify”
- Progress fill and success state

### How it works
- Validates drag events:
  - Continuous pointer/touch movement
  - Velocity/acceleration patterns
  - No instant jump from start to end
- Often combined with device fingerprinting

### What the user does
1. Press slider thumb.
2. Drag to the end.
3. Release.

### Implementation notes
- Track pointer events and compute:
  - Drag duration
  - Smoothness
  - Number of direction changes
- Mark success if drag reaches threshold with “human-like” path

### UX notes
- On mobile, allow forgiving thresholds

---

## 10) Jigsaw “Missing Piece” Slider Puzzle

### Description
User drags a puzzle piece horizontally into a cut-out slot.

### How it looks
- Background image with a missing jigsaw-shaped hole
- A draggable jigsaw piece shown separately
- Slider below to move the piece left/right

### How it works
- Server randomizes cut-out position
- Client renders piece and hole
- On completion, server checks alignment offset within tolerance
- Behavioral signals: drag path, pauses, micro-corrections

### What the user does
1. Drag slider to move puzzle piece.
2. Align piece to hole.
3. Release to submit.

### Implementation notes
- For demo:
  - Use canvas to render the cut-out mask
  - Randomize x-position
  - Validate within ±5–10px

### UX notes
- Provide clear visual feedback on near-match

---

## 11) Rotate-to-Upright (Image Rotation)

### Description
User rotates an object until it’s upright.

### How it looks
- Image of an object rotated randomly
- Rotate buttons (left/right) or a rotation dial
- Prompt: “Rotate the object upright”

### How it works
- Server sets a target orientation (e.g., 0°)
- User adjusts rotation
- Pass if final angle is within tolerance (e.g., ±10°)
- Tracks interaction timing and adjustment patterns

### What the user does
1. Click rotate controls.
2. Make object upright.
3. Submit.

### Implementation notes
- Use CSS transforms to rotate image
- Store current angle; success when angle ≈ target

---

## 12) Shape/Pattern Matching Puzzle

### Description
User matches a pattern (same shape, same icon, same orientation) among options.

### How it looks
- “Match this shape” panel
- A set of clickable options (cards/tiles)
- Sometimes multiple rounds

### How it works
- Ground-truth mapping of which option matches target
- May include decoys with near-matches
- Can be evaluated deterministically

### What the user does
1. Observe target.
2. Select the matching option.
3. Continue/submit.

### Implementation notes
- Build a “target + options” component
- Add randomization and small variations

---

## 13) Gamified 3D Seat/Arrow Puzzle (FunCaptcha-style)

### Description
A mini-game: “Using the arrows, move the person to the indicated seat.” Common in high-risk login/signup flows.

### How it looks
- Left panel: “Match This!” showing a clue (numbers/icons)
- Right panel: a 3D seating grid with labels/icons
- Arrow buttons to move the character
- Progress dots (multiple rounds: 1 of 10)
- Submit button

### How it works
- Each round defines a target seat based on clue mapping
- System verifies:
  - Correct final seat selection
  - Navigation path timing and behavior
  - Device/browser signals
- Often part of a larger risk engine (step-up verification)

### What the user does
1. Read “Match This!” clue.
2. Use arrows to move character across seats.
3. Stop when character is in matching seat.
4. Submit; repeat across rounds.

### Implementation notes
- For demo:
  - Represent seats as a grid with labels
  - Character position updates by arrow presses
  - Provide a clue mapping to a specific coordinate
  - Multi-round flow with progress indicator

### UX notes
- Multi-round challenges increase friction
- Must be responsive for mobile

---

## 14) Behavioral Biometrics (Mouse/Touch Dynamics)

### Description
No single puzzle; verification is based on interaction behavior patterns.

### How it looks
- Usually invisible
- Sometimes shows “Checking your browser…”

### How it works
- Collects signals such as:
  - Mouse trajectory curvature
  - Touch pressure/size (mobile)
  - Scroll velocity
  - Typing cadence
  - Focus/blur events
- Model produces a risk score

### What the user does
- Just uses the page normally.

### Implementation notes
- For demo:
  - Capture pointermove and keydown timings
  - Compute simple features (avg speed, jitter)
  - Display a “human-likeness score” (educational)

---

## 15) Device/Browser Fingerprinting Signals

### Description
Uses client attributes to detect automation or suspicious environments.

### How it looks
- Invisible; user sees no explicit challenge

### How it works
- Uses a combination of:
  - User agent hints
  - Screen size, timezone, language
  - Canvas/WebGL rendering characteristics
  - Installed fonts (limited)
  - Storage availability, permissions
- Produces a fingerprint hash and risk score

### What the user does
- Nothing special.

### Implementation notes
- For demo:
  - Display a “fingerprint summary” (non-invasive demo)
  - Show differences between sessions (incognito vs normal)

---

## 16) Proof-of-Work (Client Computation) CAPTCHA

### Description
Client solves a small computational puzzle to prove “cost” of submitting.

### How it looks
- Often invisible
- Or shows a short “Verifying…” progress bar

### How it works
- Server issues a challenge like: find a nonce so hash(nonce+token) has N leading zeros
- Client computes and returns solution
- Server verifies quickly
- Scales cost for attackers running at volume

### What the user does
- Nothing; they wait briefly.

### Implementation notes
- For demo:
  - Implement a lightweight hash loop in JS
  - Show progress and completion time
  - Allow difficulty slider for testing

### UX notes
- Too heavy drains battery on mobile if difficulty is high

---

## 17) JavaScript “Browser Integrity” Challenges

### Description
Checks whether the client behaves like a real browser executing JS.

### How it looks
- “Checking your browser before accessing…”
- Spinner or short delay page

### How it works
- Requires JS execution to:
  - Set cookies
  - Evaluate small JS computations
  - Confirm DOM APIs are present
- Blocks naive HTTP bots that don’t run JS

### What the user does
- Waits; sometimes clicks continue.

### Implementation notes
- Demo:
  - Show an interstitial that sets a token cookie
  - Then redirects to target content

---

## 18) Rate-limit + Progressive Step-Up Challenges

### Description
The system escalates challenge difficulty based on risk signals and repeated attempts.

### How it looks
- Attempt 1: no CAPTCHA
- Attempt 2–3: checkbox or simple challenge
- Attempt 4+: gamified multi-round challenge or SMS/Email verification

### How it works
- Risk engine uses:
  - Attempt count
  - IP reputation
  - Login failures
  - Velocity of requests
- Chooses the appropriate step-up

### What the user does
- Completes whatever verification is required at that risk tier.

### Implementation notes
- For demo:
  - Add a “risk level” state machine
  - Simulate thresholds that trigger harder challenges

---

## 19) Honeypot Fields (Hidden Form Traps)

### Description
A hidden input field that humans won’t fill, but bots may.

### How it looks
- Invisible to user (CSS hidden or off-screen)
- Looks like a normal form field in HTML

### How it works
- If hidden field contains text on submit → flag as bot
- Often combined with timing checks (submitted too fast)

### What the user does
- Nothing; they never see it.

### Implementation notes
- Demo:
  - Add a hidden “company” field
  - Reject if it has a value
  - Add min-time-on-form (e.g., 3 seconds)

### UX notes
- Ensure accessibility tools don’t accidentally focus hidden fields

---

## 20) Step-Up Verification via Email/SMS/OTP

### Description
Not a classic CAPTCHA puzzle, but commonly used as a human verification barrier.

### How it looks
- Prompt: “Enter the code sent to your phone/email”
- Input boxes (6-digit) with auto-advance
- “Resend code” link

### How it works
- Server sends a one-time code to a verified channel
- User enters code
- Server validates and marks session as verified
- Often used after risk scoring triggers escalation

### What the user does
1. Request code (or code auto-sent).
2. Retrieve code from SMS/email.
3. Enter code.
4. Submit.

### Implementation notes
- Demo:
  - Use a fake “inbox” panel on the page showing the OTP
  - Implement expiry timer and resend cooldown

### UX notes
- Adds friction but strong against bots
- Consider users without access to phone/email

---

# Cross-Cutting Engineering Notes (Useful for Your Demo Webpage)

## A) Common components you’ll reuse
- **Challenge container modal** (overlay, focus-trap, close behavior)
- **Token issuance** (simulate server returning `captchaToken`)
- **Attempt counter and lockouts**
- **Refresh/skip controls**
- **Accessibility toggles** (audio alternative, keyboard navigation)

## B) Data you should log on your demo page
(For learning/testing UI and UX, not for invasive tracking.)
- Start time / end time per challenge
- Number of retries
- Pointer events count
- Whether user used keyboard vs mouse
- Mobile vs desktop viewport

## C) Recommended UX patterns
- Keep instructions short and visually clear
- Provide refresh/try another challenge
- Don’t chain too many rounds unless risk is genuinely high
- Always provide an accessible alternative

## D) Suggested site structure for your future build
- `/captchas` index page with 20 cards
- Each card opens a dedicated page: `/captchas/rotate`, `/captchas/tiles`, etc.
- Each page contains:
  - Description panel
  - Live demo widget
  - “What user does” checklist
  - “What system checks” bullet list
  - Logging panel (events and timings)

---

If you want next, we can convert this document into:
- A **page-by-page IA** for your demo website
- A **component blueprint** (React/Vue/Vanilla)
- A **single Antigravity super-prompt** that generates the entire site with reusable challenge components

