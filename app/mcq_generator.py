import httpx
import json
import re
from typing import List, Dict, Any
import traceback


OLLAMA_API_URL = "http://localhost:11434/api/generate"

async def check_ollama_server() -> bool:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:11434/api/version")
            return response.status_code == 200
    except Exception as e:
        print(f"Ollama server check failed: {str(e)}")
        return False

async def generate_mcqs(segment_text: str) -> List[Dict[str, Any]]:
    if not await check_ollama_server():
        raise Exception("Ollama server is not running. Please start the Ollama server first.")

    if not segment_text.strip():
        raise ValueError("Empty text provided for MCQ generation")

    prompt = f"""
Generate 3 multiple-choice questions (MCQs) from the following passage.
Each question must have exactly 4 options and one correct answer.
Use facts from the passage only.

Passage:
\"\"\"
{segment_text}
\"\"\"

Return the output as a valid JSON array with exactly this format:
[
  {{
    "question": "First question text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Correct Option"
  }},
  {{
    "question": "Second question text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Correct Option"
  }},
  {{
    "question": "Third question text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Correct Option"
  }}
]

Only return the JSON array. Do not include any commentary.
"""

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(OLLAMA_API_URL, json=payload)

            response.raise_for_status()

            output = response.json().get("response", "").strip()
            if not output:
                raise ValueError("Empty response from Ollama API")

            try:
                # Attempt direct JSON load
                mcqs = json.loads(output)
            except json.JSONDecodeError:
                # Fallback: extract first JSON array in string
                match = re.search(r"\[\s*{.*?}\s*(,\s*{.*?}\s*){2}\s*\]", output, re.DOTALL)
                if not match:
                    raise ValueError("Could not extract valid JSON array from model output.")
                mcqs = json.loads(match.group())

            # Structural validation
            if not isinstance(mcqs, list) or len(mcqs) != 3:
                raise ValueError("Expected a list of 3 MCQs")
            return mcqs

    except httpx.HTTPStatusError as e:
        raise Exception(f"HTTP status error {e.response.status_code}: {e.response.text}")
    except httpx.HTTPError as e:
        print("Full traceback:")
        traceback.print_exc()
        raise Exception(f"HTTP error occurred: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse MCQ JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating MCQs: {str(e)}")
