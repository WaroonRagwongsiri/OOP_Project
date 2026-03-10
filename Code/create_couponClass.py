from abc import ABC, abstractmethod
from datetime import datetime
import uuid

def generate_id(prefix=""):
    return f"{prefix}-{str(uuid.uuid4())[:4]}"

class GameStore:
    def __init__(self, store_name):
        self.__store_name = store_name
        self.__store_id = generate_id("S")
        self.__customer_list = []
        self.__manager_list = []
        self.__log_list = []

    def get_customer_by_id(self, customer_id):
        for customer in self.__customer_list:
            if customer._Customer__customer_id == customer_id:
                return customer
        return None
    
    def get_manager_by_id(self, manager_id):
        for manager in self.__manager_list:
            if manager._Manager__manager_id == manager_id:
                return manager
        return None
    
    def create_coupon(self, manager_id, customer_id, minimum_amount, discount_amount, expire_date):
        manager = self.get_manager_by_id(manager_id)
        if not manager:
            return "Manager not found"
        
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return "Customer not found"
        
        coupon_id = generate_id("CP")
        coupon = Coupon(coupon_id, "coupon", customer, minimum_amount, discount_amount, expire_date)
        customer.coupons.append(coupon)
        
        log = Log.create_log(manager, coupon)
        self.__log_list.append(log)
        
        return "Coupon created successfully"
    
    def add_coupon(self, customer_id, coupon):
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return "Customer not found"
        
        customer.coupons.append(coupon)
        return "Coupon added to customer successfully"

    def add_customer(self, name):
        customer = Customer(name, generate_id("C"))
        self.__customer_list.append(customer)
        return customer

    def get_all_customers(self):
        return self.__customer_list

    def add_manager(self, name):
        manager = Manager(name, generate_id("M"))
        self.__manager_list.append(manager)
        return manager
    
    def get_all_managers(self):
        return self.__manager_list
    
class Discount(ABC):
    def __init__(self, id, type, owner, minimum_amount, discount_amount, expire_date):
        self.__id = id
        self.__type = type
        self.__owner = owner
        self.__minimum_amount = minimum_amount
        self.__discount_amount = discount_amount
        self.__expire_date = expire_date
    
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
    
class Coupon(Discount):
    def __init__(self, id, type, owner, minimum_amount, discount_amount, expire_date):
        super().__init__(id, type, owner, minimum_amount, discount_amount, expire_date)

class Log:
    def __init__(self, log_id, log_type, manager, coupon):
        self.__log_id = log_id
        self.__log_type = log_type
        self.__manager = manager
        self.__coupon = coupon
        
    @staticmethod
    def create_log(manager, coupon):
        log_id = generate_id("L")
        log_type = "create_coupon"
        return Log(log_id, log_type, manager, coupon)

class Customer:
    def __init__(self, name, customer_id):
        self.__customer_name = name
        self.__customer_id = customer_id
        self.__coupon_list = []

    @property
    def id(self):
        return self.__customer_id
    
    @property
    def name(self):
        return self.__customer_name
    
    @property
    def coupons(self):
        return self.__coupon_list
    
class Manager:
    def __init__(self, name, manager_id):
        self.__manager_name = name
        self.__manager_id = manager_id

    @property
    def id(self):
        return self.__manager_id
    
    @property
    def name(self):
        return self.__manager_name
