# English Phrase Trainer

A C2-level business English drill built from real lesson notes.
**155 phrases across 11 lessons**, covering negotiation, meetings, networking,
financial and legal English, plus the idioms and register traps that actually
separate C2 from C1.

Runs entirely in the browser. No accounts, no backend, no tracking — progress is
stored on your own device.

## Use it

**→ https://USERNAME.github.io/english-trainer/**

On iPhone: open that link in **Safari**, then **Share → Add to Home Screen**. It
then launches full-screen and works offline.

> Replace `USERNAME` above with your GitHub username once Pages is enabled.

## Two modes

**Learning** — phrases in random order, each with the Czech meaning, a register
badge (casual / neutral / client-safe / formal / idiom / slang), an example in
context, and a usage tip. Where the original note contained a mistake, the card
shows the correction explicitly.

**Testing** — a situation in Czech only. Say it in English out loud, reveal the
target phrase and its acceptable variants, then grade yourself
*Got it / Nearly / Missed*.

Pick a theme (19 available) and an order before starting.

## Spaced repetition

Leitner boxes with intervals of **1 / 3 / 7 / 21 / 60 days**.

| Grade | Effect |
|---|---|
| Got it | promoted a box; next review further out |
| Nearly | due again tomorrow |
| Missed | back to box 1, and resurfaces later in the same session |

Order modes: **Smart** (due first, then a mild recency bias), Random,
Newest first, Oldest first. Recency only *weights* the draw — every phrase always
stays reachable.

The home screen tracks reviews over the **last 7 and 30 days**, first-time
phrases, active days, a 14-day sparkline and your current streak.

## Multiple users

Everyone opens the same URL and gets the same phrases. Progress lives in each
browser's `localStorage`, so **every person and device keeps its own independent
history** — nothing is shared or synced, and no account is needed.

Progress is tied to the origin, so always launch from the same place (the
home-screen icon once installed). Tap **back up** in the footer to copy a small
JSON blob of your progress; paste it back to restore.

## Layout

```
src/index.html    the app — UI, drill logic, SRS, styles
src/content.js    the phrase repository (edit this to add lessons)
build.py          inlines content into a single deployable file
docs/index.html   GENERATED — this is what GitHub Pages serves
```

Never edit `docs/index.html` by hand; it is overwritten on every build.

## Making changes

```bash
python3 build.py
git add -A && git commit -m "Update phrases" && git push
```

The live site updates about a minute after the push. The build refuses to
publish if the content is empty or would produce a broken bundle.

## Adding lessons

Source notes are handwritten OneNote pages exported to PDF. Typed portions
extract with `pdftotext -layout`; handwritten ink is vector strokes that no OCR
can read, so those pages have to be transcribed by eye.

Lesson dates come from the **OneNote header stamp on page 1**, not the filename —
filename numbering is not chronological.

When a phrase already exists, don't duplicate it: add the lesson id to its
`lessons[]` and set `date` to the newer lesson. Later lessons revisit topics to go
deeper, so the newer wording wins.

**Phrase `id`s are permanent.** Spaced-repetition progress is keyed to them, so
adding lessons or fixing wording never resets anyone's history. Changing an `id`
orphans that phrase's progress.

## Notes on the content

Everything is corrected to present-day American business English. Some
corrections worth knowing:

| Original | Corrected | Why |
|---|---|---|
| "I'm sure I was good" | "All good things, I hope." | the idiomatic fixed reply |
| "let's talk **shortly**" | "let's talk **briefly**" | *shortly* = soon, not briefly |
| "cut this conversation **off**" | "cut this conversation **short**" | *cut off* = interrupt (rude) |
| "Since we're speaking" | "While I have you" | not idiomatic |
| "How **do you find** the event?" | "How **are you finding** it?" | continuous for an ongoing experience |
| "The deal is shady." | "The deal structure appears opaque…" | professional register |

## Why a single file

The app is built as one self-contained HTML file with no external requests, so it
works offline once installed and can be opened from anywhere.

Note that iOS will **not** run JavaScript in a local `.html` opened from Files,
Mail or AirDrop — those use Quick Look, which renders the page but executes no
script, producing a page that looks fine and does nothing. Serving it over
`https://` is what makes it work, which is why this is hosted rather than shared
as a file.
