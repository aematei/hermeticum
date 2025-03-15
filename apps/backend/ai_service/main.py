import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY environment variable is not set!")

# Initialize OpenAI client if API key is available
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

app = FastAPI(title="AI Service")

class TarotReadingRequest(BaseModel):
    journal_id: str
    deck: str
    spread: str
    cards: List[str]
    user_thoughts: Optional[str] = None

@app.post("/chat")
def get_tarot_guidance(reading: TarotReadingRequest):
    """Processes a tarot reading and generates AI guidance."""
    
    if not OPENAI_API_KEY or client is None:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
    try:
        # Construct prompt
        prompt = f"""
        User's Tarot Reading:
        - Deck: {reading.deck}
        - Spread: {reading.spread}
        - Cards Drawn: {', '.join(reading.cards)}
        - User's Initial Thoughts: "{reading.user_thoughts}"

        Task: 
        Engage the user in a Socratic dialogue to refine their interpretation.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a tarot AI that guides users through reflection."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=250,
            temperature=0.7,
        )
        
        return {"ai_response": response.choices[0].message.content}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    """Simple health check endpoint."""
    return {"status": "AI service is running"}
