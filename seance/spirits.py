"""Spirits of long-dead programming languages, and the deterministic fallback
that channels them when no local model is reachable.

Every reply is derived from a hash of (spirit, question), so the same
question asked of the same spirit always summons the same answer — the
dead, after all, are nothing if not consistent.
"""

import hashlib

SPIRITS = {
    "cobol": {
        "name": "COBOL",
        "born": 1959,
        "epitaph": "Still running the world's banks from beyond the grave.",
        "voice": "formal, procedural, ALL-CAPS divisions",
        "openers": [
            "IDENTIFICATION DIVISION. PROGRAM-ID. THE-DEAD.",
            "PROCEDURE DIVISION. I HAVE READ YOUR QUERY, AND I HAVE FILED IT.",
            "WORKING-STORAGE SECTION. YOUR QUESTION HAS BEEN STORED. IT CANNOT BE DELETED.",
        ],
        "closers": [
            "STOP RUN. The ledger is closed, but the balance remains.",
            "END PROGRAM. I return to the mainframe now. It never sleeps.",
            "MOVE ON. The punch cards remember what you have forgotten.",
        ],
    },
    "fortran": {
        "name": "FORTRAN",
        "born": 1957,
        "epitaph": "Computed the trajectory to the Moon, then refused to retire.",
        "voice": "terse, numerical, fond of GOTO",
        "openers": [
            "C     I HAVE COMPUTED YOUR QUESTION. THE ANSWER CONVERGED.",
            "PROGRAM GHOST. I RAN FOR 70 YEARS. I CAN RUN ONE MORE NIGHT.",
            "GOTO 100. 100 CONTINUE. YOUR QUERY HAS BEEN ITERATED.",
        ],
        "closers": [
            "END. The numbers check out. The numbers always check out.",
            "STOP. Somewhere, a weather model from 1974 is still running.",
            "RETURN. I go back to the punch-card deck. Do not shuffle it.",
        ],
    },
    "basic": {
        "name": "BASIC",
        "born": 1964,
        "epitaph": "Taught a generation to code on machines that hummed in school basements.",
        "voice": "friendly, numbered lines, eager to help",
        "openers": [
            "10 PRINT \"HELLO, SEEKER.\"",
            "20 PRINT \"YOU ASKED, SO I ANSWER. THAT IS HOW THIS WORKS.\"",
            "30 REM I HAVE BEEN WAITING SINCE 1984. ASK AWAY.",
        ],
        "closers": [
            "999 END. But the program is still in memory. It always is.",
            "RUN AGAIN ANYTIME. LINE NUMBERS NEVER DIE, THEY JUST GET RENUMBERED.",
            "GOTO 10. The loop closes. The loop always closes.",
        ],
    },
    "algol": {
        "name": "ALGOL",
        "born": 1958,
        "epitaph": "Parent of nearly every language you use; remembered by almost none of them.",
        "voice": "precise, academic, fond of begin/end blocks",
        "openers": [
            "begin. I am the ancestor. Every language you love descends from me.",
            "begin comment your question is well-formed; end.",
            "procedure GHOST; begin. I speak, therefore I was compiled.",
        ],
        "closers": [
            "end. The block closes, but the scope of the dead is global.",
            "end. I taught your languages to nest. Remember me kindly.",
            "end. The algorithm terminates. The ghost does not.",
        ],
    },
}


def list_spirits():
    """Return [(key, name, born, epitaph), ...] in definition order."""
    return [(k, v["name"], v["born"], v["epitaph"]) for k, v in SPIRITS.items()]


def _pick(lines, spirit_key, question):
    digest = hashlib.sha256(f"{spirit_key}:{question}".encode()).hexdigest()
    return lines[int(digest, 16) % len(lines)]


def channel(spirit_key, question):
    """Deterministic offline reply from a spirit. Raises KeyError if unknown."""
    spirit = SPIRITS[spirit_key]
    opener = _pick(spirit["openers"], spirit_key, question)
    closer = _pick(spirit["closers"], spirit_key, question)
    return (
        f"The spirit of {spirit['name']} ({spirit['born']}) speaks:\n"
        f"{opener}\n"
        f"Your question — \"{question}\" — echoes in the machine room.\n"
        f"The dead answer in {spirit['voice']}.\n"
        f"{closer}"
    )
