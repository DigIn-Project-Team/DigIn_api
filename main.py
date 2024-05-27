import uuid
from fastapi import FastAPI, Depends, HTTPException, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse, Response, RedirectResponse
from starlette.status import HTTP_204_NO_CONTENT
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "supersecretkey"),
)

# Load OAuth configuration from environment variables
config = Config('.env')
oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:8000/auth',
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

class DiginGrass(BaseModel):
    user_id: str
    name: str
    description: str

class ResponseModal(BaseModel):
    id: str

class RequestToken(BaseModel):
    id_token: str

@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse({"message": "Hello World"})

@app.get("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    return JSONResponse({"token": token, "user": user})

@app.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/{grass_id}", response_model=DiginGrass)
async def get_DigIn(grass_id: str) -> JSONResponse:
    return JSONResponse({"id": grass_id})

@app.post("/{grass_id}")
async def post_DigIn(item: DiginGrass) -> JSONResponse:
    jandi = dict(item.dict())
    return JSONResponse(jandi)

@app.put("/{grass_id}")
async def update_DigIn(item: DiginGrass) -> JSONResponse:
    jandi = {"name": item.name, "description": item.description, **item.dict()}
    return JSONResponse(jandi)

@app.delete("/{grass_id}")
async def delete_DigIn() -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)

@app.get("/{user_id}")
async def get_grass(user_id: str) -> JSONResponse:
    return JSONResponse({"user_id": user_id})

@app.post("/{grass_id}/fill")
async def fill_grass(grass_id: str) -> JSONResponse:
    return JSONResponse({"grass_id": grass_id, "count": int})
