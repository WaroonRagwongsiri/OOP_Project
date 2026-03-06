from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from AllClass import *
import uvicorn

app = FastAPI()

store = GameStore("GameStore Demo")

@app.get("/")
def test_connection():
	return "Hello World"

if __name__ == "__main__":
	uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)