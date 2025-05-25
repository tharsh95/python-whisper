from time import clock_getres
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.transcription import transcribe_audio
from app.mcq_generator import generate_mcqs
import shutil
import os

app = FastAPI()

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        transcript = transcribe_audio(temp_path)

        os.remove(temp_path)
        return {"transcript": transcript}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-mcq")
async def generate_mcq(data: dict):
    try:
        segment_text = data.get("transcript")
        if not segment_text:
            raise ValueError("Missing transcript in request body")

        questions = await generate_mcqs(segment_text)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
