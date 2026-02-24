from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from subscribeClass import GameStore, Customer, Reservation
import uvicorn

app = FastAPI()

store = GameStore("GameStore Demo")

@app.get("/")
def test_connection():
	return "Hello World"

@app.post("/create_customer")
def create_customer(name: str, age: int):
	return store.create_customer(name, age).id

@app.get("/get_all_customer")
def	get_all_customer():
	return [customer.id for customer in store.get_all_customer()]

@app.post("/subscribe")
def subscribe(customer_id: str, payment_gateway_name: str, payment_information: str):
	try:
		return store.subscribe(customer_id, payment_gateway_name, payment_information)
	except Exception as e:
		return {e.__str__()}

@app.get("/check_member")
def check_member(member_id: str):
	try:
		return store.get_member_by_id(member_id)
	except Exception as e:
		return {e.__str__()}

if __name__ == "__main__":
	uvicorn.run("subscribeAPI:app",host="127.0.0.1",port=8000,reload=True)