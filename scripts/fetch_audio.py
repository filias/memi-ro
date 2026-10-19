"""Download the language cards' recordings from Wikimedia Commons.

    uv run python scripts/fetch_audio.py

Fetches each file in ``RECORDINGS`` and converts it with ffmpeg to
``static/audio/<slug>.mp3``: mono MP3 (every browser plays it), silence
trimmed at both ends and loudness evened out. Rewrites static/audio/CREDITS.md
with each recording's speaker and licence, which CC BY-SA requires.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from memi_ro.categories.language import RECORDINGS, phrase_slug  # noqa: E402

AUDIO_DIR = ROOT / "static" / "audio"
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "memi-ro (+https://ro.memi.games)"}

# Trim leading silence, then (reversed) trailing silence; even out loudness;
# leave a short tail so the clip doesn't stop dead.
TRIM = "silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.15"
FILTERS = ",".join([
    TRIM, "areverse", TRIM, "areverse",
    "loudnorm=I=-16:TP=-1.5:LRA=11", "apad=pad_dur=0.15",
])


def file_info(filename):
    resp = requests.get(API, headers=UA, params={
        "action": "query", "format": "json", "prop": "imageinfo",
        "iiprop": "url|extmetadata", "titles": f"File:{filename}",
    })
    page = next(iter(resp.json()["query"]["pages"].values()))
    info = page["imageinfo"][0]
    meta = info["extmetadata"]
    speaker = re.search(r"Speaker: <a[^>]*>([^<]+)</a>", meta["Artist"]["value"])
    return {
        "url": info["url"],
        "page": info["descriptionurl"],
        "license": meta["LicenseShortName"]["value"],
        "speaker": speaker.group(1) if speaker else filename.split("-")[2],
    }


def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    credits = []
    for romanian, filename in RECORDINGS.items():
        info = file_info(filename)
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            tmp.write(requests.get(info["url"], headers=UA).content)
            tmp.flush()
            out = AUDIO_DIR / f"{phrase_slug(romanian)}.mp3"
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", tmp.name,
                 "-af", FILTERS, "-ac", "1", "-b:a", "96k", str(out)],
                check=True,
            )
        print(f"{romanian:16} -> {out.name}")
        credits.append(
            f"- `{out.name}` — {romanian}: {info['speaker']}, "
            f"[{info['license']}]({info['page']})"
        )
    (AUDIO_DIR / "CREDITS.md").write_text(
        "# Recordings\n\n"
        "Native Romanian speakers recorded for [Lingua Libre](https://lingualibre.org),\n"
        "from Wikimedia Commons, converted to MP3 and trimmed.\n\n"
        + "\n".join(credits) + "\n"
    )


if __name__ == "__main__":
    main()
