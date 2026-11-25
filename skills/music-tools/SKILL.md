---
name: music-tools
description: Calculate piano chords and inversions, scales, standard guitar and bass fret positions, vetted open guitar shapes, and generate original MIDI practice exercises for Practice Room learners.
---
# Music tools
Use this skill for music reference questions and original practice tracks. Follow explicit constraints; confirm instrument/tuning only when it materially affects correctness. Defaults: standard 6-string guitar E2 A2 D3 G3 B3 E4 and standard 4-string bass E1 A1 D2 G2.

When Python execution is available, run the bundled `scripts/music.py` via Python 3.10+ (no installs or network needed). Resolve path relative to this skill. Examples:
- `python scripts/music.py chord Eb maj7 --inversion 1`
- `python scripts/music.py scale F# minor`
- `python scripts/music.py fretboard bass A minor-pentatonic --frets 7`
- `python scripts/music.py shape Am`
- `python scripts/music.py exercise bass A --kind minor --bpm 75 --bars 8 --difficulty beginner --out practice.mid`
Read the JSON result, present a simple diagram/table, and explain what to play. For guitar tabs label high string at top, frets left to right; returned fretboard/shape arrays are low-to-high, so reverse for tab. Include muted strings and distinguish chord shapes from scale positions. Piano: list exact pitches with octaves and optional fingers; suggest inversions or split hands for comfort. Do not promise a universal fingering.

For exercise generation, pick a major or natural minor key, tempo 40–200, 4–32 bars, beginner quarter-note or intermediate eighth-note practice. The engine writes original chord-tone patterns, harmony backing and click as four named Type 1 MIDI tracks, 480 PPQ, no program/bank messages. Give the file only after confirming creation; also give a short playing guide. Tell users to assign sounds in their DAW and mute the practice track to play along. The MIDI pattern is a drill, not a transcription or full song. For guitars/bass, pitch-to-fret suggestions must be checked against standard tuning or user's tuning; do not imply all pitches are feasible in one position. For other requests use text explanation or ask for specifics.

If execution is unavailable, use `references/music-reference.md` for interval math, shapes and manual verification. Do not imply script or file ran. If requested output exceeds the tool's scope, offer a text-based drill or a supported variant; never invent an attachment.
