from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
import uuid

from abc import ABC, abstractmethod


def make_id(prefix: str) -> str:
	# Example: C-550e8400-e29b-41d4-a716-446655440000
	return f"{prefix}-{uuid.uuid4()}"


class Customer:
	def __init__(self, customer_id: str, name: str, age: int):
		self.__customer_id: str = customer_id
		self.__name: str = name
		self.__age: int = age
		self.__cart: "Cart" = Cart(self)
		self.__reservation_list: list[Reservation] = []
		self.__bill_list: list[Bill] = []
		self.__coupons_list: list[Coupon] = []

	def get_customer_id(self) -> str:
		return self.__customer_id

	def get_cart(self) -> "Cart":
		return self.__cart

	def get_reservation_list(self) -> list[Reservation]:
		return self.__reservation_list

	def add_reservation(self, reservation: "Reservation"):
		self.__reservation_list.append(reservation)

	def get_name(self) -> str:
		return self.__name

	def get_age(self) -> int:
		return self.__age

	@property
	def bill_list(self) -> list[Bill]:
		return self.__bill_list

	name = property(get_name)
	age = property(get_age)
	cart = property(get_cart)
	reservation_list = property(fget=get_reservation_list)
	id = property(fget=get_customer_id)

	@property
	def coupons(self) -> list[Coupon]:
		return self.__coupons_list

	def check_time_availability(self, start_time: datetime, end_time: datetime) -> bool:
		for reservation in self.__reservation_list:
			if start_time < reservation.end_time and end_time > reservation.start_time and reservation.status != ReservationStatusEnum.CANCEL:
				return False
		return True

	def get_reservation_from_id(self, reservation_id: str) -> Reservation:
		for reservation in self.__reservation_list:
			if reservation.id == reservation_id:
				return reservation
		return None

	def add_bill(self, bill: Bill):
		self.__bill_list.append(bill)

	def apply_discount_benefit(self) -> float:
		return 1

	def add_coupon(self, coupon: Coupon):
		self.__coupons_list.append(coupon)

class MemberStatusEnum(Enum):
	ACTIVE = "Active"
	INACTIVE = "Inactive"

class Cart:
	def __init__(self, owner: Customer):
		self.__owner: Customer = owner
		self.__products: list["CartItem"] = []

	@property
	def products(self):
		return self.__products
	
class CartItem:
	def __init__(self, product_item: "ProductItem"):
		self.__is_buy: bool = False
		self.__product_item: "ProductItem" = product_item

	@property
	def is_buy(self):
		return self.__is_buy
	@is_buy.setter
	def is_buy(self, value: bool):
		self.__is_buy = value

	@property
	def product_item(self):
		return self.__product_item

# Member Always get 15% discount
class Member(Customer):
	def __init__(self, member_id: str, customer_id: str, name: str, age: int):
		super().__init__(customer_id, name, age)
		self.__member_id: str = member_id
		self.__expire_date: datetime = datetime.today()
		self.__status: MemberStatusEnum = MemberStatusEnum.ACTIVE

	def get_member_id(self) -> str:
		return self.__member_id

	def get_status(self) -> MemberStatusEnum:
		return self.__status

	def set_status(self, status: MemberStatusEnum):
		self.__status = status

	member_id = property(get_member_id)
	status = property(get_status, set_status)

	def apply_discount_benefit(self) -> float:
		return 0.85

class Staff:
	def __init__(self, id: str, name: str, age: int):
		self.__id: str = id
		self.__name: str = name
		self.__age: int = age

	def get_id(self) -> str:
		return self.__id

	id = property(get_id)

class Manager(Staff):
	def __init__(self, id, name, age):
		super().__init__(id, name, age)

class Product:
	def __init__(self, id: str, name: str):
		self._id = id
		self._name = name

	def get_id(self) -> str:
		return self._id

	id = property(get_id)

class Game(Product):
	def __init__(self, id: str, name: str, description: str, genre: str, support_platform: tuple[Machine]):
		super().__init__(id, name)
		self.__description: str = description
		self.__genre: str = genre
		self.__support_platform: tuple[Machine] = support_platform

	def play(self):
		return f"Playing {self._name}"

	def get_support_platform(self) -> tuple[Machine]:
		return self.__support_platform

	support_platform = property(get_support_platform)

class GameDisc(Game):
	def __init__(self, id, name, description, genre):
		super().__init__(id, name, description, genre, (PC, Playstation))

class GameCartridge(Game):
	def __init__(self, id, name, description, genre):
		super().__init__(id, name, description, genre, (GameBoy))

class GameKeyCard(Game):
	def __init__(self, id, name, description, genre):
		super().__init__(id, name, description, genre, (Switch))

class Machine(Product):
	def __init__(self, id, name):
		super().__init__(id, name)

	def run_game(self, game: Game):
		if not isinstance(self, game.support_platform):
			raise ValueError("This machine cannot play this game")
		return "Running Game"

class PC(Machine):
	def __init__(self, id):
		super().__init__(id, "PC")

class Playstation(Machine):
	def __init__(self, id):
		super().__init__(id, "Playstation")

class Switch(Machine):
	def __init__(self, id):
		super().__init__(id, "Switch")

class GameBoy(Machine):
	def __init__(self, id):
		super().__init__(id, "GameBoy")

# Stockerd, Selling, Solded, Renting
class ProductItemStatus(Enum):
	STOCKED = "Stocked"
	SELLING = "Selling"
	SOLDED = "Solded"
	RENTING = "Renting"

class ProductItem:
	def __init__(self, product: Product, sell_price: float):
		self.__serial_number: str = make_id("SE")
		self.__product: Product = product
		self.__status: ProductItemStatus = ProductItemStatus.STOCKED
		self.__sell_price: float = sell_price
		self.__condition: float = 1

	def get_product(self) -> Product:
		return self.__product
	
	product = property(get_product)

	@property
	def serial_number(self) -> str:
		return self.__serial_number
	@property
	def status(self) -> ProductItemStatus:
		return self.__status
	@status.setter
	def status(self, value: ProductItemStatus):
		self.__status = value
	@property
	def condition(self) -> float:
		return self.__condition

	def calculate_price(self) -> float:
		return self.__sell_price * self.__condition

class RoomStatusEnum(Enum):
	AVAILABLE = "Available"
	BEING_USE = "BeingUse"
	RESERVED = "Reserved"
	UNDER_MAINTAINACE = "UnderMaintainace"

class RoomTypeEnum(Enum):
	NORMAL = "Normal"
	VIP = "VIP"

class Room:
	def __init__(self, room_id: str, max_customer: int, rate_price: float):
		self.__room_id: str = room_id
		self.__max_customer: int = max_customer
		self.__rate_price: float = rate_price
		self.__room_type: RoomTypeEnum = RoomTypeEnum.NORMAL
		self.__status: RoomStatusEnum = RoomStatusEnum.AVAILABLE
		self.__product_item_list: list[ProductItem] = []
		self.__customer: Customer = None
		self.__reservation_list: list[Reservation] = []

	def get_room_id(self) -> str:
		return self.__room_id

	id = property(fget=get_room_id)

	def get_status(self) -> RoomStatusEnum:
		return self.__status

	def set_status(self, status: RoomStatusEnum):
		self.__status = status

	status = property(fget=get_status, fset=set_status)

	def get_rate_price(self) -> float:
		return self.__rate_price

	rate_price = property(get_rate_price)

	def get_reservation(self) -> list[Reservation]:
		return self.__reservation_list

	reservation = property(get_reservation)

	@property
	def customer(self) -> Customer:
		return self.__customer

	@customer.setter
	def customer(self, customer: Customer):
		self.__customer = customer

	def create_reservation(self, reservation_id: str, customer: Customer, start_time: datetime, end_time: datetime) -> "Reservation":
		if self.check_time_availability(start_time, end_time) == False:
			return None
		new_reservation = Reservation(reservation_id, customer, self, start_time, end_time)
		self.__reservation_list.append(new_reservation)
		return new_reservation

	def check_time_availability(
		self,
		start_time: datetime,
		end_time: datetime,
		exclude_reservation_id: str | None = None
	) -> bool:
		for reservation in self.__reservation_list:
			if exclude_reservation_id is not None and reservation.id == exclude_reservation_id:
				continue

			if (
				reservation.status != ReservationStatusEnum.CANCEL
				and start_time < reservation.end_time
				and end_time > reservation.start_time
			):
				return False
		return True

	def set_room_status(self, reservation: Reservation):
		self.__customer = reservation.customer

	def add_item(self, transfer: list[ProductItem]):
		for item in transfer:
			item.status = ProductItemStatus.RENTING
		self.__product_item_list.extend(transfer)

	def get_product_item_list(self) -> list[ProductItem]:
		return self.__product_item_list

	product_item_list = property(get_product_item_list)

	def clear_item(self):
		self.__product_item_list.clear()

class ReservationStatusEnum(Enum):
	PENDING = "Pending"
	SUCCESS = "Success"
	CANCEL = "Cancel"
	CHECK_IN = "CheckIn"
	CHECK_OUT = "CheckOut"


class Reservation:
	def __init__(self, reservation_id: str, customer: Customer, room: Room, start_time: datetime, end_time: datetime):
		self.__id: str = reservation_id
		self.__customer: Customer = customer
		self.__room: Room = room
		self.__status: ReservationStatusEnum = ReservationStatusEnum.PENDING
		self.__start_time: datetime = start_time
		self.__end_time: datetime = end_time

	def get_status(self) -> ReservationStatusEnum:
		return self.__status

	def set_status(self, status: ReservationStatusEnum):
		self.__status = status

	status = property(fget=get_status, fset=set_status)

	def get_id(self) -> str:
		return self.__id

	id = property(fget=get_id)

	def get_start_time(self) -> datetime:
		return self.__start_time

	def get_end_time(self) -> datetime:
		return self.__end_time
	
	start_time = property(get_start_time)
	end_time = property(get_end_time)

	@end_time.setter
	def end_time(self, value: datetime):
		self.__end_time = value

	def calculate_price(self) -> float:
		duration = self.__end_time - self.__start_time
		hours = duration.total_seconds() / 3600
		return hours * self.__room.rate_price
	
	@property
	def room(self) -> Room:
		return self.__room

	@property
	def customer(self) -> Customer:
		return self.__customer

class StockProduct:
	def __init__(self, product: Product, product_item_list: list[ProductItem] | None = None):
		self.__id: str = make_id('ST')
		self.__product: Product = product
		self.__product_item_list: list[ProductItem] = product_item_list if product_item_list is not None else []

	def get_product(self) -> Product:
		return self.__product

	product = property(get_product)

	def get_product_item_list(self) -> list[ProductItem]:
		return self.__product_item_list

	product_item_list = property(get_product_item_list)

	def get_id(self) -> str:
		return self.__id

	id = property(get_id)

	def refill_stock(self, quantity: int, sell_price: float):
		for i in range(quantity):
			new_product_item = ProductItem(self.__product, sell_price)
			self.__product_item_list.append(new_product_item)

	def take_product_items(self, quantity: int) -> list[ProductItem]:
		if quantity > len(self.__product_item_list):
			raise ValueError("Not enough product in stock")

		transfer = self.__product_item_list[:quantity]
		for item in transfer:
			self.__product_item_list.remove(item)

		return transfer

	def add_to_stock(self, transfer: list[ProductItem]):
		self.__product_item_list.extend(transfer)
		for product_item in self.__product_item_list:
			product_item.status = ProductItemStatus.STOCKED

class Shelf:
	def __init__(self, max_capacity: int):
		self.__id: str = make_id('SH')
		self.__max_capacity: int = max_capacity
		self.__product_on_shelf: list[ProductItem] = []

	def refill_shelf(self, product_item_list: list[ProductItem]):
		if len(self.__product_on_shelf) + len(product_item_list) > self.__max_capacity:
			raise ValueError("Exceed capacity")

		self.__product_on_shelf.extend(product_item_list)
		for product_item in product_item_list:
			product_item.status = ProductItemStatus.SELLING

	def get_id(self) -> str:
		return self.__id

	id = property(get_id)

	def get_product_on_shelf(self) -> list[ProductItem]:
		return self.__product_on_shelf

	product_on_shelf = property(get_product_on_shelf)

	def get_max_capacity(self) -> int:
		return self.__max_capacity

	max_capacity = property(get_max_capacity)

class Logs:
	def __init__(self, log_id: str):
		self.__log_id: str = log_id

class CustomerAction(Enum):
	CREATE_RESERVATION = "Create Reservation"
	SUBSCRIBE = "Subscribe"
	UNSUBSCRIBE = "Unsubscribe"
	PURCHASE = "Purchase"
	REFUND = "Refund"
	CANCEL_RESERVATION = "Cancel Reservation"
	CHECK_IN = "Check In"
	CHECK_OUT = "Check Out"
	EXTEND_TIME = "Extend Time"

class CustomerLogs(Logs):
	def __init__(self, log_id: str, customer: Customer, action: CustomerAction):
		super().__init__(log_id)
		self.__customer: Customer = customer
		self.__action: CustomerAction = action

class StaffAction(Enum):
	REFILL_SHELF = "RefillShelf"

class StaffLogs(Logs):
	def __init__(self, log_id: str, staff: Staff, action: StaffAction):
		super().__init__(log_id)
		self.__staff: Staff = staff
		self.__action: StaffAction = action

class ManagerAction(Enum):
	CREATE_GAME = "Create Game"
	CREATE_MACHINE = "Create Machine"
	REFILL_STOCK = "Refill Stock"
	CREATE_COUPON = "Create Coupon"

class ManagerLogs(StaffLogs):
	def __init__(self, log_id: str, manager: Manager, action: ManagerAction, target=None):
		super().__init__(log_id, manager, action)
		self.__target = target

class GameStore:
	def __init__(self, store_name: str):
		self.__store_id: str = make_id("S")
		self.__store_name: str = store_name

		self.__customer_list: list[Customer] = []
		self.__member_list: list[Member] = []
		self.__room_list: list[Room] = []
		self.__staff_list: list[Staff] = []
		self.__stock_product_list: list[StockProduct] = []
		self.__shelf_list: list[Shelf] = []
		self.__bought_list: list[ProductItem] = []

		self.__customer_logs_list: list[CustomerLogs] = []
		self.__staff_logs_list: list[StaffLogs] = []
		self.__bill_list: list[Bill] = []

		self.__payment_gateway_list: list[PaymentGateway] = [QRCode()]

	def create_customer(self, name: str, age: int) -> Customer:
		new_customer = Customer(make_id("C"), name, age)
		self.__customer_list.append(new_customer)
		return new_customer

	def create_member(self, customer: Customer) -> Member:
		new_member = Member(make_id('ME'), customer.id, customer.name, customer.age)
		self.__member_list.append(new_member)
		return new_member
	
	def create_manager(self, name: str, age: int) -> Manager:
		new_manager = Manager(make_id('MA'), name, age)
		self.__staff_list.append(new_manager)
		return new_manager

	def create_staff(self, name: str, age: int) -> Manager:
		new_staff = Staff(make_id('STA'), name, age)
		self.__staff_list.append(new_staff)
		return new_staff

	def create_room(self, max_customer: int, rate_price: float) -> Room:
		new_room = Room(make_id("RO"), max_customer, rate_price)
		self.__room_list.append(new_room)
		return new_room

	def get_available_room(self) -> list[Room]:
		return [room for room in self.__room_list if room.status == RoomStatusEnum.AVAILABLE]

	def get_all_customer(self) -> list[Customer]:
		return self.__customer_list

	def get_customer_by_id(self, customer_id: str) -> Customer | None:
		for customer in self.__customer_list:
			if customer.id == customer_id:
				return customer
		return None

	def get_room_by_id(self, room_id: str) -> Room | None:
		for room in self.__room_list:
			if room.id == room_id:
				return room
		return None
	
	def get_reservation_by_id(self, reservation_id: str) -> Reservation | None:
		for room in self.__room_list:
			for reservation in room.reservation:
				if reservation.id == reservation_id:
					return reservation
		return None

	def create_customer_logs(self, customer: Customer, action: CustomerAction, target=None) -> CustomerLogs:
		new_log = CustomerLogs(make_id(f"LC-{action}"), customer, action)
		self.__customer_logs_list.append(new_log)
		return new_log

	def create_staff_logs(self, staff: Staff, action: StaffAction, target=None) -> StaffLogs:
		new_log = StaffLogs(make_id(f'LS-{action}'), staff, action)
		self.__staff_logs_list.append(new_log)
		return new_log

	def create_manager_logs(self, manager: Manager, action: ManagerAction, target=None) -> ManagerLogs:
		new_log = ManagerLogs(make_id(f'LM-{action}'), manager, action, target)
		self.__staff_logs_list.append(new_log)
		return new_log

	def create_reservation(self, customer_id: str, room_id: str, start_time: datetime, end_time: datetime) -> str:
		customer = self.get_customer_by_id(customer_id)
		if customer is None:
			raise ValueError("Invalid User")

		room = self.get_room_by_id(room_id)
		if room is None:
			raise ValueError("No Room this ID")
		
		if customer.check_time_availability(start_time, end_time) == False:
			raise ValueError("Invalid Time Frame")

		reservation = room.create_reservation(make_id("RE"), customer, start_time, end_time)
		if reservation is None:
			raise ValueError("Invalid Time Frame")
		customer.add_reservation(reservation)
		self.create_customer_logs(customer, CustomerAction.CREATE_RESERVATION)
		return reservation.id

	def get_payment_gateway_by_name(self, payment_gateway_name: str) -> PaymentGateway | None:
		for payment_gateway in self.__payment_gateway_list:
			if payment_gateway.name == payment_gateway_name:
				return payment_gateway
		return None

	def create_bill(self, payment_gateway: PaymentGateway, amount: float) -> Bill:
		new_bill = Bill(payment_gateway, amount)
		self.__bill_list.append(new_bill)
		return new_bill

	def subscribe(self, customer_id: str, payment_gateway_name: str, payment_information: str) -> Member:
		SUBSCRIBE_PRICE = 500

		customer = self.get_customer_by_id(customer_id)
		if customer is None:
			raise ValueError("Customer not found")

		member = self.get_member_by_customer_id(customer_id)
		if member and member.status == MemberStatusEnum.ACTIVE:
			raise ValueError("Fail already be a member")

		payment_gateway = self.get_payment_gateway_by_name(payment_gateway_name)
		if payment_gateway is None:
			raise ValueError("Payment gateway not found")

		if not payment_gateway.start_payment(payment_information, SUBSCRIBE_PRICE):
			raise ValueError("Fail to payment")

		new_bill = self.create_bill(payment_gateway, SUBSCRIBE_PRICE)
		customer.add_bill(new_bill)

		if member:
			member.status = MemberStatusEnum.ACTIVE
			self.create_customer_logs(customer, CustomerAction.SUBSCRIBE)
			return member

		new_member = self.create_member(customer)
		self.create_customer_logs(customer, CustomerAction.SUBSCRIBE)
		return new_member

	def get_member_by_member_id(self, member_id: str) -> Member | None:
		for member in self.__member_list:
			if member.member_id == member_id:
				return member
		return None

	def get_member_by_customer_id(self, custoemr_id: str) -> Member | None:
		for member in self.__member_list:
			if member.id == custoemr_id:
				return member
		return None

	def get_manager_by_id(self, manager_id: str) -> Manager | None:
		for staff in self.__staff_list:
			if isinstance(staff, Manager):
				if staff.id == manager_id:
					return staff
		return None

	def get_staff_by_id(self, staff_id: str) -> Staff | None:
		for staff in self.__staff_list:
			if staff.id == staff_id:
				return staff
		return None

	def create_stock_product(self, product: Product, product_item_list: list[ProductItem] | None = None) -> StockProduct:
		new_stock_product = StockProduct(product, product_item_list)
		self.__stock_product_list.append(new_stock_product)
		return new_stock_product

	def create_game(self, manager_id: str, name: str, description: str, genre: str, game_type: str) -> Game:
		manager = self.get_manager_by_id(manager_id)
		if manager is None:
			raise ValueError("Not found manager")

		if game_type.upper() == "DISC":
			new_game = GameDisc(make_id('G'), name, description, genre)
		elif game_type.upper() == "KEYCARD":
			new_game = GameKeyCard(make_id('G'), name, description, genre)
		elif game_type.upper() == "CARTRIDGE":
			new_game = GameCartridge(make_id('G'), name, description, genre)
		else:
			raise ValueError("No this type of game available (Available type: DISC, KEYCARD, CARTRIDGE)")

		self.create_stock_product(new_game, [])
		self.create_manager_logs(manager, ManagerAction.CREATE_GAME)
		return new_game

	def create_machine(self, manager_id: str, name: str, machine_type: str) -> Machine:
		manager = self.get_manager_by_id(manager_id)
		if manager is None:
			raise ValueError("Not found manager")

		if machine_type.upper() == "PC":
			new_machine = PC(make_id('M'))
		elif machine_type.upper() == "PLAYSTATION":
			new_machine = Playstation(make_id('M'))
		elif machine_type.upper() == "GAMEBOY":
			new_machine = GameBoy(make_id('M'))
		elif machine_type.upper() == "SWITCH":
			new_machine = Switch(make_id('M'))
		else:
			raise ValueError("No this type of machine available (Available type: PC, PLAYSTATION, GAMEBOY, SWITCH)")

		self.create_stock_product(new_machine, [])
		self.create_manager_logs(manager, ManagerAction.CREATE_MACHINE)
		return new_machine

	def get_product_by_id(self, product_id: str) -> Product:
		for stock in self.__stock_product_list:
			if stock.product.id == product_id:
				return stock.product
		return None

	def cancel_reservation(self, customer_id: str, reservation_id: str) -> Reservation:
		customer = self.get_customer_by_id(customer_id)
		if customer is None:
			raise ValueError("Customer Not Found")

		reservation = customer.get_reservation_from_id(reservation_id)
		if reservation is None:
			raise ValueError("Reservaton Not Found")

		if reservation.status == ReservationStatusEnum.CANCEL:
			raise ValueError("Reservation is already cancel")
		reservation.status = ReservationStatusEnum.CANCEL

		new_log = self.create_customer_logs(customer, CustomerAction.CANCEL_RESERVATION)
		return reservation

	def unsubscribe(self, member_id: str):
		member = self.get_member_by_member_id(member_id)
		if member is None:
			raise ValueError("Member not found")

		if member.status == MemberStatusEnum.INACTIVE:
			raise ValueError("Member already inactive")

		member.status = MemberStatusEnum.INACTIVE
		self.create_customer_logs(member, CustomerAction.UNSUBSCRIBE)
		return "Success"

	def get_all_stock(self) -> list[StockProduct]:
		return self.__stock_product_list

	def get_stock_by_id(self, stock_id: str) -> StockProduct | None:
		for stock in self.__stock_product_list:
			if stock.id == stock_id:
				return stock
		return None

	def create_shelf(self, max_capacity: int) -> Shelf:
		new_shelf = Shelf(max_capacity)

		self.__shelf_list.append(new_shelf)
		return new_shelf

	def get_all_shelf(self) -> list[Shelf]:
		return self.__shelf_list

	def get_shelf_by_id(self, shelf_id: str) -> Shelf | None:
		for shelf in self.__shelf_list:
			if shelf.id == shelf_id:
				return shelf
		return None

	def refill_shelf(self, staff_id: str, shelf_id: str, stock_id: str, quantity: int) -> Shelf:
		staff = self.get_staff_by_id(staff_id)
		if not staff:
			raise ValueError("No staff found")

		shelf = self.get_shelf_by_id(shelf_id)
		if not shelf:
			raise ValueError("No shelf found")

		stock = self.get_stock_by_id(stock_id)
		if not stock:
			raise ValueError("No stock found")

		if len(shelf.product_on_shelf) + quantity > shelf.max_capacity:
			raise ValueError("Exceed capacity")

		transfer = stock.take_product_items(quantity)
		shelf.refill_shelf(transfer)

		self.create_staff_logs(staff, StaffAction.REFILL_SHELF)
		return shelf

	def refill_stock(self, manager_id : str, stock_id : str, quantity : int, sell_price: float) -> StockProduct:
		manager = self.get_manager_by_id(manager_id)
		if not manager:
			raise ValueError("Manager Not found")

		stock = self.get_stock_by_id(stock_id)
		if not stock:
			raise ValueError("Stock Not found")

		stock.refill_stock(quantity, sell_price)

		new_log = self.create_manager_logs(manager, ManagerAction.REFILL_STOCK, stock)
		return stock

	def check_in(self, customer_id: str, reservation_id: str) -> Reservation:
		customer = self.get_customer_by_id(customer_id)
		if not customer:
			raise ValueError("Customer not found")

		reservation = customer.get_reservation_from_id(reservation_id)
		if not reservation:
			raise ValueError("Reservation not found")

		room = reservation.room
		if not room:
			raise ValueError("Room not found")

		room.customer = reservation.customer
		reservation.status = ReservationStatusEnum.CHECK_IN

		log = CustomerLogs(make_id("LC-CHECK_IN"), customer, CustomerAction.CHECK_IN)
		self.__customer_logs_list.append(log)

		return reservation

	def check_out(self, customer_id: str, reservation_id: str) -> Reservation:
		customer = self.get_customer_by_id(customer_id)
		if not customer:
			raise ValueError("Customer not found")

		reservation = customer.get_reservation_from_id(reservation_id)
		if not reservation:
			raise ValueError("Reservation not found")

		if reservation.status != ReservationStatusEnum.CHECK_IN:
			raise ValueError("Reservation not checked in")

		room = reservation.room
		if room.customer != customer:
			raise ValueError("Invalid Customer")

		reservation.status = ReservationStatusEnum.CHECK_OUT
		room.customer = None

		self.clear_room(room)

		log = CustomerLogs(make_id("LC-CHECK_OUT"), customer, CustomerAction.CHECK_OUT)
		self.__customer_logs_list.append(log)

		return reservation

	def extend_time(self, customer_id: str, reservation_id: str, additional_hours: float) -> Reservation:
		customer = self.get_customer_by_id(customer_id)
		if not customer:
			raise ValueError("Customer not found")

		reservation = customer.get_reservation_from_id(reservation_id)
		if not reservation:
			raise ValueError("Reservation not found")

		if reservation.status != ReservationStatusEnum.CHECK_IN:
			raise ValueError("Reservation not checked in")

		if additional_hours <= 0:
			raise ValueError("Invalid additional hours")

		new_end_time = reservation.end_time + timedelta(hours=additional_hours)

		if not reservation.room.check_time_availability(
			reservation.start_time,
			new_end_time,
			exclude_reservation_id=reservation.id
		):
			raise ValueError("Room not available for extended time")

		reservation.end_time = new_end_time

		self.create_customer_logs(customer, CustomerAction.EXTEND_TIME)
		return reservation
	
	def create_coupon(self, manager_id: str, customer_id: str, minimum_amount: float, discount_amount: float, expire_date: datetime) -> Coupon:
		manager = self.get_manager_by_id(manager_id)
		if not manager:
			raise ValueError("Manager not found")

		customer = self.get_customer_by_id(customer_id)
		if not customer:
			raise ValueError("Customer not found")

		coupon_id = make_id("D-CP")
		coupon = Coupon(coupon_id, "coupon", customer, minimum_amount, discount_amount, expire_date)
		customer.add_coupon(coupon)

		self.create_manager_logs(manager, ManagerAction.CREATE_COUPON, coupon)

		return coupon

	def get_product_from_shelf(self, product_id: str) -> ProductItem:
		for shelf in self.get_all_shelf():
			for product_item in shelf.product_on_shelf:
				if product_item.product.id == product_id:
					return product_item
		return None

	def add_product_to_customer(self, customer_id : str, product_id : str):
		product_item = self.get_product_from_shelf(product_id)
		if product_item is None:
			raise Exception("No product with matching ID")

		customer_instance = self.get_customer_by_id(customer_id)
		cart: Cart = customer_instance.cart

		cart.products.append(CartItem(product_item))

		return cart
	
	def view_cart(self, customer_id : str) -> list[CartItem]:
		customer_instance = self.get_customer_by_id(customer_id)
		cart: Cart = customer_instance.cart
		return [item for item in cart.products]
	
	def remove_item_from_cart(self, customer_id: str, product_id: str) -> Cart:
		customer_instance = self.get_customer_by_id(customer_id)
		cart: Cart = customer_instance.cart
		for cartItem in cart.products:
			if cartItem.product_item.product.id == product_id:
				cart.products.remove(cartItem)
				break
		return cart
	
	def view_product_detail(self, serial_number: str) -> dict:
		product = self.get_product_by_id(serial_number)
		for stock in self.get_all_stock():
			for product_item in stock.product_item_list:
				if product_item.serial_number == serial_number:
					return {
						"status": product_item.status,
						"sell_price": product_item.calculate_price(),
						"condition": product_item.condition
					}
		return None
	
	def view_store(self) -> dict:
		return {
			"id": self.__store_id,
			"name": self.__store_name,
			"customers" : self.__customer_list,
			"members": self.__member_list,
			"rooms": self.__room_list,
			"staffs": self.__staff_list,
			"stock product list": self.__stock_product_list,
			"shelfs": self.__shelf_list,
			"customer logs": self.__customer_logs_list,
			"staff logs": self.__staff_logs_list,
			"bills": self.__bill_list,
			"payment gateways": self.__payment_gateway_list
		}

	def get_coupon_by_id(self, customer_id : str, coupon_id : str) -> Coupon:
		customer_instance = self.get_customer_by_id(customer_id)
		for coupon in customer_instance.coupons:
			if coupon_id == coupon.id:
				return coupon
		return None

	def purchase(self, customer_id : str, payment_method_name : str, payment_info : list, coupon_id: str = None) -> tuple[Bill, list[str]]:
		customer_instance = self.get_customer_by_id(customer_id)
		if not customer_instance:
			raise Exception("Customer doesn't exist")

		payment_method = self.get_payment_gateway_by_name(payment_method_name)
		if not payment_method:
			raise Exception("Payment method not found")

		cart_instance: Cart = customer_instance.cart
		cart_item_instances: list[CartItem] = cart_instance.products

		# Setting the buy product item list
		cart_items_given_to_customer: list[CartItem] = []
		for cart_item in cart_item_instances:
			if cart_item.is_buy:
				cart_items_given_to_customer.append(cart_item)

		# Check if stock does still have that instance
		for cart_item in cart_items_given_to_customer:
			if cart_item.product_item.status != ProductItemStatus.SELLING:
				raise Exception("Product is unavailable")
			
		# Pricing
		total_pricing = 0
		for cart_item in cart_items_given_to_customer:
			total_pricing += cart_item.product_item.calculate_price()
		total_pricing *= customer_instance.apply_discount_benefit()
		if coupon_id is not None:
			coupon_instance = self.get_coupon_by_id(customer_id, coupon_id)
			if datetime.now() >= coupon_instance.expire_date or total_pricing < coupon_instance.minimum_amount or coupon_instance is None:
				raise Exception("Error while applying coupon")
			total_pricing -= coupon_instance.discount_amount
			
		# Payment
		status = payment_method.start_payment(total_pricing, payment_info)
		if not status:
			raise Exception("Payment Failed.")

		# Changing the status of the product item stored in game store
		for cart_item in cart_items_given_to_customer:
			cart_item.product_item.status = ProductItemStatus.SOLDED

		# Remove product item from customer's cart
		for cart_item in cart_items_given_to_customer:
			cart_item_instances.remove(cart_item)

		bought_items = [cart_item.product_item for cart_item in cart_items_given_to_customer]

		bill = self.create_bill(payment_method, total_pricing)
		self.__bill_list.append(bill)
		bill.add_product_items(bought_items)
		self.__bought_list.extend(bought_items)
		customer_instance.add_bill(bill)

		customer_log = self.create_customer_logs(customer_instance, CustomerAction.PURCHASE)
		self.__customer_logs_list.append(customer_log)

		product_sn_list = [item.serial_number for item in bought_items]
		return [bill, product_sn_list]
	
	def get_product_item_by_serial_number(self, serial_number: str) -> ProductItem:
		for stock in self.__stock_product_list:
			for product_item in stock.product_item_list:
				if product_item.serial_number == serial_number:
					return product_item
		for shelf in self.__shelf_list:
			for product_item in shelf.product_on_shelf:
				if product_item.serial_number == serial_number:
					return product_item
		return None

	def get_bill_by_id(self, bill_id : str) -> Bill:
		for bill in self.__bill_list:
			if bill.id == bill_id:
				return bill
		return None
		

	def refund(self, customer_id : str, bill_id : str, product_sn_list: list[str]) -> Coupon:
		bill_instance : Bill = self.get_bill_by_id(bill_id)
		if bill_instance is None:
			raise Exception("Unable to find the bill instance")

		# Validate every serial was part of this specific bill
		bill_sn_set = {item.serial_number for item in bill_instance.product_items}
		invalid = [sn for sn in product_sn_list if sn not in bill_sn_set]
		if invalid:
			raise Exception(f"Serial numbers not found in this bill: {invalid}")

		product_items: list[ProductItem] = [self.get_product_item_by_serial_number(sn) for sn in product_sn_list]
		total_price = 0
		for product_item in product_items:
			total_price += product_item.calculate_price()
			if product_item.status != ProductItemStatus.SOLDED:
				raise Exception("Product is not sold")

		if bill_instance.amount != total_price:
			raise Exception("Not matching money amount")

		for product_item in product_items:
			product_item.status = ProductItemStatus.STOCKED

		customer_instance = self.get_customer_by_id(customer_id)
		log = self.create_customer_logs(customer_instance, CustomerAction.REFUND)
		self.__customer_logs_list.append(log)

		manager_id = None
		for staff in self.__staff_list:
			if isinstance(staff, Manager):
				manager_id = staff.id
				break
		coupon = self.create_coupon(manager_id, customer_id, 0, total_price, datetime.today() + timedelta(days=90))

		return coupon

	def get_stock_by_product_id(self, product_id: str) -> StockProduct:
		for stock in self.__stock_product_list:
			if stock.product.id == product_id:
				return stock

	def request_item_for_room(self, customer_id: str, reservation_id: str, product_id: str, quantity: int) -> Room:
		customer = self.get_customer_by_id(customer_id)
		if not customer:
			raise ValueError("Customer not found")

		reservation = customer.get_reservation_from_id(reservation_id)
		if not reservation:
			raise ValueError("Reservation not found")

		room = reservation.room
		if not room:
			raise ValueError("Room not found")

		stock = self.get_stock_by_product_id(product_id)

		if not stock:
			raise ValueError("Stock not found")

		if room.customer != customer:
			raise ValueError("Invalid Customer")

		transfer = stock.take_product_items(quantity)
		room.add_item(transfer)
		return room

	def clear_room(self, room: Room):
		for product_item in room.product_item_list:
			product_item: ProductItem = product_item
			stock = self.get_stock_by_product_id(product_item.product.id)
			stock.add_to_stock([product_item])

		room.clear_item()

	def get_stock_by_product_id(self, product_id: str) -> StockProduct:
		for stock in self.__stock_product_list:
			if stock.product.id == product_id:
				return stock

	def request_item_for_room(self, customer_id: str, reservation_id: str, product_id: str, quantity: int) -> Room:
		customer = self.get_customer_by_id(customer_id)
		if not customer:
			raise ValueError("Customer not found")

		reservation = customer.get_reservation_from_id(reservation_id)
		if not reservation:
			raise ValueError("Reservation not found")

		room = reservation.room
		if not room:
			raise ValueError("Room not found")

		stock = self.get_stock_by_product_id(product_id)

		if not stock:
			raise ValueError("Stock not found")

		if room.customer != customer:
			raise ValueError("Invalid Customer")

		transfer = stock.take_product_items(quantity)
		room.add_item(transfer)
		return room

	def clear_room(self, room: Room):
		for product_item in room.product_item_list:
			product_item: ProductItem = product_item
			stock = self.get_stock_by_product_id(product_item.product.id)
			stock.add_to_stock([product_item])

		room.clear_item()

	def set_cart_item_buy(self, customer_id: str, serial_number: str, is_buy: bool) -> ProductItem:
		customer = self.get_customer_by_id(customer_id)
		if not customer:
			raise Exception("Customer not found")

		for item in customer.cart.products:
			if item.product_item.serial_number == serial_number:
				item.is_buy = is_buy
				return item

		raise Exception("Item not found in cart")

class Bill:
	def __init__(self, payment_gateway: PaymentGateway, amount: float):
		super().__init__()
		self.__id: str = make_id('B')
		self.__timestamp: datetime = datetime.now()
		self.__payment_gateway: PaymentGateway = payment_gateway
		self.__amount: float = amount
		self.__product_items: list[ProductItem] = []

	@property
	def id(self) -> str:
		return self.__id

	@property
	def amount(self) -> float:
		return self.__amount

	@property
	def product_items(self) -> list[ProductItem]:
		return self.__product_items

	def add_product_items(self, items: list[ProductItem]):
		self.__product_items.extend(items)


class PaymentGateway(ABC):
	def __init__(self, name: str):
		super().__init__()
		self.__id: str = make_id('P')
		self.__name: str = name
		self.__status: str = "Active"

	@abstractmethod
	def authenticate():
		pass

	@abstractmethod
	def pay():
		pass

	@abstractmethod
	def start_payment():
		pass

	def get_name(self) -> str:
		return self.__name

	name = property(get_name)

# QRCode
class QRCode(PaymentGateway):
	def __init__(self):
		super().__init__("QRCode")

	def authenticate(self, payment_information) -> bool:
		return True

	def pay(self, amount) -> bool:
		return True

	def start_payment(self, payment_information, amount) -> bool:
		if not self.authenticate(payment_information):
			return False
		if not self.pay(amount):
			return False
		return True

class Coupon():
	def __init__(self, id: str, type: str, owner: Customer, minimum_amount: float, discount_amount: float, expire_date: datetime):
		self.__id: str = id
		self.__type: str = type
		self.__owner: Customer = owner
		self.__minimum_amount: float = minimum_amount
		self.__discount_amount: float = discount_amount
		self.__expire_date: datetime = expire_date

	@property
	def id(self):
		return self.__id

	@property
	def type(self):
		return self.__type

	@property
	def minimum_amount(self):
		return self.__minimum_amount

	@property
	def discount_amount(self):
		return self.__discount_amount

	@property
	def expire_date(self):
		return self.__expire_date
