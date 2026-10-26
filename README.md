# seance 👻

Hold a séance with the ghosts of dead programming languages — with a
**local open-weight model** doing the haunting. Built for [DEV's
Hacktoberfest Week 4 challenge](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)
("Ghost in the Machine": build something spooky, or something that honors
the past in the spirit of Día de los Muertos, with open-weight models or
open-source AI).

Ask a question, and the spirit of COBOL, FORTRAN, BASIC, or ALGOL answers
in character. The dead answer best, of course, with the lights off: no
accounts, no API keys, nothing leaves your machine.

## Setup

```bash
# 1. Clone and enter
git clone https://github.com/sonawaneutkarsh/seance.git seance && cd seance

# 2. (Optional) Install Ollama and pull Gemma for AI séances
#    https://ollama.com  →  ollama pull gemma3

# 3. No Python dependencies — stdlib only
python3 -m seance --list-spirits
```

## Usage

```bash
# Meet the spirits
python3 -m seance --list-spirits

# Ask COBOL a question (tries local Gemma first, falls back offline)
python3 -m seance "Will my code outlive me?"

# Ask another spirit, fully offline and deterministic
python3 -m seance "Why did you disappear?" --spirit basic --offline
python3 -m seance "Did you really go to the Moon?" --spirit fortran --offline
```

## How it works

1. **Summon.** You pick a spirit (COBOL, FORTRAN, BASIC, ALGOL) and ask
   a question.
2. **Channel.** The question goes to Gemma via Ollama (`localhost:11434`,
   plain HTTP, stdlib only), prompted to answer in that language's voice.
   Anything the model returns is the reply.
3. **Fallback, honestly.** No model reachable — or `--offline` passed —
   and a deterministic fallback answers instead: lines picked by hashing
   (spirit, question), so the same question always summons the same
   answer. The dead are nothing if not consistent. The reply always says
   which source produced it, so a fallback is never passed off as AI.
4. **No ghosts in the cloud.** Everything runs on your machine, which is
   the whole point: the past you are communing with never leaves your
   laptop, and the séance works with the internet off.

## Tests

```bash
python3 -m unittest discover -s tests -v
# 9 tests, all passing. Ollama is mocked — no model or network needed.
```
