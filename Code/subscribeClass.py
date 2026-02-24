from __future__ import annotations

from datetime import datetime
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
		self.__reservation_list: list[Reservation] = []
		self.__bill_list: list[Bill] = []

	def get_customer_id(self):
		return self.__customer_id

	def get_reservation_list(self):
		return self.__reservation_list

	def add_reservation(self, reservation: "Reservation"):
		self.__reservation_list.append(reservation)

	reservation_list = property(fget=get_reservation_list)
	id = property(fget=get_customer_id)

	def check_time_availability(self, start_time: datetime, end_time: datetime) -> bool:
		for reservation in self.__reservation_list:
			if start_time < reservation.end_time and end_time > reservation.start_time:
				return False
		return True

	def get_reservation_from_id(self, reservation_id: str) -> Reservation:
		for reservation in self.__reservation_list:
			if reservation.id == reservation_id:
				return reservation
		return None

	def add_bill(self, bill: Bill):
		self.__bill_list.append(bill)

	def get_name(self):
		return self.__name

	def get_age(self):
		return self.__age
	
	name = property(get_name)
	age = property(get_age)

class Member(Customer):
	def __init__(self, member_id: str, customer_id: str, name: str, age: int):
		super().__init__(customer_id, name, age)
		self.__member_id = member_id
		self.__expire_date: datetime = datetime.today()

	def get_member_id(self):
		return self.__member_id

	member_id = property(get_member_id)


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
		self.__reservation_list: list[Reservation] = []

	def get_room_id(self) -> str:
		return self.__room_id

	id = property(fget=get_room_id)

	def get_status(self) -> RoomStatusEnum:
		return self.__status

	status = property(fget=get_status)

	def create_reservation(self, reservation_id: str, customer: Customer, start_time: datetime, end_time: datetime) -> "Reservation":
		if self.check_time_availability(start_time, end_time) == False:
			return None
		new_reservation = Reservation(reservation_id, customer, self, start_time, end_time)
		self.__reservation_list.append(new_reservation)
		return new_reservation

	def check_time_availability(self, start_time: datetime, end_time: datetime) -> bool:
		for reservation in self.__reservation_list:
			if start_time < reservation.end_time and end_time > reservation.start_time:
				return False
		return True


class ReservationStatusEnum(Enum):
	PENDING = "Pending"
	SUCCESS = "Success"
	CANCEL = "CANCEL"


class Reservation:
	def __init__(self, reservation_id: str, customer: Customer, room: Room, start_time: datetime, end_time: datetime):
		self.__id: str = reservation_id
		self.__customer: Customer = customer
		self.__room: Room = room
		self.__status: ReservationStatusEnum = ReservationStatusEnum.PENDING
		self.__start_time: datetime = start_time
		self.__end_time: datetime = end_time

	def get_status(self):
		return self.__status

	def set_status(self, status: ReservationStatusEnum):
		self.__status = status

	status = property(fget=get_status, fset=set_status)

	def get_id(self):
		return self.__id

	id = property(fget=get_id)

	def get_start_time(self):
		return self.__start_time

	def get_end_time(self):
		return self.__end_time
	
	start_time = property(get_start_time)
	end_time = property(get_end_time)

class Logs:
	def __init__(self, transaction_id: str):
		self.__transaction_id: str = transaction_id

class CustomerAction(Enum):
	CREATE_RESERVATION = "Create Reservation"
	SUBSCRIBE = "Subscribe"

class CustomerLogs(Logs):
	def __init__(self, transaction_id: str, customer: Customer, action: CustomerAction):
		super().__init__(transaction_id)
		self.__customer: Customer = customer
		self.__action: CustomerAction = action

class GameStore:
	def __init__(self, store_name: str):
		self.__store_id: str = make_id("S")
		self.__store_name: str = store_name
		self.__customer_list: list[Customer] = []
		self.__room_list: list[Room] = []
		self.__customer_logs_list: list[CustomerLogs] = []
		self.__bill_list: list[Bill] = []
		self.__member_list: list[Member] = []
		self.__payment_gateway_list: list[PaymentGateway] = [QRCode()]

	def create_customer(self, name: str, age: int) -> Customer:
		new_customer = Customer(make_id("C"), name, age)
		self.__customer_list.append(new_customer)
		return new_customer

	def create_member(self, customer: Customer) -> Member:
		new_member = Member(make_id('M'), customer.id, customer.name, customer.age)
		self.__member_list.append(new_member)
		return new_member

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

	def create_customer_logs(self, customer: Customer, action: CustomerAction) -> Logs:
		new_log = CustomerLogs(make_id(f"LC-{action}"), customer, action)
		self.__customer_list.append(new_log)
		return new_log

	def create_booking(self, customer_id: str, room_id: str, start_time: datetime, end_time: datetime) -> str:
		customer = self.get_customer_by_id(customer_id)
		if customer is None:
			raise ValueError("Invalid User")
		
		if customer.check_time_availability(start_time, end_time) == False:
			raise ValueError("Invalid Time Frame")

		room = self.get_room_by_id(room_id)
		if room is None:
			raise ValueError("No Room this ID")

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

	def subscribe(self, customer_id: str, payment_gateway_name: str, payment_information: str):
		SUBSCRIBE_PRICE = 500
		customer = self.get_customer_by_id(customer_id)
		payment_gateway = self.get_payment_gateway_by_name(payment_gateway_name)
		if not payment_gateway.start_transaction(payment_information, SUBSCRIBE_PRICE):
			raise ValueError("Fail to create")
		new_bill = self.create_bill(payment_gateway, SUBSCRIBE_PRICE)
		customer.add_bill(new_bill)
		new_member = self.create_member(customer)
		log = self.create_customer_logs(customer, CustomerAction.SUBSCRIBE)
		return new_member.member_id
	
	def get_member_by_id(self, member_id: str) -> Member | None:
		for member in self.__member_list:
			if member.member_id == member_id:
				return member
		return None


class Bill:
	def __init__(self, payment_gateway: PaymentGateway, amount: float):
		super().__init__()
		self.__id: str = make_id('B')
		self.__timestamp: datetime = datetime.now()
		self.__payment_gateway: PaymentGateway = payment_gateway
		self.__amount: float = amount

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
	def start_transaction():
		pass

	def get_name(self):
		return self.__name

	name = property(get_name)

# QRCode
class QRCode(PaymentGateway):
	def __init__(self):
		super().__init__("QRCode")

	def authenticate(self, payment_information) -> bool:
		return True

	def pay(self, amount):
		return True

	def start_transaction(self, payment_information, amount):
		if not self.authenticate(payment_information):
			return False
		if not self.pay(amount):
			return False
		return True