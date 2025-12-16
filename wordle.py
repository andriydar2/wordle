import os
import random
import uuid
from collections import Counter

import nltk
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Only need to run these once, or comment them after the first run
nltk.download('words')
nltk.download('brown')

# Gather all lowercase 5-letter words from nltk.corpus.words
all_five_letter_words = [
    w.lower() for w in nltk.corpus.words.words()
    if len(w) == 5 and w.isalpha() and w.islower()
]
all_five_letter_words = list(set(all_five_letter_words))

# Count frequency in Brown corpus
brown_words = [w.lower() for w in nltk.corpus.brown.words()]
brown_counts = Counter(brown_words)

# Sort by Brown corpus frequency (most frequent first)
all_five_letter_words.sort(key=lambda w: brown_counts[w], reverse=True)

# Build allowed guess list (top 10,000)
GUESSES = all_five_letter_words[:10000] if len(all_five_letter_words) >= 10000 else all_five_letter_words

# Build answer pool (top 2,000 most common words)
ANSWERS = all_five_letter_words[:2000] if len(all_five_letter_words) >= 2000 else all_five_letter_words

app = FastAPI()
games = {}  # Maps game_id to {"answer": ..., "guesses": [...]}

origins = [
    origin.strip()
    for origin in os.environ.get(
        "CORS_ORIGINS", "https://dar.southcentralus.cloudapp.azure.com"
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StartResponse(BaseModel):
    game_id: str

class GuessRequest(BaseModel):
    game_id: str
    guess: str

class GuessResponse(BaseModel):
    feedback: list
    correct: bool
    guesses: int
    max_guesses: int = 6

def get_feedback(guess, answer):
    result = ["gray"] * 5
    answer_chars = list(answer)
    used = [False] * 5
    # Green pass
    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = "green"
            used[i] = True
    # Yellow pass
    for i in range(5):
        if result[i] == "gray":
            for j in range(5):
                if not used[j] and guess[i] == answer[j]:
                    result[i] = "yellow"
                    used[j] = True
                    break
    return result

@app.post("/start", response_model=StartResponse)
def start_game():
    answer = random.choice(ANSWERS)
    game_id = str(uuid.uuid4())
    games[game_id] = {"answer": answer, "guesses": []}
    return StartResponse(game_id=game_id)

@app.post("/guess", response_model=GuessResponse)
def make_guess(req: GuessRequest):
    game = games.get(req.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    guess = req.guess.lower()
    if len(guess) != 5 or guess not in GUESSES:
        raise HTTPException(status_code=400, detail="Invalid guess")
    if len(game["guesses"]) >= 6:
        raise HTTPException(status_code=400, detail="No more guesses")
    feedback = get_feedback(guess, game["answer"])
    game["guesses"].append({"guess": guess, "feedback": feedback})
    correct = guess == game["answer"]
    return GuessResponse(
        feedback=feedback,
        correct=correct,
        guesses=len(game["guesses"])
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)