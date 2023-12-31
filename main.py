# main.py
import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from core.config import settings, logger
from genFeaturesFromEpic import generate_features
import re
from dotenv import load_dotenv

#logger = logging.getLogger(__name__)

app = FastAPI()
# Create a logger object before initializing FastAPI
# Load and apply the logging configuration

# Configure logging at app startup based on the desired environment
@app.on_event("startup")
async def startup_event():
    # Load the .env file 
    try:
        load_dotenv()
        logger.info("Starting the application")
    except Exception as e:
        print(f"Exception during app startup: {e}")
        raise    


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MIRO_ACCESS_TOKEN = os.getenv("MIRO_ACCESS_TOKEN")
MIRO_API_BASE_URL = "https://api.miro.com/v2"


headers = {
    "Authorization": f"Bearer {MIRO_ACCESS_TOKEN}",
    "Content-Type": "application/json",
}



def remove_html_tags(text):
    """
    Remove HTML tags from the given text.

    Parameters:
        text (str): The text containing HTML tags.

    Returns:
        str: The text with HTML tags removed.
    """
    clean = re.compile("<[^>]*>")
    return re.sub(clean, "", text)

@app.get("/")
def hello_api():
    """
    A function that represents the handler for the root endpoint ("/") of the API.

    Returns:
        dict: A dictionary containing the message "Hello, This is IBC MIRO REST API Test Service 🚀".
    """
    return {"msg": "Hello, This is IBC MIRO REST API Test Service 🚀"}


def get_item_info(board_id, item_id):
    """
    Retrieves information about a specific item in a board.

    Args:
        board_id (str): The ID of the board containing the item.
        item_id (str): The ID of the item to retrieve information for.

    Returns:
        dict or None: The JSON response containing the item information if the request is successful,
        None otherwise.
    """
    response = requests.get(
        f"{MIRO_API_BASE_URL}/boards/{board_id}/items/{item_id}", headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get frame info. Reason: {response.content.decode('utf-8')}.")
        return None


def get_frame_info(board_id, frame_id):
    """
    Retrieves information about a specific frame on a Miro board.

    Args:
        board_id (str): The ID of the Miro board.
        frame_id (str): The ID of the frame on the Miro board.

    Returns:
        dict: The JSON response containing the information about the frame.

    Raises:
        HTTPException: If the request to fetch the Miro frame fails.

    """
    response = requests.get(
        f"{MIRO_API_BASE_URL}/boards/{board_id}/frames/{frame_id}", headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        error_reason = (
            response.json().get("message")
            if response.json().get("message")
            else "Failed to fetch Miro Frame"
        )
        raise HTTPException(status_code=response.status_code, detail=error_reason)


def get_miro_frames(board_id):
    """
    Retrieves the frames from the Miro API for a given board ID.

    Parameters:
        board_id (str): The ID of the Miro board.

    Returns:
        dict: A dictionary containing the frames retrieved from the Miro API.

    Raises:
        HTTPException: If the request to the Miro API fails or returns a non-200 status code.
    """

    url = f"{MIRO_API_BASE_URL}/boards/{board_id}/frames"
    response = requests.get(url, headers)

    if response.status_code == 200:
        return response.json()
    else:
        error_reason = (
            response.json().get("message")
            if response.json().get("message")
            else "Failed to fetch Miro frames"
        )
        raise HTTPException(status_code=response.status_code, detail=error_reason)


def get_miro_cards(board_id, frame_id):
    """
    Retrieves the cards from a Miro board frame.

    Parameters:
        board_id (str): The ID of the Miro board.
        frame_id (str): The ID of the Miro board frame.

    Returns:
        dict: A dictionary containing the cards retrieved from the Miro board frame.

    Raises:
        HTTPException: If the API call to retrieve the cards fails.

    """
    url = f"{MIRO_API_BASE_URL}/boards/{board_id}/frames/{frame_id}/cards"
    response = requests.get(url, headers)

    if response.status_code == 200:
        return response.json()
    else:
        error_reason = (
            response.json().get("message")
            if response.json().get("message")
            else "Failed to fetch Miro cards"
        )
        raise HTTPException(status_code=response.status_code, detail=error_reason)


@app.get("/miro-frames")
async def display_miro_frames(board_id: str = Query(..., title="Miro Board ID")):
    """
    Retrieves the Miro frames associated with a specific board.

    Parameters:
        board_id (str): The ID of the Miro board.

    Returns:
        List[Frame]: A list of Miro frames.

    Raises:
        HTTPException: If there is an error retrieving the Miro frames.
    """
    try:
        frames = get_miro_frames(board_id)
        return frames
    except HTTPException as e:
        logger.error("An error occurred while retrieving Miro frames: %s", e)
        raise e


@app.get("/miro-cards")
async def display_miro_cards(
    board_id: str = Query(..., title="Miro Board ID"),
    frame_id: str = Query(..., title="Miro Frame ID"),
):
    """
    Retrieve and display Miro cards from a specific Miro board and frame.

    Parameters:
    - board_id (str): The ID of the Miro board.
    - frame_id (str): The ID of the Miro frame.

    Returns:
    - cards: The Miro cards retrieved from the specified board and frame.

    Raises:
    - HTTPException: If there is an error retrieving the Miro cards.
    """
    try:
        cards = get_miro_cards(board_id, frame_id)
        return cards
    except HTTPException as e:
        logger.error("An error occurred while retrieving Miro Cards: %s", e)
        raise e


@app.get("/generate-features")
async def call_generate_features(epic_description: str):
    """
    Call generate_features method by passing the epic_description and return the generated_features.

    Parameters:
        - epic_description (str): The description of the epic.

    Returns:
        - dict: A dictionary containing the generated features.
          If an error occurs, it returns a dictionary with the error message.
    """
    try:
        # Call generate_features method here by passing the epic_description
        generated_features = generate_features(epic_description)
        return {"generated_features": generated_features}
    except Exception as e:
        return {"error": str(e)}
