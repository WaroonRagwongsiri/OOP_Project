from fastapi import FastAPI
from purchaseClass import *

app = FastAPI()

store_payment = [PaymentMethod("QR")]
store = GameStore("Stream", store_payment)

@app.get("/")
def connection():
    return "SDIYBT"