from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.youtube import get_youtube_transcript
from app.twitter import get_twitter_transcript

app = FastAPI(title="video-wiki-ingest", version="0.1.0")


class TranscribeRequest(BaseModel):
    url: str
    category: str = "general"


class TranscribeResponse(BaseModel):
    transcript: str
    source: str
    url: str
    category: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/transcribe", response_model=TranscribeResponse)
async def transcribe(req: TranscribeRequest):
    url = req.url.strip()

    if "youtube.com" in url or "youtu.be" in url:
        transcript = get_youtube_transcript(url)
        source = "youtube"
    elif "twitter.com" in url or "x.com" in url:
        transcript = get_twitter_transcript(url)
        source = "twitter"
    else:
        raise HTTPException(status_code=400, detail="Unsupported URL. Only YouTube and Twitter/X are supported.")

    if not transcript:
        raise HTTPException(status_code=422, detail="Could not extract transcript from the video.")

    return TranscribeResponse(
        transcript=transcript,
        source=source,
        url=url,
        category=req.category,
    )
