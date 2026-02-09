from fastapi import FastAPI
from purchaseClass import *

app = FastAPI()

store_payment = PaymentMethod()
store = GameStore("Stream", store_payment)

@app.get("/")
def connection():
    return "SDIYBT"



@app.get("/customer_list")
def customer_list():
    return store.customers

@app.post("/create_customer")
def create_customer(id : str):
    return store.create_customer(id)

@app.post("/add_product_to_cart")
def add_product_to_cart(customer_id : str, product_id : str):
    return store.search_customer(customer_id).add_prodcut_to_cart(product_id)

@app.post("/select_product")
def select_product(customer_id : str, product_id : str):
    return store.search_customer(customer_id).select_product(product_id)



@app.get("/list_stock")
def list_stock():
    return store.stock

@app.post("/add_product_to_store")
def add_product_to_store(product_id : str, product_sn : str, product_price : int):
    return store.add_product(product_id, product_sn, product_price)



@app.post("/purchase")
def purchase(customer_id : str):
    return store.purchase(customer_id)