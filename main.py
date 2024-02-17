import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_204_NO_CONTENT

app = FastAPI()

class digin_grass(BaseModel):
    user_id: str
    name: str
    description: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/{grass_id}")
async def get_DigIn(grass_id: str):
    return JSONResponse({
        "id": grass_id
    })

@app.post("/{grass_id}")
async def post_DigIn(item: digin_grass):
    jandi = dict(item.dict())
    return JSONResponse(jandi)

@app.put("/{grass_id}")
async def update_DigIn(item: digin_grass):
    jandi = {"name": item.name, "description": item.description, **item.dict()}
    return JSONResponse(jandi)

@app.delete("/{grass_id}")
async def delete_DigIn():
    return Response(status_code=HTTP_204_NO_CONTENT)

@app.get("/{user_id}")
async def get_grass(user_id: str):
    return JSONResponse({"user_id": user_id})

@app.post("/{grass_id}/fill")
async def fill_grass(grass_id:str):
    return JSONResponse({"grass_id": grass_id, "count": int})
