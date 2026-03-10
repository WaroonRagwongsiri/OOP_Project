from datetime import datetime

from mcp.server.fastmcp import FastMCP

from AllClass import *

mcp = FastMCP("OOP Project")
store = GameStore("Microslop")


@mcp.tool()
def test_connection():
	"""
	Test the connection to the GameStore MCP service.

	Returns:
		dict: A dictionary indicating the service is working.
	"""
	return {"message": "Hello World"}


# -------------------------
# Customer
# -------------------------
@mcp.tool()
def create_customer(name: str, age: int):
	"""
	Create a new customer.

	Args:
		name (str): Customer name.
		age (int): Customer age.

	Returns:
		dict: Customer information.
	"""
	try:
		customer = store.create_customer(name, age)
		return {
			"id": customer.id,
			"name": customer.name,
			"age": customer.age
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def get_all_customers():
	"""
	Get all customers.

	Returns:
		list[dict]: Customer records.
	"""
	try:
		customers = store.get_all_customer()
		return [
			{
				"id": customer.id,
				"name": customer.name,
				"age": customer.age
			}
			for customer in customers
		]
	except Exception as e:
		return f"Error: {e.__str__()}"


# -------------------------
# Staff / Manager
# -------------------------
@mcp.tool()
def create_staff(name: str, age: int):
	"""
	Create a new staff.

	Args:
		name (str): Staff name.
		age (int): Staff age.

	Returns:
		dict: Staff information.
	"""
	try:
		staff = store.create_staff(name, age)
		return {
			"id": staff.id
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def create_manager(name: str, age: int):
	"""
	Create a new manager.

	Args:
		name (str): Manager name.
		age (int): Manager age.

	Returns:
		dict: Manager information.
	"""
	try:
		manager = store.create_manager(name, age)
		return {
			"id": manager.id
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


# -------------------------
# Room
# -------------------------
@mcp.tool()
def create_room(max_customer: int, rate_price: float):
	"""
	Create a new room.

	Args:
		max_customer (int): Maximum number of customers in room.
		rate_price (float): Room price.

	Returns:
		dict: Room information.
	"""
	try:
		room = store.create_room(max_customer, rate_price)
		return {
			"id": room.id,
			"status": room.status
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def get_available_rooms():
	"""
	Get all available rooms.

	Returns:
		list[dict]: Available room records.
	"""
	try:
		rooms = store.get_available_room()
		return [
			{
				"id": room.id,
				"status": room.status
			}
			for room in rooms
		]
	except Exception as e:
		return f"Error: {e.__str__()}"


# -------------------------
# Reservation
# -------------------------
@mcp.tool()
def create_reservation(
	customer_id: str,
	room_id: str,
	start_time: datetime,
	end_time: datetime
):
	"""
	Create a reservation.

	Args:
		customer_id (str): Customer id.
		room_id (str): Room id.
		start_time (datetime): Reservation start time.
		end_time (datetime): Reservation end time.

	Returns:
		dict: Reservation information.
	"""
	try:
		reservation_id = store.create_reservation(customer_id, room_id, start_time, end_time)
		reservation = store.get_reservation_by_id(reservation_id)
		return {
			"id": reservation.id,
			"status": reservation.status,
			"start_time": reservation.start_time,
			"end_time": reservation.end_time,
			"room_id": reservation.room.id,
			"customer_id": reservation.customer.id
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def cancel_reservation(customer_id: str, reservation_id: str):
	"""
	Cancel a reservation.

	Args:
		customer_id (str): Customer id.
		reservation_id (str): Reservation id.

	Returns:
		dict: Cancellation result.
	"""
	try:
		reservation = store.cancel_reservation(customer_id, reservation_id)
		return {
			"message": "Reservation cancelled",
			"id": reservation.id,
			"status": reservation.status
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def check_in(customer_id: str, reservation_id: str):
	"""
	Check in a reservation.

	Args:
		customer_id (str): Customer id.
		reservation_id (str): Reservation id.

	Returns:
		dict: Check-in result.
	"""
	try:
		reservation = store.check_in(customer_id, reservation_id)
		return {
			"message": "Check in success",
			"id": reservation.id,
			"status": reservation.status,
			"room_id": reservation.room.id,
			"customer_id": reservation.customer.id
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def check_out(customer_id: str, reservation_id: str):
	"""
	Check out a reservation.

	Args:
		customer_id (str): Customer id.
		reservation_id (str): Reservation id.

	Returns:
		dict: Check-out result.
	"""
	try:
		reservation = store.check_out(customer_id, reservation_id)
		return {
			"message": "Check out success",
			"id": reservation.id,
			"status": reservation.status,
			"room_id": reservation.room.id,
			"customer_id": reservation.customer.id
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def extend_time(customer_id: str, reservation_id: str, additional_hours: float):
	"""
	Extend reservation time.

	Args:
		customer_id (str): Customer id.
		reservation_id (str): Reservation id.
		additional_hours (float): Additional hours to add.

	Returns:
		dict: Updated reservation information.
	"""
	try:
		reservation = store.extend_time(customer_id, reservation_id, additional_hours)
		return {
			"message": "Reservation extended",
			"id": reservation.id,
			"status": reservation.status,
			"start_time": reservation.start_time,
			"end_time": reservation.end_time,
			"room_id": reservation.room.id,
			"customer_id": reservation.customer.id,
			"additional_hours": additional_hours
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


# -------------------------
# Member
# -------------------------
@mcp.tool()
def subscribe(
	customer_id: str,
	payment_gateway_name: str,
	payment_information: str
):
	"""
	Subscribe a customer as a member.

	Args:
		customer_id (str): Customer id.
		payment_gateway_name (str): Payment gateway name.
		payment_information (str): Payment information.

	Returns:
		dict: Membership information.
	"""
	try:
		member = store.subscribe(customer_id, payment_gateway_name, payment_information)
		return {
			"member_id": member.member_id,
			"customer_id": member.id,
			"status": member.status
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def unsubscribe(member_id: str):
	"""
	Unsubscribe a member.

	Args:
		member_id (str): Member id.

	Returns:
		dict: Unsubscribe result.
	"""
	try:
		result = store.unsubscribe(member_id)
		return {
			"message": result
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


# -------------------------
# Product / Game / Machine
# -------------------------
@mcp.tool()
def create_game(
	manager_id: str,
	name: str,
	description: str,
	genre: str,
	game_type: str
):
	"""
	Create a new game.

	Args:
		manager_id (str): Manager id.
		name (str): Game name.
		description (str): Game description.
		genre (str): Game genre.
		game_type (str): Game type.

	Returns:
		dict: Game information.
	"""
	try:
		game = store.create_game(manager_id, name, description, genre, game_type)
		return {
			"id": game.id
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def create_machine(
	manager_id: str,
	name: str,
	machine_type: str
):
	"""
	Create a new machine.

	Args:
		manager_id (str): Manager id.
		name (str): Machine name.
		machine_type (str): Machine type.

	Returns:
		dict: Machine information.
	"""
	try:
		machine = store.create_machine(manager_id, name, machine_type)
		return {
			"id": machine.id
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


# -------------------------
# Stock
# -------------------------
@mcp.tool()
def get_all_stocks():
	"""
	Get all stocks.

	Returns:
		list[dict]: Stock records.
	"""
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
		return f"Error: {e.__str__()}"


@mcp.tool()
def refill_stock(
	manager_id: str,
	stock_id: str,
	quantity: int,
	sell_price: float
):
	"""
	Refill stock.

	Args:
		manager_id (str): Manager id.
		stock_id (str): Stock id.
		quantity (int): Quantity to add.
		sell_price (float): Sell price.

	Returns:
		dict: Refill result.
	"""
	try:
		stock = store.refill_stock(manager_id, stock_id, quantity, sell_price)
		return {
			"message": "Stock refilled",
			"stock_id": stock.id,
			"product_id": stock.product.id,
			"quantity": len(stock.product_item_list),
			"sell_price": stock.product_item_list[-1].calculate_price()
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


# -------------------------
# Shelf
# -------------------------
@mcp.tool()
def create_shelf(max_capacity: int):
	"""
	Create a shelf.

	Args:
		max_capacity (int): Shelf capacity.

	Returns:
		dict: Shelf information.
	"""
	try:
		shelf = store.create_shelf(max_capacity)
		return {
			"id": shelf.id,
			"max_capacity": shelf.max_capacity,
			"current_amount": len(shelf.product_on_shelf)
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def get_all_shelves():
	"""
	Get all shelves.

	Returns:
		list[dict]: Shelf records.
	"""
	try:
		shelves = store.get_all_shelf()
		return [
			{
				"id": shelf.id,
				"max_capacity": shelf.max_capacity,
				"current_amount": len(shelf.product_on_shelf)
			}
			for shelf in shelves
		]
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def refill_shelf(
	staff_id: str,
	shelf_id: str,
	stock_id: str,
	quantity: int
):
	"""
	Refill a shelf from stock.

	Args:
		staff_id (str): Staff id.
		shelf_id (str): Shelf id.
		stock_id (str): Stock id.
		quantity (int): Quantity to move.

	Returns:
		dict: Refill result.
	"""
	try:
		shelf = store.refill_shelf(staff_id, shelf_id, stock_id, quantity)
		return {
			"message": "Shelf refilled",
			"shelf_id": shelf.id,
			"current_amount": len(shelf.product_on_shelf),
			"max_capacity": shelf.max_capacity
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


# -------------------------
# Coupon
# -------------------------
@mcp.tool()
def create_coupon(
	manager_id: str,
	customer_id: str,
	minimum_amount: float,
	discount_amount: float,
	expire_date: datetime
):
	"""
	Create a coupon.

	Args:
		manager_id (str): Manager id.
		customer_id (str): Customer id.
		minimum_amount (float): Minimum amount.
		discount_amount (float): Discount amount.
		expire_date (datetime): Expiration date.

	Returns:
		dict: Coupon information.
	"""
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
	except Exception as e:
		return f"Error: {e.__str__()}"

@mcp.tool()
def view_coupon(customer_id: str):
	"""
	View Coupon customer have

	Args:
		customer_id (str): Customer id

	Returns:
		dict: Coupon information
	"""
	try:
		coupon_list = store.view_coupon(customer_id)

		return {
			"customer_id": customer_id,
			"coupons": [
				{
					"id": coupon.id,
					"type": coupon.type,
					"minimum_amount": coupon.minimum_amount,
					"discount_amount": coupon.discount_amount,
					"expire_date": coupon.expire_date
				}
				for coupon in coupon_list
			]
		}
	except Exception as e:
		return f"Error: {e.__str__()}"

# -------------------------
# Cart
# -------------------------
@mcp.tool()
def add_product_to_cart(customer_id: str, product_id: str):
	"""
	Add a product to customer cart.

	Args:
		customer_id (str): Customer id.
		product_id (str): Product id.

	Returns:
		dict: Cart summary.
	"""
	try:
		cart = store.add_product_to_customer(customer_id, product_id)
		return {
			"message": "Product added to cart",
			"total_items": len(cart.products)
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def view_cart(customer_id: str):
	"""
	View a customer cart.

	Args:
		customer_id (str): Customer id.

	Returns:
		list[dict]: Cart items.
	"""
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
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def remove_item_from_cart(customer_id: str, product_id: str):
	"""
	Remove an item from customer cart.

	Args:
		customer_id (str): Customer id.
		product_id (str): Product id.

	Returns:
		dict: Cart summary.
	"""
	try:
		cart = store.remove_item_from_cart(customer_id, product_id)
		return {
			"message": "Product removed from cart",
			"total_items": len(cart.products)
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


# -------------------------
# Product Detail
# -------------------------
@mcp.tool()
def view_product_detail(serial_number: str):
	"""
	View product detail by serial number.

	Args:
		serial_number (str): Product serial number.

	Returns:
		dict | None: Product detail or None.
	"""
	try:
		product_detail = store.view_product_detail(serial_number)
		if product_detail is None:
			return None

		return {
			"serial_number": serial_number,
			"status": product_detail["status"],
			"sell_price": product_detail["sell_price"],
			"condition": product_detail["condition"]
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


# -------------------------
# Room Item Request
# -------------------------
@mcp.tool()
def request_item_for_room(
	customer_id: str,
	reservation_id: str,
	product_id: str,
	quantity: int
):
	"""
	Request item for a room.

	Args:
		customer_id (str): Customer id.
		reservation_id (str): Reservation id.
		product_id (str): Product id.
		quantity (int): Quantity requested.

	Returns:
		dict: Room item request result.
	"""
	try:
		room = store.request_item_for_room(customer_id, reservation_id, product_id, quantity)
		return {
			"message": "Item requested for room",
			"room_id": room.id,
			"total_items_in_room": len(room.product_item_list)
		}
	except Exception as e:
		return f"Error: {e.__str__()}"

# -------------------------
# Cart Purchase Controls
# -------------------------
@mcp.tool()
def set_cart_item_buy(customer_id: str, serial_number: str, is_buy: bool):
	"""
	Mark a cart item as selected for purchase.

	Args:
		customer_id (str): Customer id.
		serial_number (str): Product serial number.
		is_buy (bool): True if customer wants to buy.

	Returns:
		dict: Updated cart item.
	"""
	try:
		store.set_cart_item_buy(customer_id, serial_number, is_buy)
		return {
				"serial_number": serial_number,
				"is_buy": is_buy
			}
	except Exception as e:
		return f"Error: {e.__str__()}"


# -------------------------
# Purchase
# -------------------------
@mcp.tool()
def purchase(
	customer_id: str,
	payment_method_name: str,
	payment_information: list,
	coupon_id: str = None
):
	"""
	Purchase selected items in cart.

	Args:
		customer_id (str): Customer id.
		payment_method_name (str): Payment method.
		payment_information (list): Payment information.
		coupon_id (str | None): Coupon id.

	Returns:
		dict: Purchase result.
	"""
	try:
		bill, product_serials = store.purchase(
			customer_id,
			payment_method_name,
			payment_information,
			coupon_id
		)

		return {
			"bill_id": bill.id,
			"amount": bill.amount,
			"products": product_serials
		}

	except Exception as e:
		return f"Error: {e.__str__()}"


# -------------------------
# Refund
# -------------------------
@mcp.tool()
def refund(
	customer_id: str,
	bill_id: str,
	product_serial_numbers: list[str]
):
	"""
	Refund purchased items.

	Args:
		customer_id (str): Customer id.
		bill_id (str): Bill id.
		product_serial_numbers (list[str]): Product serial numbers.

	Returns:
		dict: Refund result.
	"""
	try:
		coupon = store.refund(customer_id, bill_id, product_serial_numbers)

		return {
			"message": "Refund successful",
			"coupon_id": coupon.id,
			"discount_amount": coupon.discount_amount,
			"expire_date": coupon.expire_date
		}

	except Exception as e:
		return f"Error: {e.__str__()}"


def main():
	mcp.run(transport="stdio")


if __name__ == "__main__":
	main()