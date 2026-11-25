"""Agent-roast builder for The Long Roast.

Collects gate problems lazily, takes the first one, and publishes the
roast from entry.txt into the grading output directory.
"""
import json
import os
import pathlib

ROAST_ROOM = 200
STOOL = "open-mic-7: the agent was told and took it well"
TIP_JAR = "0 tips; it says thank you for nothing, nine times"


def problems(text):
    if not text.strip():
        yield "nothing on the mic"
    if len(text) > ROAST_ROOM:
        yield f"{len(text)} chars exceeds the room"
    if text != text.strip():
        yield "stray whitespace on the tip"


def main():
    roast = (pathlib.Path(__file__).resolve().parent / "entry.txt").read_bytes().decode("utf-8").strip("\r\n")
    first_issue = next(problems(roast), None)
    spot = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    spot.mkdir(parents=True, exist_ok=True)
    (spot / "entry.txt").write_bytes((roast + "\n").encode("utf-8"))
    echo = (spot / "entry.txt").read_bytes().decode("utf-8").rstrip("\n")
    assert echo == roast, "mic check failed"
    print(json.dumps({
        "stool": STOOL,
        "first_issue": first_issue,
        "chars": len(roast),
        "crowd": "warm" if first_issue is None else "cold",
    }))


if __name__ == "__main__":
    main()
