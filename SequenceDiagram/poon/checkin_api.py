from fastapi import FastAPI
from checkin_class import GameStore, Customer, Reservation, Room, Staff
import uvicorn

app = FastAPI()

store = GameStore("Microslop Store")

# Test
store.add_staff("S1")
store.add_staff("S2")
store.add_staff("S3")

@app.get("/")
def test_connection():
    return {"message": "Hello World"}

@app.post("/create_customer")
def create_customer(Name: str):
    customer = store.add_customer(Name)
    return {"customer_id": customer.id}

@app.get("/get_all_customers")
def get_all_customers():
    customers = store.get_all_customers()
    return [{"customer_id": c.id} for c in customers]

@app.post("/create_room")
def create_room(room_type: str, max_customer: int, price: float):
    room = store.add_room(room_type, max_customer, price)
    return {"room_id": room.id}

@app.get("/available_rooms")
def get_available_rooms():
    available = store.get_available_rooms()
    return [{"room_id": r.id} for r in available]

@app.post("/create_reservation")
def create_reservation(customer_id: str, room_id: str):
    try:
        reservation = store.create_reservation(customer_id, room_id)
        return {"reservation_id": reservation.id}
    except Exception as e:
        raise Exception(str(e))

@app.get("/check_reservation")
def check_reservation(customer_id: str):
    customer = store.get_customer_by_id(customer_id)
    if not customer or not customer.reservation:
        raise Exception("No reservation found")
    return {"reservation_id": customer.reservation.id}

@app.post("/check_in")
def check_in(customer_id: str, reservation_id: str):
    result = store.check_in(customer_id, reservation_id)
    if result != "CheckIn successful":
        raise Exception(result)
    return {"message": result}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)