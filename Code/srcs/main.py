from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from AllClass import *
import uvicorn

app = FastAPI()

store = GameStore("GameStore Demo")


@app.get("/")
def test_connection():
	return {"message": "Hello World"}


@app.post("/customers")
def create_customer(
	name: str,
	age: int
):
	try:
		customer = store.create_customer(name, age)
		return {
			"id": customer.id,
			"name": customer.name,
			"age": customer.age
		}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))


@app.get("/customers")
def get_all_customers():
	customers = store.get_all_customer()
	return [
		{
			"id": customer.id,
			"name": customer.name,
			"age": customer.age
		}
		for customer in customers
	]


@app.post("/rooms")
def create_room(
	max_customer: int,
	rate_price: float
):
	try:
		room = store.create_room(max_customer, rate_price)
		return {
			"id": room.id,
			"status": room.status.value
		}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))


@app.get("/rooms/available")
def get_available_rooms():
	rooms = store.get_available_room()
	return [
		{
			"id": room.id,
			"status": room.status.value
		}
		for room in rooms
	]


@app.post("/bookings")
def create_booking(
	customer_id: str,
	room_id: str,
	start_time: datetime,
	end_time: datetime
):
	try:
		reservation_id = store.create_booking(customer_id, room_id, start_time, end_time)
		return {
			"reservation_id": reservation_id
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.post("/subscribe")
def subscribe(
	customer_id: str,
	payment_gateway_name: str,
	payment_information: str
):
	try:
		member_id = store.subscribe(customer_id, payment_gateway_name, payment_information)
		return {
			"member_id": member_id
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.post("/managers")
def create_manager(
	name: str,
	age: int
):
	try:
		manager = store.create_manager(name, age)
		return {
			"id": manager.id
		}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))


@app.post("/games")
def create_game(
	manager_id: str,
	name: str,
	description: str,
	genre: str,
	game_type: str
):
	try:
		result = store.create_game(manager_id, name, description, genre, game_type)

		if isinstance(result, str) and result.startswith("Error:"):
			raise HTTPException(status_code=400, detail=result)

		return {
			"id": result.id
		}
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.post("/machines")
def create_machine(
	manager_id: str,
	name: str,
	machine_type: str
):
	try:
		result = store.create_machine(manager_id, name, machine_type)

		if isinstance(result, str) and result.startswith("Error:"):
			raise HTTPException(status_code=400, detail=result)

		return {
			"id": result.id
		}
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.patch("/bookings/cancel")
def cancel_booking(
	customer_id: str,
	reservation_id: str
):
	try:
		result = store.cancel_booking(customer_id, reservation_id)

		if isinstance(result, str) and result.startswith("Error:"):
			raise HTTPException(status_code=400, detail=result)

		return {
			"message": "Reservation cancelled"
		}
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@app.patch("/members/unsubscribe")
def unsubscribe(member_id: str):
	try:
		result = store.unsubscribe(member_id)

		if isinstance(result, str) and result.startswith("Error:"):
			raise HTTPException(status_code=400, detail=result)

		return {
			"message": "Member unsubscribed"
		}
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
	uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)