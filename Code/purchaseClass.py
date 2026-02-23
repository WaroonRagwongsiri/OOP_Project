import datetime
import uuid

class Customer:
    def __init__(self, id : str):
        self.__id : str = id
        self.__cart : "Cart" = Cart()
        self.__transactions : list["Bill"] = []

    @property
    def id(self):
        return self.__id
    
    @property
    def product_in_cart(self):
        return self.__cart.products
    
    @property
    def transactions(self):
        return self.__transactions
    
    def add_prodcut_to_cart(self, product_instance : "ProductItem"):
        self.product_in_cart.append(product_instance)
        return self.product_in_cart

    def select_product(self, product_id : str):
        select_list = []
        for product in self.product_in_cart:
            if product.id == product_id:
                product.is_selected = not product.is_selected
                select_list.append(product)
        return select_list

class GameStore:
    def __init__(self, store_name : str, payment_list : list["PaymentMethod"], customers : list[Customer] = [], stock : list["ProductItem"] = []):
        self.__store_name : str = store_name
        self.__payment_methods : list["PaymentMethod"] = payment_list
        self.__customers : list[Customer] = customers
        self.__stock : list["ProductItem"] = stock
        self.__logs : list["Log"] = []
        self.__transactions : list["Bill"] = []

    @property
    def customers(self):
        return self.__customers
    
    @property
    def stock(self):
        return self.__stock

    def search_product(self, product_id : str):
        found_product = []
        for product in self.__stock:
            if product.id == product_id:
                found_product.append(product)
        return found_product

    def create_customer(self, id : str):
        for customer in self.__customers:
            if customer.id == id:
                raise Exception("Customer already exist.")
        new_customer = Customer(id)
        self.__customers.append(new_customer)
        return new_customer

    def search_customer(self, customer_id : str):
        for customer in self.__customers:
            if customer.id == customer_id:
                return customer

    def add_product_to_customer(self, customer_id : str, product_id : str):
        found_product = self.search_product(product_id)
        available_product = [x for x in found_product if not x.is_selected]
        customer_instance = self.search_customer(customer_id)
        cart_product_ids = [x.id for x in customer_instance.product_in_cart]
        return customer_instance.add_prodcut_to_cart(available_product[cart_product_ids.count(product_id)])

    def add_product(self, product_id : str, product_sn : str, product_price : int):
        new_product = ProductItem(product_id, product_sn, product_price)
        self.__stock.append(new_product)
        return new_product

    def purchase(self, customer_id : str, payment_method_name : str, payment_info : list):
        customer_instance = self.search_customer(customer_id)
        if not customer_instance:
            raise Exception("Customer doesn't exist")

        payment_method = None
        for method in self.__payment_methods:
            if method.name == payment_method_name:
                payment_method = method
        if not payment_method:
            raise Exception("Payment method not found")

        cart_product_instances = customer_instance.product_in_cart

        # Check if stock does still have that instance
        for product_instance in cart_product_instances:
            if product_instance.is_selected and (not product_instance in self.__stock):
                raise Exception("Store already sold that product")
            
        # Payment
        total_pricing = 0
        for product_instance in cart_product_instances:
            if product_instance.is_selected:
                total_pricing += product_instance.price
        status = payment_method.create_transaction(total_pricing, payment_info)
        if not status:
            raise Exception("Payment Failed.")

        # Giving the customer their product
        products_given_to_customer = []
        for product_instances in cart_product_instances:
            if product_instance.is_selected:
                products_given_to_customer.append(product_instances)
                self.__stock.remove(product_instances)
        
        for product in products_given_to_customer:
            cart_product_instances.remove(product)

        transaction = Bill(self.__payment_methods, total_pricing, products_given_to_customer)
        self.__transactions.append(transaction)
        customer_instance.transactions.append(transaction)

        log = Log(customer_instance, "Purchase")
        self.__logs.append(log)

        product_sn_list = [product.sn for product in products_given_to_customer]
        return [transaction, product_sn_list]

class Cart:
    def __init__(self, products : list["ProductItem"] = []):
        self.__products : list["ProductItem"] = products

    @property
    def products(self):
        return self.__products

class ProductItem:
    def __init__(self, id : str, sn : str, price : int):
        self.__id : str = id
        self.__sn : str = sn
        self.__is_selected : bool = False
        self.__price : int = price

    @property
    def id(self):
        return self.__id
    
    @property
    def sn(self):
        return self.__sn
    
    @property
    def is_selected(self):
        return self.__is_selected
    @is_selected.setter
    def is_selected(self, value : bool):
        self.__is_selected = value

    @property
    def price(self):
        return self.__price

class PaymentMethod:
    def __init__(self, name : str):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def create_transaction(self, total : int, payment_info : list):
        return True

class Log:
    def __init__(self, customer : Customer, action : str):
        self.__customer = customer
        self.__action = action

    @property
    def data(self):
        return [self.__customer, self.__action]
    
class Bill:
    def __init__(self, payment_method : PaymentMethod, amount : float, product_item_list):
        self.__id = uuid.uuid4()
        self.__timestamp = datetime.datetime.now()
        self.__payment_method = payment_method
        self.__amount = amount
        self.__product_item_list = product_item_list

    @property
    def data(self):
        return [self.__id, self.__timestamp, self.__payment_method, self.__amount, self.__product_item_list]