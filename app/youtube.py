import re
import subprocess
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled


def extract_video_id(url: str) -> str | None:
    patterns = [
        r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_youtube_transcript(url: str) -> str | None:
    video_id = extract_video_id(url)
    if not video_id:
        return None

    # Try youtube-transcript-api first (no audio download needed)
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(chunk["text"] for chunk in transcript_list)
    except (NoTranscriptFound, TranscriptsDisabled):
        pass
    except Exception:
        pass

    # Fallback: yt-dlp subtitles
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--skip-download",
                "--write-auto-sub",
                "--sub-format", "vtt",
                "--sub-lang", "en",
                "--output", "/tmp/downloads/%(id)s.%(ext)s",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        # Parse VTT file
        import glob
        vtt_files = glob.glob(f"/tmp/downloads/{video_id}*.vtt")
        if vtt_files:
            raw = open(vtt_files[0]).read()
            lines = [l for l in raw.splitlines() if l and not l.startswith("WEBVTT") and "-->" not in l and not l.strip().isdigit()]
            return " ".join(lines)
    except Exception:
        pass

    return None
