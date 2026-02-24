from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from create_game_discClass import GameStore, Customer, Reservation
import uvicorn

app = FastAPI()

store = GameStore("GameStore Demo")

@app.get("/")
def test_connection():
	return "Hello World"

@app.post("/create_manager")
def create_manager(name: str, age: int):
	try:
		return store.create_manager(name, age).id
	except Exception as e:
		return {e.__str__()}

@app.post("/create_game")
def create_game(manager_id: str, name: str, price: float, description: str, genre: str, support_platform: str):
	try:
		return store.create_game_disc(manager_id, name, price, description, genre, support_platform).id
	except Exception as e:
		return {e.__str__()}


if __name__ == "__main__":
	uvicorn.run("create_game_discAPI:app",host="127.0.0.1",port=8000,reload=True)