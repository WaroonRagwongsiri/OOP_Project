import datetime
import uuid
from enum import Enum

class Staff:
    def __init__(self, name : str, store : "GameStore"):
        self.__id : uuid.UUID = uuid.uuid4()
        self.__name : str = name
        self.__store : "GameStore" = store

    @property
    def id(self):
        return self.__id

class Manager(Staff):
    def __init__(self, name : str, store : "GameStore"):
        super.__init__(name, store)

class GameStore:
    def __init__(self, store_name : str, stock : list["ProductItem"] = [], staffs : list[Staff]= []):
        self.__store_name : str = store_name
        self.__stock : "StockProduct" = stock
        self.__staff : list [Staff] = staffs
        self.__logs : list["Log"] = []
    
    @property
    def stock(self):
        return self.__stock
    
    def order_product(self, managerID : str, productID : str, quantity : int):
        managerUUID = uuid.UUID(managerID)
        managerInstance = None
        for staff in self.__staff:
            if staff.id == managerUUID:
                managerInstance = staff
        if not staff:
            raise Exception("Unable to find manager")

        productUUID = uuid.UUID(productID)
        productInstance = None
        for staff in self.__staff:
            if staff.id == managerUUID:
                productInstance = staff
        if not staff:
            raise Exception("Unable to find manager")

class Product:
    def __init__(self, name : str, sell_price : int):
        self.__id : uuid.UUID = uuid.uuid4()
        self.__name : str = name
        self.__sell_price : int = sell_price

    @property
    def id(self):
        return self.__id

class ProductItem:
    def __init__(self, product : Product, serial_number : str, condition : str):
        self.__product : Product = product
        self.__serial_number : str = serial_number
        self.__condition : str = condition

    @property
    def id(self):
        return self.__id
    
    @property
    def sn(self):
        return self.__sn
    
    @property
    def price(self):
        return self.__price

class StockProduct:
    def __init__(self, product : Product, product_item_list : list[ProductItem] = []):
        self.__product : Product = product
        self.__product_item_list : list[ProductItem] = product_item_list

    @property
    def product(self):
        return self.__product
    
    @property
    def product_item_list(self):
        return self.__product_item_list

class Log:
    def __init__(self):
        self.__id : uuid.UUID = uuid.uuid4()

class StaffLogAction(Enum):
    CHECK_IN = 0
    CHECK_OUT = 1
    REFILL_SHELF = 2

class ManagerLogAction(StaffLogAction):
    ORDER_PRODUCT = 3

class StaffLog(Log):
    def __init__(self, actor : Staff, action : StaffLogAction):
        super().__init__()
        self.__actor = actor
        self.__action = action