from datetime import datetime
import uuid

def generate_id(prefix=""):
    return f"{prefix}-{str(uuid.uuid4())[:4]}"

class GameStore:
    def __init__(self, store_name):
        self.__store_name = store_name
        self.__store_id = generate_id("S")
        self.__customer_list = []
        self.__room_list = []
        self.__log_list = []
        self.__staff_list = []

    def find_available_staff(self):
        for staff in self.__staff_list:
            if not staff.is_busy():
                return staff
        return None

    def get_customer_by_id(self, customer_id):
        for customer in self.__customer_list:
            if customer._Customer__customer_id == customer_id:
                return customer
        return None

    def get_available_rooms(self):
        return [room for room in self.__room_list if not room.is_occupied()]

    def check_in(self, customer_id, reservation_id):
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return "Customer not found"
        
        reservation = customer.get_reservation_by_id(reservation_id)
        if not reservation:
            return "Reservation not found"
        
        room = reservation._Reservation__room
        if not room or room.is_occupied():
            return "Room not available"
        
        staff = self.find_available_staff()
        if not staff:
            return "No staff available"
        
        staff.set_busy(True)
        
        room.set_room_status(reservation)
        reservation.check_in(staff)
        
        log = Log.create_log(customer, reservation)
        self.__log_list.append(log)
        
        return "CheckIn successful"

    def add_customer(self, name):
        customer = Customer(name, generate_id("C"))
        self.__customer_list.append(customer)
        return customer

    def get_all_customers(self):
        return self.__customer_list

    def add_room(self, room_type, max_customer, price):
        room = Room(generate_id("R"), room_type, max_customer, price)
        self.__room_list.append(room)
        return room

    def add_staff(self, staff_id):
        staff = Staff(staff_id)
        self.__staff_list.append(staff)
        return staff

    def create_reservation(self, customer_id, room_id):
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise Exception("Customer not found")
        
        room = None
        for r in self.__room_list:
            if r.id == room_id:
                room = r
                break
        if not room:
            raise Exception("Room not found")
        
        if room.is_occupied():
            raise Exception("Room not available")
        
        reservation = Reservation(generate_id("E"), customer, room, None, None, None)
        customer.add_reservation(reservation)
        return reservation

class Log:
    def __init__(self, log_id, log_type, customer, room, checkin_date, checkout_date):
        self.__log_id = log_id
        self.__log_type = log_type
        self.__customer = customer
        self.__room = room
        self.__checkin_date = checkin_date
        self.__checkout_date = checkout_date

    @staticmethod
    def create_log(customer, reservation):
        log_id = generate_id("L")
        log_type = "checkin"
        room = reservation._Reservation__room
        checkin_date = reservation._Reservation__checkin_date
        checkout_date = reservation._Reservation__checkout_date
        return Log(log_id, log_type, customer, room, checkin_date, checkout_date)

class Room:
    def __init__(self, room_id, room_type, max_customer, price):
        self.__room_id = room_id
        self.__room_type = room_type
        self.__max_customer = max_customer
        self.__price = price
        self.__reservation: Reservation| None = None

    @property
    def id(self):
        return self.__room_id

    def is_occupied(self):
        return self.__reservation is not None

    def set_room_status(self, reservation):
        self.__reservation = reservation

class Reservation:
    def __init__(self, reservation_id, customer, room, staff, checkin_date, checkout_date):
        self.__reservation_id = reservation_id
        self.__customer = customer
        self.__room = room
        self.__staff = staff
        self.__checkin_date = checkin_date
        self.__checkout_date = checkout_date
        self.__status = "pending"

    @property
    def id(self):
        return self.__reservation_id

    def set_status(self, status):
        self.__status = status

    def get_status(self):
        return self.__status
    
    def check_in(self, staff):
        self.__checkin_date = datetime.now()
        self.__staff = staff
        self.set_status("checked_in")

class Customer:
    def __init__(self, name, customer_id):
        self.__customer_name = name
        self.__customer_id = customer_id
        self.__reservation_list = []
        self.reservation = None

    @property
    def id(self):
        return self.__customer_id

    def add_reservation(self, reservation):
        self.__reservation_list.append(reservation)
        self.reservation = reservation

    def get_reservation_by_id(self, reservation_id):
        for reservation in self.__reservation_list:
            if reservation.id == reservation_id:
                return reservation
        return None

class Staff:
    def __init__(self, staff_id):
        self.__staff_id = staff_id
        self.__busy = False

    def is_busy(self):
        return self.__busy

    def set_busy(self, busy):
        self.__busy = busy