from io import BytesIO
import httpx
from starlette.config import Config
from starlette.datastructures import Secret
from starlette.responses import JSONResponse
from fastapi import FastAPI, Request, HTTPException
from os import environ

config = Config(environ=environ)

HOST: str = config("HOST", cast=str, default="0.0.0.0")
PORT: int = config("PORT", cast=int, default=8000)
DEBUG: bool = config("DEBUG", cast=bool, default=False)
OPENAI_API_KEY = Secret = config("OPENAI_API_KEY", cast=Secret)

app = FastAPI(debug=DEBUG)


async def send_request(mode: str, data: bytes) -> dict:
    content = data.split(b"\r\n\r\n")[-1]

    file = ("audio.m4a", BytesIO(content), "audio/m4a")

    print(f"Making request with {data[:500]=}")

    async with httpx.AsyncClient(timeout=3600) as client:
        r = await client.post(
            f"https://api.openai.com/v1/audio/{mode}",
            files={"file": file},
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            data={"model": "whisper-1", "response_format": "verbose_json"},
        )

    print(f"OpenAI response: {r.text[:500]=}")

    return r.json()


@app.get("/")
async def handle_index(request: Request):
    return JSONResponse({"hello": "world"})


@app.post("/{mode}")
async def handle_whisper(request: Request, mode: str):
    if mode not in ["transcriptions", "translations"]:
        raise HTTPException(status_code=400, detail="Invalid mode. Use 'transcriptions' or 'translations'.")
    request_file: bytes = await request.body()
    transcription = await send_request(mode, request_file)
    return JSONResponse(transcription)
