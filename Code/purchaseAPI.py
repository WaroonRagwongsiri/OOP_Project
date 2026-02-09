from fastapi import FastAPI
from purchaseClass import *

app = FastAPI()

store_payment = [PaymentMethod("QR")]
store = GameStore("Stream", store_payment)

@app.get("/")
def connection():
    return "SDIYBT"

<<<<<<< HEAD
<<<<<<< HEAD


=======
>>>>>>> 38fd179 (purchase stuff)
=======


>>>>>>> 7274d8b (add finish purchase stuff)
@app.get("/customer_list")
def customer_list():
    return store.customers

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 7274d8b (add finish purchase stuff)
@app.post("/create_customer")
def create_customer(name : str):
    return store.create_customer(name)

<<<<<<< HEAD
=======
>>>>>>> 38fd179 (purchase stuff)
=======
>>>>>>> 7274d8b (add finish purchase stuff)
@app.post("/add_product_to_cart")
def add_product_to_cart(customer_id : str, product_id : str):
    return store.add_product_to_customer(customer_id, product_id)

@app.post("/select_product")
def select_product(customer_id : str, product_id : str):
    return store.search_customer(customer_id).select_product(product_id)



<<<<<<< HEAD
<<<<<<< HEAD
=======
@app.post("/create_customer")
def create_customer(id : str):
    return store.create_customer(id)

>>>>>>> 38fd179 (purchase stuff)
=======
>>>>>>> 7274d8b (add finish purchase stuff)
@app.get("/list_stock")
def list_stock():
    return store.stock

@app.post("/add_product_to_store")
def add_product_to_store(product_id : str, product_sn : str, product_price : int):
    return store.add_product(product_id, product_sn, product_price)

<<<<<<< HEAD
<<<<<<< HEAD


=======
>>>>>>> 38fd179 (purchase stuff)
=======


>>>>>>> 7274d8b (add finish purchase stuff)
@app.post("/purchase")
def purchase(customer_id : str, payment_method_name : str):
    return store.purchase(customer_id, payment_method_name, [])