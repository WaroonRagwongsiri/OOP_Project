class Customer:
    def __init__(self, id : str):
        self.__id : str = id
        self.__cart : "Cart" = Cart()
        self.__histories : list["History"] = None

    @property
    def id(self):
        return self.__id
    
    @property
    def product_in_cart(self):
        return self.__cart.products

    @property
    def selected_product(self):
        return self.__cart.selected_product
    
    def add_prodcut_to_cart(self, product_id : str):
        self.product_in_cart.append(product_id)
        return self.product_in_cart

    def select_product(self, product_id : str):
        if product_id not in self.selected_product:
            self.selected_product.append(product_id)
        return self.selected_product

class GameStore:
    def __init__(self, store_name : str, payment : "PaymentMethod", customers : list[Customer] = [], stock : list["ProductItem"] = []):
        self.__store_name : str = store_name
        self.__payment : "PaymentMethod" = payment
        self.__customers : list[Customer] = customers
        self.__stock : list["ProductItem"] = stock

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

    def add_product(self, product_id : str, product_sn : str, product_price : int):
        new_product = ProductItem(product_id, product_sn, product_price)
        self.__stock.append(new_product)
        return new_product

    def purchase(self, customer_id : str):
        customer_instance = self.search_customer(customer_id)
        if not customer_instance:
            raise Exception("Customer doesn't exist in store.")
        
        selected_products_id = customer_instance.selected_product

        # Get stock of each product that user selected
        selected_products_stock_instances = [self.search_product(id) for id in selected_products_id]

        for product_id in selected_products_id:
            product_stock_count = 0
            for stock_products in selected_products_stock_instances:
                if len(stock_products) > 0 and stock_products[0].id == product_id:
                    product_stock_count = len(stock_products)
                    break

            if product_stock_count < selected_products_id.count(product_id):
                raise Exception("Store doesn't have this / enough product.")
            
        total_pricing = 0
        for products in selected_products_stock_instances:
            total_pricing += (products[0].price * selected_products_id.count(products[0].id))
        status = self.__payment.create_transaction(total_pricing)
        if not status:
            raise Exception("Payment Failed.")

        products_given_to_customer = []
        for products in selected_products_stock_instances:
            remove_count = selected_products_id.count(products[0].id)
            for i in range(remove_count):
                products_given_to_customer.append(products[i])
                self.__stock.remove(products[i])

        history = History(products_given_to_customer, total_pricing)

        product_sn_list = [product.sn for product in products_given_to_customer]
        return [history, product_sn_list]

class Cart:
    def __init__(self, products : list["ProductItem"] = [], selected_products : list["ProductItem"] = []):
        self.__products : list["ProductItem"] = products
        self.__selected_product : list["ProductItem"] = selected_products

    @property
    def products(self):
        return self.__products
    
    @property
    def selected_product(self):
        return self.__selected_product

class ProductItem:
    def __init__(self, id : str, sn : str, price : int):
        self.__id : str = id
        self.__sn : str = sn
        self.__price : int = price

    @property
    def id(self):
        return self.__id
    
    @property
    def sn(self):
        return self.__sn
    
    @property
    def price(self):
        return self.__price

class PaymentMethod:
    def __init__(self):
        pass

    def create_transaction(self, total : int):
        return True

class History:
    def __init__(self, products : list[ProductItem], total_price : int):
        self.__products = products
        self.__total_price = total_price

    @property
    def data(self):
        return [self.__products, self.__total_price]