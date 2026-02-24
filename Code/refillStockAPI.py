from fastapi import FastAPI
from refillStockClass import *

app = FastAPI()

product = Product("ROBLOX", 100)
stockProduct = StockProduct(product)
store = GameStore("Stream", [stockProduct])

@app.get("/")
def connection():
    return "SDIYBT"

@app.get("/stock_product_list")
def list_manager():
    return store.stock_product_list

@app.get("/manager_list")
def list_manager():
    return store.managers

@app.post("/create_manager")
def create_manager(name : str):
    return store.create_manager(name)

@app.post("/refill_stock")
def refill_stock(manager_id : str, product_id : str, quantity : int):
    return store.refill_stock(manager_id, product_id, quantity)