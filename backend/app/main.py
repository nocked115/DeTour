from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
from fastapi import FastAPI #FastAPI 도구 가져오기 
import json 
from pathlib import Path # 파일 경로 다룸(이 코드 파일 기준으로 어디) 

app = FastAPI() # 서버 만들어 - app이라는 이름 붙이기 
app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"], # 아무 출처나 허락
    allow_methods=["*"],
    allow_headers =["*"],
)
DATA_FILE = Path(__file__).parent.parent / "data" / "places.json"

with open(DATA_FILE,encoding ="utf-8") as f:
    PLACES = json.load(f)["places"]

@app.get("/health") #누가 health 주소로 찾아오면 바로 아래 함수 실행해. 
def health():
    return {"status":"ok"} #파이썬 dict 돌려주면 fastapi 알아서 json으로 바꿔서 보내줌 

class RecommendRequest(BaseModel): #이런 모양의 데이터 틀 정의 
    origin: str
    destination: str
    time: int
    budget: int
    activity: str



@app.get("/places") # 주소 
def list_places():
    return {"count": len(PLACES),"places":PLACES}

@app.post("/recommend")
def recommend(req:RecommendRequest):
    candidates = [
        place
        for place in PLACES
        if place["activity"] == req.activity
        and place["stayMinutes"] + place["travelMinutes"] <= req.time
        and place["cost"] <= req.budget
    ]
    candidates.sort(key=lambda p: p["stayMinutes"] + p['travelMinutes'],
                    reverse = True)
    return {
        "origin": req.origin,
        "destination": req.destination,
        "time":req.time,
        "results": candidates[:2],
    }

