from fastapi import FastAPI, HTTPException, Request, Response, Depends
import firebase_admin
from firebase_admin import auth, credentials
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
import httpx
import json
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Authentication Service")

# Initialize Firebase Admin SDK
# First try to use credentials from the JSON string environment variable
firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
if firebase_creds_json:
    try:
        # Convert the JSON string to a dictionary
        cred_dict = json.loads(firebase_creds_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized with credentials from environment variable")
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error loading Firebase credentials from environment: {str(e)}")
        # Fall back to file-based approach
        cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print(f"Firebase initialized with credentials from file: {cred_path}")
        except ValueError:
            # App already initialized
            print("Firebase app already initialized")
        except FileNotFoundError:
            print(f"Firebase credentials file not found at {cred_path}")
            # Initialize with default credentials for development
            firebase_admin.initialize_app()
            print("Firebase initialized with default credentials")
else:
    # Fall back to file-based approach if JSON string not provided
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print(f"Firebase initialized with credentials from file: {cred_path}")
    except ValueError:
        # App already initialized
        print("Firebase app already initialized")
    except FileNotFoundError:
        print(f"Firebase credentials file not found at {cred_path}")
        # Initialize with default credentials for development
        firebase_admin.initialize_app()
        print("Firebase initialized with default credentials")

# Models
class TokenResponse(BaseModel):
    id_token: str
    refresh_token: Optional[str] = None
    
class UserCredentials(BaseModel):
    id_token: str
    
class SignInLink(BaseModel):
    sign_in_url: str

# Firebase configuration
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN")
REDIRECT_URL = os.getenv("REDIRECT_URL", "http://localhost:8002/auth/callback")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok"}
# @app.get("/")
# async def root():
#     """Health check endpoint"""
#     return {
#         "status": "Authentication service is running",
#         "firebase_config": {
#             "api_key_configured": bool(FIREBASE_API_KEY),
#             "auth_domain_configured": bool(FIREBASE_AUTH_DOMAIN)
#         }
#     }

@app.get("/login")
async def login():
    """Generate Google sign-in URL"""
    if not FIREBASE_API_KEY:
        raise HTTPException(status_code=500, detail="Firebase API key not configured")
        
    if not FIREBASE_AUTH_DOMAIN:
        raise HTTPException(status_code=500, detail="Firebase Auth domain not configured")
    
    # For Firebase, we typically handle the sign-in flow from the frontend
    # This is a simplified URL that would redirect to Google's sign-in page
    provider_id = "google.com"
    
    # Return information about how to authenticate
    return {
        "message": "In a real application, the Google sign-in would be initiated from the frontend.",
        "firebase_config": {
            "apiKey": FIREBASE_API_KEY,
            "authDomain": FIREBASE_AUTH_DOMAIN,
            "redirectUrl": REDIRECT_URL
        },
        "instructions": "To test the flow, you need to implement a frontend that uses Firebase Authentication SDK."
    }

@app.post("/verify-token")
async def verify_token(user_credentials: UserCredentials):
    """Verify Firebase ID token"""
    try:
        # Verify the ID token using Firebase Admin SDK
        decoded_token = auth.verify_id_token(user_credentials.id_token)
        
        # Get user information
        uid = decoded_token['uid']
        user = auth.get_user(uid)
        
        # Return user information
        return {
            "uid": uid,
            "email": user.email,
            "name": user.display_name,
            "photo_url": user.photo_url,
            "email_verified": user.email_verified,
            "provider_data": [
                {"provider_id": provider.provider_id}
                for provider in user.provider_data
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

@app.get("/auth/callback")
async def auth_callback(code: str = None, state: str = None):
    """Handle OAuth callback"""
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")
    
    if not FIREBASE_API_KEY:
        raise HTTPException(status_code=500, detail="Firebase API key not configured")
    
    try:
        # Exchange code for Firebase token
        # Note: This is a simplified example and may need adjustments based on your exact OAuth setup
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={FIREBASE_API_KEY}",
                json={
                    "postBody": f"code={code}&providerId=google.com",
                    "requestUri": REDIRECT_URL,
                    "returnIdpCredential": True,
                    "returnSecureToken": True
                }
            )
            
            if response.status_code != 200:
                error_msg = "Failed to exchange code for token"
                try:
                    error_data = response.json()
                    error_msg = f"{error_msg}: {error_data.get('error', {}).get('message', 'Unknown error')}"
                except:
                    pass
                raise HTTPException(status_code=response.status_code, detail=error_msg)
                
            token_data = response.json()
            return TokenResponse(
                id_token=token_data["idToken"],
                refresh_token=token_data.get("refreshToken")
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")

@app.post("/logout")
async def logout(response: Response):
    """Logout - Frontend should clear tokens"""
    response.delete_cookie(key="session")
    return {"message": "Logged out successfully. Frontend should discard tokens."}

@app.get("/user/me")
async def get_current_user(request: Request):
    """Get current user from Authorization header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = auth_header.replace("Bearer ", "")
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        user = auth.get_user(uid)
        
        return {
            "uid": uid,
            "email": user.email,
            "name": user.display_name,
            "photo_url": user.photo_url,
            "email_verified": user.email_verified
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

@app.post("/refresh-token")
async def refresh_token(refresh_token: str):
    """Refresh an ID token using a refresh token"""
    if not FIREBASE_API_KEY:
        raise HTTPException(status_code=500, detail="Firebase API key not configured")
        
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_API_KEY}",
                json={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to refresh token")
                
            token_data = response.json()
            return {
                "id_token": token_data["id_token"],
                "refresh_token": token_data["refresh_token"],
                "expires_in": token_data["expires_in"]
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token refresh error: {str(e)}")