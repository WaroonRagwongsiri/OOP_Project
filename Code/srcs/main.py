from datetime import datetime

from mcp.server.fastmcp import FastMCP

from AllClass import *

mcp = FastMCP("OOP Project")
store = GameStore("GameStore Demo")

@mcp.tool()
def test_connection():
	"""
    Test the connection to the GameStore MCP service.

    Returns:
        dict: A dictionary indicating the service name to confirm
        that the API connection is functioning.
    """
	return {"service": "GameStore API"}

@mcp.tool()
def create_customer(name: str, age: int):
	"""
    Create a new customer in the GameStore system.

    Args:
        name (str): Name of the customer.
        age (int): Age of the customer.

    Returns:
        dict: Customer information including id, name, and age.

    Raises:
        Exception: If customer creation fails.
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
    Retrieve all registered customers.

    Returns:
        list[dict]: List of customers containing:
            - id (str): Customer identifier
            - name (str): Customer name
            - age (int): Customer age
    """
	customers = store.get_all_customer()
	return [
		{
			"id": customer.id,
			"name": customer.name,
			"age": customer.age
		}
		for customer in customers
	]


@mcp.tool()
def create_room(max_customer: int, rate_price: float):
	"""
    Create a new game room.

    Args:
        max_customer (int): Maximum number of customers allowed in the room.
        rate_price (float): Hourly or session price for the room.

    Returns:
        dict: Room information including id and status.

    Raises:
        Exception: If the room cannot be created.
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
    Retrieve all rooms that are currently available.

    Returns:
        list[dict]: List of available rooms including:
            - id (str): Room identifier
            - status (str): Current room status
    """
	rooms = store.get_available_room()
	return [
		{
			"id": room.id,
			"status": room.status
		}
		for room in rooms
	]


@mcp.tool()
def create_reservation(
	customer_id: str,
	room_id: str,
	start_time: datetime,
	end_time: datetime
):
	"""
    Create a reservation for a room.

    Args:
        customer_id (str): Identifier of the customer making the reservation.
        room_id (str): Identifier of the room to reserve.
        start_time (datetime): Reservation start time.
        end_time (datetime): Reservation end time.

    Returns:
        dict: Reservation details including id, status, start_time, and end_time.

    Raises:
        ValueError: If reservation validation fails.
        Exception: For unexpected system errors.
    """
	try:
		reservation = store.create_reservation(customer_id, room_id, start_time, end_time)
		return {
			"id": reservation.id,
			"status": reservation.status,
			"start_time": reservation.start_time,
			"end_time": reservation.end_time
		}
	except ValueError as e:
		return f"Error: {e.__str__()}"
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def cancel_reservation(customer_id: str, reservation_id: str):
	"""
    Cancel an existing reservation.

    Args:
        customer_id (str): Identifier of the customer requesting cancellation.
        reservation_id (str): Identifier of the reservation.

    Returns:
        dict: Cancellation confirmation including reservation id and status.

    Raises:
        ValueError: If the reservation or customer is invalid.
        Exception: For unexpected system errors.
    """
	try:
		reservation = store.cancel_reservation(customer_id, reservation_id)
		return {
			"message": "Reservation cancelled",
			"id": reservation.id,
			"status": reservation.status
		}
	except ValueError as e:
		return f"Error: {e.__str__()}"
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def subscribe(
	customer_id: str,
	payment_gateway_name: str,
	payment_information: str
):
	"""
    Subscribe a customer to the membership program.

    Args:
        customer_id (str): Identifier of the customer.
        payment_gateway_name (str): Payment provider used for subscription.
        payment_information (str): Payment details or reference.

    Returns:
        dict: Membership details including member_id, customer_id, and status.

    Raises:
        ValueError: If subscription validation fails.
        Exception: For unexpected system errors.
    """
	try:
		member = store.subscribe(customer_id, payment_gateway_name, payment_information)
		return {
			"member_id": member.member_id,
			"customer_id": member.id,
			"status": member.status
		}
	except ValueError as e:
		return f"Error: {e.__str__()}"
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def unsubscribe(member_id: str):
	"""
    Cancel a customer's membership subscription.

    Args:
        member_id (str): Identifier of the membership.

    Returns:
        dict: Message indicating whether the unsubscription succeeded.

    Raises:
        ValueError: If the member_id is invalid.
        Exception: For unexpected system errors.
    """
	try:
		result = store.unsubscribe(member_id)
		return {
			"message": result
		}
	except ValueError as e:
		return f"Error: {e.__str__()}"
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def create_manager(name: str, age: int):
	"""
    Create a new manager account.

    Args:
        name (str): Manager's name.
        age (int): Manager's age.

    Returns:
        dict: Manager information including id, name, and age.

    Raises:
        Exception: If manager creation fails.
    """
	try:
		manager = store.create_manager(name, age)
		return {
			"id": manager.id,
			"name": manager.name,
			"age": manager.age
		}
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def create_game(
	manager_id: str,
	name: str,
	description: str,
	genre: str,
	game_type: str
):
	"""
    Create a new game product.

    Args:
        manager_id (str): Identifier of the manager creating the game.
        name (str): Name of the game.
        description (str): Game description.
        genre (str): Game genre category.
        game_type (str): Type of game (DISC, KEYCARD, CARTRIDGE).

    Returns:
        dict: Created game information including id and name.

    Raises:
        ValueError: If validation fails.
        Exception: For unexpected system errors.
    """
	try:
		game = store.create_game(manager_id, name, description, genre, game_type)
		return {
			"id": game.id,
			"name": game.name
		}
	except ValueError as e:
		return f"Error: {e.__str__()}"
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def create_machine(
	manager_id: str,
	name: str,
	machine_type: str
):
	"""
    Create a new gaming machine.

    Args:
        manager_id (str): Identifier of the manager.
        name (str): Machine name.
        machine_type (str): Type of machine.

    Returns:
        dict: Machine information including id and name.

    Raises:
        ValueError: If validation fails.
        Exception: For unexpected system errors.
    """
	try:
		machine = store.create_machine(manager_id, name, machine_type)
		return {
			"id": machine.id,
			"name": machine.name
		}
	except ValueError as e:
		return f"Error: {e.__str__()}"
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def get_all_stocks():
	"""
    Retrieve all stock items in the inventory.

    Returns:
        list[dict]: Stock records including:
            - id (str): Stock identifier
            - product_id (str): Product identifier
            - product_name (str): Name of the product
    """
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
		return f"Error: {e.__str__()}"


@mcp.tool()
def refill_stock(
	manager_id: str,
	stock_id: str,
	quantity: int,
	sell_price: float
):
	"""
    Refill inventory stock for a product.

    Args:
        manager_id (str): Identifier of the manager performing the refill.
        stock_id (str): Identifier of the stock entry.
        quantity (int): Quantity of product added.
        sell_price (float): Selling price for the product.

    Returns:
        dict: Confirmation including stock id and product details.

    Raises:
        ValueError: If refill validation fails.
        Exception: For unexpected system errors.
    """
	try:
		stock = store.refill_stock(manager_id, stock_id, quantity, sell_price)
		return {
			"message": "Stock refilled",
			"stock_id": stock.id,
			"product_id": stock.product.id,
			"product_name": stock.product.name
		}
	except ValueError as e:
		return f"Error: {e.__str__()}"
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def create_shelf(max_capacity: int):
	"""
    Create a new shelf for product display.

    Args:
        max_capacity (int): Maximum number of items the shelf can hold.

    Returns:
        dict: Shelf identifier.

    Raises:
        ValueError: If capacity validation fails.
        Exception: For unexpected system errors.
    """
	try:
		shelf = store.create_shelf(max_capacity)
		return {
			"id": shelf.id
		}
	except ValueError as e:
		return f"Error: {e.__str__()}"
	except Exception as e:
		return f"Error: {e.__str__()}"


@mcp.tool()
def get_all_shelves():
	"""
    Retrieve all shelves in the store.

    Returns:
        list[dict]: List of shelf identifiers.
    """
	try:
		shelves = store.get_all_shelf()
		return [
			{
				"id": shelf.id
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
    Move items from stock to a shelf.

    Args:
        staff_id (str): Identifier of the staff member performing the refill.
        shelf_id (str): Identifier of the shelf.
        stock_id (str): Identifier of the stock source.
        quantity (int): Quantity of items placed on the shelf.

    Returns:
        dict: Confirmation message including shelf id.

    Raises:
        ValueError: If validation fails.
        Exception: For unexpected system errors.
    """
	try:
		shelf = store.refill_shelf(staff_id, shelf_id, stock_id, quantity)
		return {
			"message": "Shelf refilled",
			"shelf_id": shelf.id
		}
	except ValueError as e:
		return f"Error: {e.__str__()}"
	except Exception as e:
		return f"Error: {e.__str__()}"

def main():
	mcp.run(transport="stdio")

if __name__ == "__main__":
	main()
