#main.py
import os
from fastapi import FastAPI, Query, HTTPException
import requests
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)

MIRO_ACCESS_TOKEN = os.getenv("MIRO_ACCESS_TOKEN")
MIRO_API_BASE_URL = "https://api.miro.com/v2/boards/"
OPENAI_key = os.getenv("OpenAI_Key")

@app.get("/")
def hello_api():
    return {"msg":"Hello, This is IBC MIRO Test API Service 🚀"}

def get_miro_frames(board_id):
    url = f"{MIRO_API_BASE_URL}{board_id}/frames"
    response = requests.get(url, headers={"Authorization": f"Bearer {MIRO_ACCESS_TOKEN}"})

    if response.status_code == 200:
        return response.json()
    else:
        error_reason = response.json().get("message") if response.json().get("message") else "Failed to fetch Miro frames"
        raise HTTPException(status_code=response.status_code, detail=error_reason)

def get_miro_cards(board_id, frame_id):
    url = f"{MIRO_API_BASE_URL}{board_id}/frames/{frame_id}/cards"
    response = requests.get(url, headers={"Authorization": f"Bearer {MIRO_ACCESS_TOKEN}"})

    if response.status_code == 200:
        return response.json()
    else:
        error_reason = response.json().get("message") if response.json().get("message") else "Failed to fetch Miro cards"
        raise HTTPException(status_code=response.status_code, detail=error_reason)

@app.get("/miro-frames")
async def display_miro_frames(board_id: str = Query(..., title="Miro Board ID")):
    try:
        frames = get_miro_frames(board_id)
        return frames
    except HTTPException as e:
        raise e

@app.get("/miro-cards")
async def display_miro_cards(board_id: str = Query(..., title="Miro Board ID"), frame_id: str = Query(..., title="Miro Frame ID")):
    try:
        cards = get_miro_cards(board_id, frame_id)
        return cards
    except HTTPException as e:
        raise e

