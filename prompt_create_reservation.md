🧪 create_reservation Test Suite

⚙️ Setup (Prerequisites)

Call create_customer with name="Alice", age=25 → save customer_id Call create_room with max_customer=4, rate_price=100.0 → save room_id

✅ Happy Path

Test 1 – Valid reservation Call create_reservation with:





customer_id={customer_id}, room_id={room_id}



start_time="2026-03-10T10:00:00", end_time="2026-03-10T12:00:00"

→ Expect: reservation object returned, save as reservation_id

❌ Fail Cases

Test 2 – Invalid customer_id (non-existent customer) Call create_reservation with:





customer_id="INVALID_ID", room_id={room_id}



start_time="2026-03-10T10:00:00", end_time="2026-03-10T12:00:00"

→ Expect: "Error: Invalid User"

Test 3 – Invalid room_id (non-existent room) Call create_reservation with:





customer_id={customer_id}, room_id="INVALID_ROOM"



start_time="2026-03-10T10:00:00", end_time="2026-03-10T12:00:00"

→ Expect: "Error: No Room this ID"

Test 4 – Overlapping time (customer already has a reservation in this window) (Uses reservation_id from Test 1 — same customer, overlapping time) Call create_reservation with:





customer_id={customer_id}, room_id={room_id}



start_time="2026-03-10T11:00:00", end_time="2026-03-10T13:00:00" (overlaps with Test 1)

→ Expect: "Error: Invalid Time Frame" (from customer.check_time_availability)

Test 5 – Room already booked in that time window Call create_reservation with a different valid customer (customer_id_2) but same room and same time as Test 1:





customer_id={customer_id_2}, room_id={room_id}



start_time="2026-03-10T10:00:00", end_time="2026-03-10T12:00:00"

→ Expect: "Error: Invalid Time Frame" (from room.create_reservation returning None)