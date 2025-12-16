# Wordle Backend & Frontend Setup

This repository contains the FastAPI back-end for a Wordle-style game and a front-end kept as a Git submodule (`wordle-frontend`). Follow the steps below to set up both pieces locally.

## Repository layout

- `wordle.py` — FastAPI server that hosts the game API.
- `wordle-frontend/` — front-end application stored as a Git submodule at [`andriydar2/wordle-frontend`](https://github.com/andriydar2/wordle-frontend).

## Cloning with the front-end submodule

1. Clone the repository:

   ```bash
   git clone <this-repo-url>
   cd wordle
   ```

2. Pull the front-end submodule (recommended):

   ```bash
   git submodule update --init --recursive
   ```

   If submodule cloning is blocked in your environment, you can also manually clone the front-end repo into `wordle-frontend/`:

   ```bash
   git clone https://github.com/andriydar2/wordle-frontend wordle-frontend
   ```

## Back-end setup (FastAPI)

### Prerequisites

- Python 3.11+ (earlier versions may work but are untested).
- `pip`.

### Install dependencies

It is recommended to use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi "uvicorn[standard]" nltk
```

### Download NLTK data (once)

The server pulls word lists from NLTK. On the first run, `wordle.py` calls `nltk.download()` to fetch the `words` and `brown` corpora; ensure the machine has internet access the first time you start the API.

To download ahead of time (avoids download on startup):

```bash
python - <<'PY'
import nltk
nltk.download('words')
nltk.download('brown')
PY
```

### Run the server

Start the FastAPI app with Uvicorn:

```bash
uvicorn wordle:app --host 0.0.0.0 --port 8000
```

Key endpoints:

- `POST /start` → returns a `game_id` to track a session.
- `POST /guess` with JSON `{ "game_id": "...", "guess": "apple" }` → returns color-coded feedback, guess count, and whether the answer is correct.

CORS: The server currently allows requests from `https://dar.southcentralus.cloudapp.azure.com`. To use a different front-end origin (e.g., `http://localhost:3000`), user the environment variable CORS_ORIGINS.
## Front-end setup (submodule)

1. Ensure the submodule is present (see cloning instructions above).
2. Install Node.js and the package manager used by the front-end (check for `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`).
3. Install dependencies and start the dev server from within the submodule directory. Typical commands with npm:

   ```bash
   cd wordle-frontend
   npm install
   npm start                            
   ```

   Check the front-end repository's README or `package.json` scripts for the exact start command.

4. Configure the front-end to point at the API. Consult the front-end README for the precise variable name.

## Running the full stack locally

1. Start the FastAPI server on port 8000 (see above).
2. Start the front-end dev server (commonly port 3000) from `wordle-frontend/`.
3. Ensure the back-end CORS settings include the front-end origin you use locally.

You should now be able to play the game from the front-end while it communicates with the FastAPI back-end.

# Running Instance

There is a currently running instance at https://dar.southcentralus.cloudapp.azure.com/ if you want to try it for yourself.

And here is an image of what the game looks like:
<p align="center">
   <img width="572" height="832" alt="wordle_app" src="https://github.com/user-attachments/assets/5875e562-ba3e-4225-9c74-538623dc08cc" />
</p>   
