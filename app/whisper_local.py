import os
import whisper

_model = None


def _get_model():
    global _model
    if _model is None:
        model_name = os.environ.get("WHISPER_MODEL", "base")
        _model = whisper.load_model(model_name)
    return _model


def transcribe_audio(audio_path: str) -> str | None:
    try:
        model = _get_model()
        result = model.transcribe(audio_path)
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Whisper transcription error: {e}")
        return None
