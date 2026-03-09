🧪 check_in Test Suite

⚙️ Setup (Prerequisites)

Call create_customer with name="Alice", age=25 → save customer_id
Call create_room with max_customer=4, rate_price=100.0 → save room_id
Call create_reservation with customer_id={customer_id}, room_id={room_id}, start_time="2026-03-10T10:00:00", end_time="2026-03-10T12:00:00" → save reservation_id


✅ Happy Path
Test 1 – Valid check-in
Call check_in with:
customer_id={customer_id}, reservation_id={reservation_id}
→ Expect: reservation object returned with status == CHECK_IN
→ Expect: room.customer is now set to Alice's customer object

❌ Fail Cases
Test 2 – Invalid customer_id (non-existent customer)
Call check_in with:
customer_id="INVALID_ID", reservation_id={reservation_id}
→ Expect: "Error: Customer not found"
(from: if not customer → raise ValueError("Customer not found"))

Test 3 – Invalid reservation_id (non-existent reservation)
Call check_in with:
customer_id={customer_id}, reservation_id="INVALID_RESERVATION_ID"
→ Expect: "Error: Reservation not found"
(from: if not reservation → raise ValueError("Reservation not found"))

Test 4 – Reservation belongs to a different customer
Create a second customer: create_customer(name="Bob", age=30) → save customer_id_2
Call check_in with:
customer_id={customer_id_2}, reservation_id={reservation_id} (reservation_id belongs to Alice, not Bob)
→ Expect: "Error: Reservation not found"
(from: customer.get_reservation_from_id returns None when the reservation doesn't belong to that customer)

Test 5 – Room not attached to reservation
(If your system supports creating a reservation with no room, or room is detached)
Call check_in with a reservation_id that has no associated room:
customer_id={customer_id}, reservation_id={reservation_id_no_room}
→ Expect: "Error: Room not found"
(from: if not room → raise ValueError("Room not found"))

Test 6 – Double check-in (already checked in)
(Uses reservation_id from Test 1, which already has status == CHECK_IN)
Call check_in again with:
customer_id={customer_id}, reservation_id={reservation_id}
→ Expect: "Error: ..." or idempotent behavior depending on implementation
(verify whether the system guards against re-checking-in an already active reservation)