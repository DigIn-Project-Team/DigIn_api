import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_204_NO_CONTENT
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() # cors 넣어주는게 좋음

app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost",
        "http://localhost:8080",
    ], # 허용할 도메인
    allow_credentials=True, # 요청시 쿠키 지원 여부
    allow_methods=["*"], # 허용할 메서드[get, post, put, fetch, delete 등등] (*[와일드카드] 쓰면 모두 쓸수 있음)
    allow_headers=["*"], # 허용할 헤더 왼만해서는 다 허용해놓음(*[와일드카드]를 써놓음)
)

class DiginGrass(BaseModel): # class, enum등은 다 CamelCase써는게 좋음
    user_id: str
    name: str
    description: str


class ResponseModal(BaseModel): # 반환할 모델 굳이 안해줘도 되는데 있으면 좋음(원래는 다른 파일에 다 모아놓고 import로 가저다 씀)
    id: str

@app.get("/")
async def root() -> JSONResponse: # 반환타입
    return JSONResponse({"message": "Hello World"}) # dict반환 말고 JSONResponse를 써야함


@app.get("/{grass_id}", response_model=DiginGrass) # 반환하는 모델
"""
자세한건 https://fastapi.tiangolo.com/tutorial/response-model/#response_model-parameter 참고하면 돼고 반환 타입은 좀 이상하게 돼있으니까 그거만 참고 하지 마셈 
"""
async def get_DigIn(grass_id: str) -> JSONResponse:
    return JSONResponse({
        "id": grass_id
    })

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
    return JSONResponse({"grass_id": grass_id, "count": int}) # 여기 int뭐하는거임? todo인가
