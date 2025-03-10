import os
import jwt
import httpx
import requests
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2AuthorizationCodeBearer
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

app = FastAPI(title="User Authentication Service")

# Load Google OAuth Config
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token"
)

class TokenRequest(BaseModel):
    code: str
    redirect_uri: str

@app.post("/token")
def exchange_token(request: TokenRequest):
    """ Exchanges authorization code for access token """
    data = {
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "code": request.code,
        "redirect_uri": request.redirect_uri,
        "grant_type": "authorization_code"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post("https://oauth2.googleapis.com/token", data=data, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Token exchange failed")

    return response.json()

@app.get("/auth/login")
def login():
    """Redirects user to Google OAuth login page."""
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/auth"
        f"?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
    )
    return {"auth_url": google_auth_url}


@app.get("/auth/callback")
async def auth_callback(code: str):
    """Handles Google OAuth callback and exchanges code for tokens."""
    token_url = "https://oauth2.googleapis.com/token"
    
    # Exchange authorization code for access token
    async with httpx.AsyncClient() as client:
        response = await client.post(
            token_url,
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch access token")
    
    tokens = response.json()
    access_token = tokens["access_token"]
    
    # Fetch user info from Google
    async with httpx.AsyncClient() as client:
        user_info = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    if user_info.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")
    
    user_data = user_info.json()
    user_id = user_data["id"]
    email = user_data["email"]

    # Generate JWT token
    jwt_payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=12),
    }
    jwt_token = jwt.encode(jwt_payload, SECRET_KEY, algorithm="HS256")

    return {"access_token": jwt_token, "token_type": "bearer", "user": user_data}
