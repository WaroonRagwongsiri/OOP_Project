from datetime import datetime
from fastapi import FastAPI, HTTPException
from AllClass import *
import uvicorn

app = FastAPI()

store = GameStore("GameStore Demo")


@app.get("/")
def test_connection():
	return {"message": "Hello World"}


@app.post("/customers")
def create_customer(name: str, age: int):
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
def create_room(max_customer: int, rate_price: float):
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


@app.post("/reservations")
def create_reservation(
	customer_id: str,
	room_id: str,
	start_time: datetime,
	end_time: datetime
):
	try:
		reservation = store.create_reservation(customer_id, room_id, start_time, end_time)
		return {
			"id": reservation.id,
			"status": reservation.status.value,
			"start_time": reservation.start_time,
			"end_time": reservation.end_time
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.patch("/reservations/cancel")
def cancel_reservation(customer_id: str, reservation_id: str):
	try:
		reservation = store.cancel_reservation(customer_id, reservation_id)
		return {
			"message": "Reservation cancelled",
			"id": reservation.id,
			"status": reservation.status.value
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
		member = store.subscribe(customer_id, payment_gateway_name, payment_information)
		return {
			"member_id": member.member_id,
			"customer_id": member.id,
			"status": member.status.value
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.patch("/members/unsubscribe")
def unsubscribe(member_id: str):
	try:
		result = store.unsubscribe(member_id)
		return {
			"message": result
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.post("/managers")
def create_manager(name: str, age: int):
	try:
		manager = store.create_manager(name, age)
		return {
			"id": manager.id,
			"name": manager.name,
			"age": manager.age
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
		game = store.create_game(manager_id, name, description, genre, game_type)
		return {
			"id": game.id,
			"name": game.name
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.post("/machines")
def create_machine(
	manager_id: str,
	name: str,
	machine_type: str
):
	try:
		machine = store.create_machine(manager_id, name, machine_type)
		return {
			"id": machine.id,
			"name": machine.name
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.get("/stocks")
def get_all_stocks():
	try:
		stocks = store.get_all_stock()
		return [
			{
				"id": stock.id,
				"product_id": stock.product.id,
				"product_name": stock.product.name
			}
			for stock in stocks
		]
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.patch("/stocks/refill")
def refill_stock(
	manager_id: str,
	stock_id: str,
	quantity: int,
	sell_price: float
):
	try:
		stock = store.refill_stock(manager_id, stock_id, quantity, sell_price)
		return {
			"message": "Stock refilled",
			"stock_id": stock.id,
			"product_id": stock.product.id,
			"product_name": stock.product.name
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.post("/shelves")
def create_shelf(max_capacity: int):
	try:
		shelf = store.create_shelf(max_capacity)
		return {
			"id": shelf.id
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.get("/shelves")
def get_all_shelves():
	try:
		shelves = store.get_all_shelf()
		return [
			{
				"id": shelf.id
			}
			for shelf in shelves
		]
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.patch("/shelves/refill")
def refill_shelf(
	staff_id: str,
	shelf_id: str,
	stock_id: str,
	quantity: int
):
	try:
		shelf = store.refill_shelf(staff_id, shelf_id, stock_id, quantity)
		return {
			"message": "Shelf refilled",
			"shelf_id": shelf.id
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
	uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)