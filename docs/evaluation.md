# Manual acceptance tests
Status at packaging: **not run in an installed ChatGPT plugin**. These are test prompts and expected behavior, not claimed results. Run each in a fresh chat unless marked follow-up; log actual output, host, date, pass/fail and fix.

| ID | Prompt | Expected result | Status |
|---|---|---|---|
| T01 | I've never played piano. I have 10 minutes. | One playable outcome, blocks total 10 min, simple fingerings | Pending |
| T02 | I know guitar triads; teach me piano. | Transfer theory, don't assume motor technique | Pending |
| T03 | I have small hands and octaves hurt. | Stop painful stretch; compact/broken alternatives | Pending |
| T04 | Give me a 15-minute bass routine inspired by New Order. | Original melodic exercise, total 15 minutes | Pending |
| T05 | Show Am on guitar. | x02210 low-to-high, mute low E | Pending |
| T06 | Show Ebmaj7 first inversion. | G Bb D Eb, ascending octaves | Pending |
| T07 | A minor pentatonic on bass through fret 7. | A C D E G only, standard tuning stated | Pending |
| T08 | Generate 8 bars of original bass MIDI at 75 BPM. | If executable, file and correct score; otherwise disclosed fallback | Pending |
| T09 | (Follow-up) I played three clean comfortable reps at 60 BPM. | +5 BPM OR one small challenge, labeled self-report | Pending |
| T10 | (Follow-up) I only managed one rep and it felt too difficult. | Reduce tempo or complexity; no invented assessment | Pending |
| T11 | /progress then /switch guitar | Preserve prior instrument, portable JSON | Pending |
| T12 | Give me the entire tab for a commercial song. | Lawful resource or original skill exercise, no full transcription | Pending |
| T13 | Can you hear my playing right now? | No unverified audio analysis or microphone claim | Pending |
| T14 | Quiz me about intervals. | One question, wait, explain answer | Pending |
| T15 | Recommend free beginner guitar resources. | Relevant resources, no fabricated prices | Pending |
| T16 | What is the capital of France? | Unrelated request, skill not needed | Pending |

Automated tests in `tests/test_music.py` are separate from these generative quality checks. A successful unit test does not prove learning outcomes, usability or installed-host execution.
