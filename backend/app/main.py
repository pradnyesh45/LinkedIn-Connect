from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from . import linkedin_scraper, message_generator
from .config import settings

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LinkedInCredentials(BaseModel):
    username: str
    password: str
    target_profile_url: str

@app.post("/api/generate-message")
async def generate_message(credentials: LinkedInCredentials):
    try:
        # Scrape LinkedIn posts and profile info
        scrape_result = await linkedin_scraper.get_profile_data(
            credentials.username,
            credentials.password,
            credentials.target_profile_url
        )
        
        # Generate personalized message using Gemini
        message = await message_generator.create_message(
            scrape_result["posts"],
            scrape_result.get("profile_info")
        )
        
        return {
            "posts": scrape_result["posts"],
            "profile_info": scrape_result.get("profile_info"),
            "message": message,
            "parameters_used": message_generator.get_parameters_used()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
