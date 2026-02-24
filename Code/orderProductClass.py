import datetime
import uuid
from enum import Enum

class Staff:
    def __init__(self, name : str):
        self.__id : uuid.UUID = uuid.uuid4()
        self.__name : str = name
    @property
    def id(self):
        return self.__id

class Manager(Staff):
    def __init__(self, name : str):
        super().__init__(name)

class GameStore:
    def __init__(self, store_name : str, stock_product_list : list["StockProduct"] = [], staffs : list[Staff]= []):
        self.__store_name : str = store_name
        self.__stock_product_list : list["StockProduct"] = stock_product_list
        self.__staff : list [Staff] = staffs
        self.__logs : list["Log"] = []
    
    @property
    def stock_product_list(self):
        return self.__stock_product_list

    @property
    def managers(self):
        manager_list = []
        for staff in self.__staff:
            if isinstance(staff, Manager):
                manager_list.append(staff)
        return manager_list

    def order_product(self, manager_id : str, product_id : str, quantity : int):
        manager_uuid = uuid.UUID(manager_id)
        manager_instance = None
        for staff in self.__staff:
            if staff.id == manager_uuid:
                manager_instance = staff
        if not manager_instance:
            raise Exception("Unable to find manager")

        product_uuid = uuid.UUID(product_id)
        stock_product_instance = None
        for stock_product in self.__stock_product_list:
            if stock_product.product.id == product_uuid:
                stock_product_instance = stock_product
        if not stock_product_instance:
            raise Exception("Product isn't available in store")

        for _ in range(quantity):
            new_product_item_instance = ProductItem(stock_product_instance.product)
            stock_product_instance.product_item_list.append(new_product_item_instance)

        log = StaffLog(manager_instance, StaffLogAction.ORDER_PRODUCT)
        self.__logs.append(log)
        return stock_product_instance
    
    def create_manager(self, name : str):
        new_manager = Manager(name)
        self.__staff.append(new_manager)
        return new_manager

class Product:
    def __init__(self, name : str, sell_price : int):
        self.__id : uuid.UUID = uuid.uuid4()
        self.__name : str = name
        self.__sell_price : int = sell_price

    @property
    def id(self):
        return self.__id

class ProductItem:
    def __init__(self, product : Product):
        self.__product : Product = product
        self.__serial_number : uuid.UUID = uuid.uuid4()
    
    @property
    def serial_number(self):
        return self.__serial_number

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
    ORDER_PRODUCT = 3

class StaffLog(Log):
    def __init__(self, actor : Staff, action : StaffLogAction):
        super().__init__()
        self.__actor = actor
        self.__action = action