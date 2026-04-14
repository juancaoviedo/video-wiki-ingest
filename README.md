# video-wiki-ingest

Extract insights from YouTube and Twitter/X videos and save them to a personal wiki.

## How it works

```
URL + category → fetch transcript → extract insights → save to wiki
```

1. **YouTube**: fetches auto-generated subtitles via `youtube-transcript-api` (no audio download needed). Falls back to `yt-dlp` subtitles.
2. **Twitter/X**: downloads audio with `yt-dlp`, transcribes with local Whisper.
3. Insights are extracted by category (startup, finance, parenting, etc.) and saved as structured wiki pages.

## API

### `POST /transcribe`

```json
{
  "url": "https://youtube.com/watch?v=...",
  "category": "startup"
}
```

Response:
```json
{
  "transcript": "...",
  "source": "youtube",
  "url": "...",
  "category": "startup"
}
```

### `GET /health`

Returns `{"status": "ok"}`.

## Running locally

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `WHISPER_MODEL` | `base` | Whisper model size (`tiny`, `base`, `small`, `medium`, `large`) |

## Categories

- `startup` — business, founder lessons, growth
- `finance` — investing, wealth building
- `parenting` — child development, communication
- `general` — any video

## Project structure

```
video-wiki-ingest/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app/
│   ├── main.py           # FastAPI server
│   ├── youtube.py        # YouTube transcript extraction
│   ├── twitter.py        # Twitter/X video download + transcription
│   └── whisper_local.py  # Local Whisper wrapper
└── prompts/
    └── extract.py        # Per-category insight extraction prompts
```
