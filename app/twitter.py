import subprocess
import os
import glob
from app.whisper_local import transcribe_audio


def get_twitter_transcript(url: str) -> str | None:
    os.makedirs("/tmp/downloads", exist_ok=True)

    # Download video with yt-dlp
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--format", "bestaudio/best",
                "--extract-audio",
                "--audio-format", "mp3",
                "--output", "/tmp/downloads/twitter_%(id)s.%(ext)s",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            return None
    except Exception:
        return None

    # Find downloaded audio file
    audio_files = glob.glob("/tmp/downloads/twitter_*.mp3")
    if not audio_files:
        return None

    audio_path = sorted(audio_files)[-1]  # most recent
    transcript = transcribe_audio(audio_path)

    # Cleanup
    try:
        os.remove(audio_path)
    except Exception:
        pass

    return transcript
