import os
import httpx

WHISPER_ASR_URL = os.environ.get("WHISPER_ASR_URL", "http://host.docker.internal:9000")


def transcribe_audio(audio_path: str) -> str | None:
    """Send audio file to Whisper ASR container and return transcript text."""
    try:
        with open(audio_path, "rb") as f:
            with httpx.Client(timeout=300) as client:
                response = client.post(
                    f"{WHISPER_ASR_URL}/asr",
                    files={"audio_file": (os.path.basename(audio_path), f, "audio/mpeg")},
                    params={"task": "transcribe", "language": "en", "output": "txt"},
                )
                response.raise_for_status()
                return response.text.strip()
    except Exception as e:
        print(f"Whisper ASR error: {e}")
        return None
