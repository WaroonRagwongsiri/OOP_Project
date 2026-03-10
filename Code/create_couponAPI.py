from fastapi import FastAPI
from create_couponClass import GameStore, Log, Customer, Manager, Coupon
import uvicorn

app = FastAPI()

store = GameStore("Microslop Store")

# Test
store.add_manager("John")
store.add_customer("Bob")

@app.get("/")
def test_connection():
    return {"message": "Hello World"}

@app.post("/create_customer")
def create_customer(Name: str):
    customer = store.add_customer(Name)
    return {"customer_name": customer.name, "customer_id": customer.id}

@app.post("/create_manager")
def create_manager(Name: str):
    manager = store.add_manager(Name)
    return {"manager_name": manager.name, "manager_id": manager.id}

@app.get("/get_all_managers_and_customers")
def get_all_managers_and_customers():
    managers = store.get_all_managers()
    customers = store.get_all_customers()
    return {
        "managers": [{"manager_name": m.name, "manager_id": m.id} for m in managers],
        "customers": [{"customer_name": c.name, "customer_id": c.id} for c in customers]
    }

@app.post("/create_coupon")
def create_coupon(manager_id: str, customer_id: str, minimum_amount: float, discount_amount: float, expire_date: str):
    result = store.create_coupon(manager_id, customer_id, minimum_amount, discount_amount, expire_date)
    return {"result": result}

@app.post("/check_coupon")
def check_coupon(customer_id: str):
    customer = store.get_customer_by_id(customer_id)
    if not customer:
        return {"error": "Customer not found"}
    
    coupons = []
    for coupon in customer.coupons:
        coupons.append({
            "coupon_id": coupon.id,
            "type": coupon.type,
            "minimum_amount": coupon.minimum_amount,
            "discount_amount": coupon.discount_amount,
            "expire_date": coupon.expire_date
        })
    return {"coupons": coupons}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)