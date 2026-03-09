from datetime import datetime
from fastapi import FastAPI, HTTPException
from AllClass import *
import uvicorn

app = FastAPI()

store = GameStore("GameStore Demo")


@app.get("/")
def test_connection():
	return {"message": "Hello World"}


# -------------------------
# Customer
# -------------------------
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


# -------------------------
# Staff / Manager
# -------------------------
@app.post("/staffs")
def create_staff(name: str, age: int):
	try:
		staff = store.create_staff(name, age)
		return {
			"id": staff.id
		}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))


@app.post("/managers")
def create_manager(name: str, age: int):
	try:
		manager = store.create_manager(name, age)
		return {
			"id": manager.id
		}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# Room
# -------------------------
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


# -------------------------
# Reservation
# -------------------------
@app.post("/reservations")
def create_reservation(
	customer_id: str,
	room_id: str,
	start_time: datetime,
	end_time: datetime
):
	try:
		reservation_id = store.create_reservation(customer_id, room_id, start_time, end_time)
		reservation = store.get_reservation_by_id(reservation_id)
		return {
			"id": reservation.id,
			"status": reservation.status.value,
			"start_time": reservation.start_time,
			"end_time": reservation.end_time,
			"room_id": reservation.room.id,
			"customer_id": reservation.customer.id
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


@app.patch("/reservations/check-in")
def check_in(customer_id: str, reservation_id: str):
	try:
		reservation = store.check_in(customer_id, reservation_id)
		return {
			"message": "Check in success",
			"id": reservation.id,
			"status": reservation.status.value,
			"room_id": reservation.room.id,
			"customer_id": reservation.customer.id
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.patch("/reservations/check-out")
def check_out(customer_id: str, reservation_id: str):
	try:
		reservation = store.check_out(customer_id, reservation_id)
		return {
			"message": "Check out success",
			"id": reservation.id,
			"status": reservation.status.value,
			"room_id": reservation.room.id,
			"customer_id": reservation.customer.id
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# Member
# -------------------------
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


# -------------------------
# Product / Game / Machine
# -------------------------
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
			"id": game.id
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
			"id": machine.id
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# Stock
# -------------------------
@app.get("/stocks")
def get_all_stocks():
	try:
		stocks = store.get_all_stock()
		return [
			{
				"id": stock.id,
				"product_id": stock.product.id
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
			"product_id": stock.product.id
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# Shelf
# -------------------------
@app.post("/shelves")
def create_shelf(max_capacity: int):
	try:
		shelf = store.create_shelf(max_capacity)
		return {
			"id": shelf.id,
			"max_capacity": shelf.max_capacity,
			"current_amount": len(shelf.product_on__shelf)
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
				"id": shelf.id,
				"max_capacity": shelf.max_capacity,
				"current_amount": len(shelf.product_on__shelf)
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
			"shelf_id": shelf.id,
			"current_amount": len(shelf.product_on__shelf),
			"max_capacity": shelf.max_capacity
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# Coupon
# -------------------------
@app.post("/coupons")
def create_coupon(
	manager_id: str,
	customer_id: str,
	minimum_amount: float,
	discount_amount: float,
	expire_date: datetime
):
	try:
		coupon = store.create_coupon(
			manager_id,
			customer_id,
			minimum_amount,
			discount_amount,
			expire_date
		)
		return {
			"id": coupon.id,
			"type": coupon.type,
			"minimum_amount": coupon.minimum_amount,
			"discount_amount": coupon.discount_amount,
			"expire_date": coupon.expire_date
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# Cart
# -------------------------
@app.post("/cart/items")
def add_product_to_cart(customer_id: str, product_id: str):
	try:
		cart = store.add_product_to_customer(customer_id, product_id)
		return {
			"message": "Product added to cart",
			"total_items": len(cart.products)
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.get("/cart")
def view_cart(customer_id: str):
	try:
		cart_items = store.view_cart(customer_id)
		return [
			{
				"serial_number": item.product_item.serial_number,
				"product_id": item.product_item.product.id,
				"is_buy": item.is_buy
			}
			for item in cart_items
		]
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.delete("/cart/items")
def remove_item_from_cart(customer_id: str, product_id: str):
	try:
		cart = store.remove_item_from_cart(customer_id, product_id)
		return {
			"message": "Product removed from cart",
			"total_items": len(cart.products)
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# Product Detail
# -------------------------
@app.get("/products/detail")
def view_product_detail(serial_number: str):
	try:
		product_detail = store.view_product_detail(serial_number)
		if product_detail is None:
			raise HTTPException(status_code=404, detail="Product item not found")

		return {
			"serial_number": serial_number,
			"status": product_detail["status"].value,
			"sell_price": product_detail["sell_price"],
			"condition": product_detail["condition"]
		}
	except HTTPException:
		raise
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# Room Item Request
# -------------------------
@app.post("/rooms/request-item")
def request_item_for_room(
	customer_id: str,
	reservation_id: str,
	product_id: str,
	quantity: int
):
	try:
		room = store.request_item_for_room(customer_id, reservation_id, product_id, quantity)
		return {
			"message": "Item requested for room",
			"room_id": room.id,
			"total_items_in_room": len(room.product_item_list)
		}
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
	uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)