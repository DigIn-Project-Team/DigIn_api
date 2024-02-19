import uuid
from fastapi import FastAPI, Depends, HTTPException, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_204_NO_CONTENT
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.openapi.models import OAuthFlows, OAuthFlowAuthorizationCode
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse

app = FastAPI()

# CORS middleware configuration
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

# Load Google client ID and secret from environment variables
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# Google OAuth 설정
google_oauth = OAuth()
google_oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    authorize_kwargs=None,
    token_url='https://accounts.google.com/o/oauth2/token',
    token_params=None,
    client_kwargs={'scope': 'openid profile email'},
)

# Google 로그인을 위한 보안 설정
oauth2_scheme_google = OAuth2AuthorizationCodeBearer(
    authorizationUrl='login',
    tokenUrl='token',
    flows=OAuthFlows(
        authorizationCode=OAuthFlowAuthorizationCode(
            authorizationUrl='login',
            tokenUrl='token',
        )
    )
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

# Google 로그인 라우터
@app.get("/login")
async def login(request: Request, google=Depends(google_oauth.create_client)):
    return await google.authorize_redirect(request, redirect_uri="your_redirect_uri")

@app.get("/token")
async def token(request: Request, google=Depends(google_oauth.create_client)):
    token = await google.authorize_access_token(request)
    user = await google.parse_id_token(request, token)
    return {"token_type": "bearer", "access_token": token["access_token"], "user": user}

# 리다이렉트 URI 처리를 위한 라우터
@app.get("/redirect_uri")
async def redirect_uri(request: Request, code: str):
    return {"code": code}

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
