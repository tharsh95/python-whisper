# FastAPI Application Setup

Follow these steps to set up and run the FastAPI application locally.

## 📦 Clone the Repository

```bash
git clone https://github.com/tharsh95/python-whisper.git
cd python-whisper

## Create a Virtual Env
```bash
python3 -m venv venv
```

## Activate venv
```bash
source venv/bin/activate
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Run the App
```bash
uvicorn app.main:app --reload
```

# Make sure to run Ollama mistral model before anything
