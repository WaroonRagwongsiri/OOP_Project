Execute the following scenario step by step using MCP tools.  
Always call the appropriate MCP tool when possible and clearly show the result.

--------------------------------
Phase 0 : Setup Environment
--------------------------------

1. Create a Manager
   name: ManagerOne
   age: 30

2. ManagerOne creates 3 rooms

Room 1
capacity: 20
price: 150

Room 2
capacity: 50
price: 700

Room 3
capacity: 30
price: 300

3. Create two customers

Customer 1
name: Bob
age: 25

Customer 2
name: Alice
age: 22

--------------------------------
Phase 1 : Prepare Reservation
--------------------------------

1. Bob views all available rooms.

2. Bob makes two reservations

Reservation A
room capacity: 50
date: 19 March
time: 10:00 - 18:00

Reservation B
room capacity: 30
date: 19 March
time: 20:00 - 22:00

3. Bob views all his reservations and remember the reservation IDs.

--------------------------------
Phase 2 : Good Test (Check In Success)
--------------------------------

1. Bob checks in with Reservation A.

Expected Result
- reservation status becomes CHECK_IN
- room.customer is set to Bob
- system returns success message

2. Bob checks in with Reservation B.

Expected Result
- reservation status becomes CHECK_IN
- room.customer is set to Bob
- check in success

--------------------------------
Phase 3 : Bad Test (Error Handling)
--------------------------------

1. Bob tries to check in using a reservation ID that does not exist.

Expected Result
- system returns error
- "Reservation not found"

2. Alice tries to check in using Bob's reservation ID.

Expected Result
- system returns error
- reservation does not belong to Alice

3. Unknown customer tries to check in

customer_id: Mamba
reservation_id: Reservation A

Expected Result
- system returns error
- "Customer not found"

4. Bob tries to check in again with Reservation A (already checked in)

Expected Result
- system returns error
- reservation already checked in

--------------------------------
Testing Rules
--------------------------------

- Always use MCP tools when available
- Show the response returned by the system
- Clearly label each step
- If an error occurs, explain why the system rejected the request