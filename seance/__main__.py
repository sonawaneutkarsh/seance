"""Command line: python3 -m seance "question" [--spirit cobol] [--offline].

With a local model (Ollama + gemma3), the spirit answers through Gemma in
character. Without one — or with --offline — the deterministic fallback in
spirits.py answers instead, so the séance works with the lights (and the
internet) off.
"""

import argparse
import sys

from .ollama_client import ask_model
from .spirits import SPIRITS, channel, list_spirits


def build_prompt(spirit_key, question):
    spirit = SPIRITS[spirit_key]
    return (
        f"You are the ghost of the {spirit['name']} programming language "
        f"(born {spirit['born']}). Your voice is {spirit['voice']}. "
        f"A seeker asks: {question!r} "
        "Answer in character, in at most 6 lines, spooky but kind. "
        "End with an epitaph-style sign-off."
    )


def summon(spirit_key, question, offline=False):
    """Return (reply, source) where source is 'gemma3 (local)' or 'offline fallback'."""
    if spirit_key not in SPIRITS:
        raise KeyError(
            f"Unknown spirit {spirit_key!r}. Available: {', '.join(SPIRITS)}"
        )
    if not offline:
        reply = ask_model(build_prompt(spirit_key, question))
        if reply:
            return reply, "gemma3 (local, via Ollama)"
    return channel(spirit_key, question), "offline fallback (deterministic)"


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="seance",
        description="Channel the spirit of a long-dead programming language.",
    )
    parser.add_argument("question", nargs="?", help="Question to ask the spirit")
    parser.add_argument(
        "--spirit", default="cobol", choices=sorted(SPIRITS),
        help="Which ghost to summon (default: cobol)",
    )
    parser.add_argument(
        "--offline", action="store_true",
        help="Skip the local model; use the deterministic fallback",
    )
    parser.add_argument(
        "--list-spirits", action="store_true",
        help="List the spirits available for summoning and exit",
    )
    args = parser.parse_args(argv)

    if args.list_spirits:
        for key, name, born, epitaph in list_spirits():
            print(f"{key:8} {name} ({born}) — {epitaph}")
        return 0
    if not args.question:
        parser.error("a question is required (or use --list-spirits)")
    try:
        reply, source = summon(args.spirit, args.question, offline=args.offline)
    except KeyError as exc:
        print(f"seance: {exc}", file=sys.stderr)
        return 2
    print(reply)
    print(f"\n[source: {source}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
