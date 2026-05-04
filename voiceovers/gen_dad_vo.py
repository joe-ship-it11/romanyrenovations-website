"""
Generate Romany Renovations voiceover variants using ElevenLabs.

Dad's cloned voice (Hany Romany) — voice_id: TJ4BrlMWAs3F9E3rLcu8
Style: elevated, controlled, premium Canadian renovation company.
Think Restoration Hardware brand spot, not Home Depot promo.

Canadian English: centre, colour, honour, programme.
Tone: understated confidence. Let the work speak. No hard-sell.
Pace: ~120-130 wpm, slow with breath pauses on '...'.

Usage:
    python gen_dad_vo.py
    python gen_dad_vo.py --script short
    python gen_dad_vo.py --script medium
    python gen_dad_vo.py --script long
    python gen_dad_vo.py --all
"""

import argparse
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
API_KEY = os.environ.get(
    "ELEVENLABS_API_KEY",
    "sk_966bf573fb1aa70d251140ca1ff87a191523c4c4f878187a",
)
VOICE_ID = "TJ4BrlMWAs3F9E3rLcu8"  # Hany Romany clone
MODEL_ID = "eleven_multilingual_v2"

VOICE_SETTINGS = {
    "stability": 0.75,           # high = locks register, kills sing-song
    "similarity_boost": 0.88,
    "style": 0.12,               # low = no theatrics
    "use_speaker_boost": True,
}

OUT_DIR = Path(__file__).parent  # voiceovers/

# ---------------------------------------------------------------------------
# Scripts — Canadian premium renovation market
# ---------------------------------------------------------------------------
SCRIPTS = {
    # ~15s — IG/TikTok hook
    "short": {
        "filename": "hany_vo_short_15s.mp3",
        "text": (
            "Every home has a story... "
            "We're here to write the next chapter. "
            "Romany Renovations... "
            "Serving the Greater Toronto Area."
        ),
    },

    # ~30s — workhorse spot (website, ads, reels)
    "medium": {
        "filename": "hany_vo_medium_30s.mp3",
        "text": (
            "For over two decades... we've been transforming homes "
            "across the Greater Toronto Area. "
            "Custom millwork... kitchen renovations... basement finishing... "
            "each project built with the care it deserves. "
            "We don't cut corners. We craft them. "
            "Your vision... our artistry. "
            "Romany Renovations."
        ),
    },

    # ~60s — website hero / brand reel
    "long": {
        "filename": "hany_vo_long_60s.mp3",
        "text": (
            "A well-built home isn't just about materials... "
            "it's about understanding what a space means to the people who live in it. "
            "That's what we do at Romany Renovations. "
            "From custom millwork and cabinetry... "
            "to full kitchen transformations and basement finishing... "
            "every detail is considered. Every joint is true. "
            "We've spent over twenty years earning the trust "
            "of families across the Greater Toronto Area... "
            "not through advertising... but through the quality of our work. "
            "Because in this trade... your reputation is built one home at a time. "
            "If you're thinking about your next renovation... "
            "we'd be honoured to be part of it. "
            "Your vision... our artistry. "
            "Romany Renovations."
        ),
    },
}


# ---------------------------------------------------------------------------
# Generate
# ---------------------------------------------------------------------------
def generate(script_key: str) -> Path:
    from elevenlabs.client import ElevenLabs

    if script_key not in SCRIPTS:
        print(f"Unknown script: {script_key}. Options: {list(SCRIPTS.keys())}")
        sys.exit(1)

    entry = SCRIPTS[script_key]
    text = entry["text"]
    out_path = OUT_DIR / entry["filename"]

    print(f"Generating '{script_key}' ({len(text)} chars)...")
    print(f"  Text: {text[:80]}...")

    client = ElevenLabs(api_key=API_KEY)

    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=text,
        model_id=MODEL_ID,
        voice_settings=VOICE_SETTINGS,
    )

    # audio is a generator of bytes chunks
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    size_kb = out_path.stat().st_size / 1024
    print(f"  Saved: {out_path} ({size_kb:.0f} KB)")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Generate Romany Renovations VO")
    parser.add_argument("--script", choices=list(SCRIPTS.keys()), help="Which script to generate")
    parser.add_argument("--all", action="store_true", help="Generate all variants")
    args = parser.parse_args()

    if args.all:
        for key in SCRIPTS:
            generate(key)
    elif args.script:
        generate(args.script)
    else:
        # Default: generate all
        for key in SCRIPTS:
            generate(key)


if __name__ == "__main__":
    main()
