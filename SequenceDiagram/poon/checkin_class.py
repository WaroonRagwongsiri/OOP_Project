
def generate_id():
    return "example_id"

class GameStore:
    def __init__(self, store_name):
        self.__store_name = store_name
        self.__store_id = generate_id()
        self.__customer_list = []
        self.__room_list = []
        self.__transaction_list = []
        self.__staff_list = []

    def find_available_staff(self):
        for staff in self.__staff_list:
            if not staff.is_busy():
                return staff
        return None

    def get_customer(self, customer_id):
        for customer in self.__customer_list:
            if customer._Customer__customer_id == customer_id:
                return customer
        return None

    def get_available_rooms(self):
        return [room for room in self.__room_list if not room.is_occupied()]

    def check_in(self, customer_id):
        customer = self.get_customer(customer_id)
        if not customer:
            return "Customer not found"
        
        reservation = customer.get_pending_reservation()
        if not reservation:
            return "No pending reservation found"
        
        room = reservation._Reservation__room
        if not room or room.is_occupied():
            return "Room not available"
        
        staff = self.find_available_staff()
        if not staff:
            return "No staff available"
        
        reservation._Reservation__staff = staff
        staff.set_busy(True)
        
        room.set_room_status(reservation)
        reservation.set_status("checked_in")
        
        transaction = Transaction.create_transaction(customer, reservation)
        self.__transaction_list.append(transaction)
        
        return "CheckIn successful"

    def add_customer(self, customer_id):
        customer = Customer(customer_id)
        self.__customer_list.append(customer)
        return customer

    def get_all_customers(self):
        return self.__customer_list

    def add_room(self, room_id, room_type, max_customer, price):
        room = Room(room_id, room_type, max_customer, price)
        self.__room_list.append(room)
        return room

    def add_staff(self, staff_id):
        staff = Staff(staff_id)
        self.__staff_list.append(staff)
        return staff

    def create_reservation(self, customer_id, room_id):
        customer = self.get_customer(customer_id)
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
        
        reservation = Reservation.check_in(customer, None)
        reservation._Reservation__room = room
        customer.add_reservation(reservation)
        return reservation

class Transaction:
    def __init__(self, transaction_id, type, customer, room, checkin_date, checkout_date):
        self.__transaction_id = transaction_id
        self.__transaction_type = type
        self.__customer = customer
        self.__room = room
        self.__checkin_date = checkin_date
        self.__checkout_date = checkout_date

    @staticmethod
    def create_transaction(customer, reservation):
        transaction_id = generate_id()
        transaction_type = "checkin"
        room = reservation._Reservation__room
        checkin_date = reservation._Reservation__checkin_date
        checkout_date = reservation._Reservation__checkout_date
        return Transaction(transaction_id, transaction_type, customer, room, checkin_date, checkout_date)

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
    def __init__(self, reservation_id, customer, room, checkin_date, checkout_date, staff=None):
        self.__reservation_id = reservation_id
        self.__customer = customer
        self.__room = room
        self.__checkin_date = checkin_date
        self.__checkout_date = checkout_date
        self.__staff = staff
        self.__status = "pending"

    @property
    def id(self):
        return self.__reservation_id

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    @staticmethod
    def check_in(customer, staff):
        reservation_id = generate_id()
        checkin_date = "09-02-2026"
        checkout_date = "10-02-2026"
        return Reservation(reservation_id, customer, None, checkin_date, checkout_date, staff)

class Customer:
    def __init__(self, customer_id):
        self.__customer_id = customer_id
        self.__reservation_list = []
        self.reservation = None

    @property
    def id(self):
        return self.__customer_id

    def add_reservation(self, reservation):
        self.__reservation_list.append(reservation)
        self.reservation = reservation

    def get_pending_reservation(self):
        for reservation in self.__reservation_list:
            if reservation.get_status() == "pending":
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