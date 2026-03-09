GameStore MCP — Test Case Prompts
TC-01 · Connection Check

```
Use the test_connection tool and confirm the service is reachable.
```

TC-02 · Create Manager

```
Create a manager named "Alice" who is 35 years old. Save the returned manager ID for later use.
```

TC-03 · Create Customers

```
Create two customers:
1. Name: "Bob", Age: 22
2. Name: "Carol", Age: 17

Save both customer IDs for later steps.
```

TC-04 · List All Customers

```
Retrieve all customers and display their id, name, and age.
```

TC-05 · Create Game Products

```
Using the manager ID from TC-02, create the following games:
1. Name: "Elden Ring", Description: "Open world RPG", Genre: "RPG", Type: "DISC"
2. Name: "Minecraft", Description: "Sandbox survival game", Genre: "Sandbox", Type: "KEYCARD"
3. Name: "Mario Kart", Description: "Racing game", Genre: "Racing", Type: "CARTRIDGE"

Save all returned game IDs.
```

TC-06 · Create Gaming Machine

```
Using the manager ID from TC-02, create a gaming machine named "PlayStation 5" with machine_type "PLAYSTATION".
Save the returned machine ID.
```

TC-07 · Create Rooms

```
Create two game rooms:
1. max_customer: 4, rate_price: 150.0
2. max_customer: 2, rate_price: 80.0

Save both room IDs.
```

TC-08 · List Available Rooms

```
Retrieve all available rooms and show their id and status.
```

TC-09 · Create Reservation & Cancel It

```
Step 1: Using the customer ID from TC-03 (Bob) and the first room ID from TC-07,
create a reservation with:
  - start_time: 2026-03-10T10:00:00
  - end_time:   2026-03-10T12:00:00

Step 2: After the reservation is created, cancel it using Bob's customer ID and the reservation ID returned in Step 1.
Confirm the reservation status after cancellation.
```

TC-10 · Subscribe & Unsubscribe

```
Step 1: Subscribe the customer "Bob" (from TC-03) using:
  - payment_gateway_name: "QRCode"
  - payment_information: "tok_visa_test_001"

Step 2: After subscribing, unsubscribe using the member_id returned in Step 1.
Confirm the result message.
```

TC-11 · Stock Management

```
Step 1: Get all current stocks using get_all_stocks.

Step 2: Using the manager ID from TC-02, refill the stock for the first stock entry found with:
  - quantity: 10
  - sell_price: 1990.0

Show the stock_id and product_name after refilling.
```

TC-12 · Shelf Management

```
Step 1: Create a shelf with max_capacity: 20. Save the shelf ID.

Step 2: List all shelves using get_all_shelves.

Step 3: Using the manager ID from TC-02 as staff_id, refill the shelf from TC-12 Step 1
using the stock_id from TC-11, with quantity: 5.
Confirm the shelf ID in the response.
```

TC-13 · Shopping Cart Flow

```
Step 1: Add the game "Elden Ring" (product_id from TC-05) to Bob's cart (customer_id from TC-03).

Step 2: View Bob's cart and list all items including product_name, serial_number, and is_buy.

Step 3: View the product detail for the first serial_number shown in the cart.

Step 4: Remove "Elden Ring" from Bob's cart.

Step 5: View Bob's cart again to confirm the item was removed and total_items decreased.
```

TC-14 · Full End-to-End Flow

```
Run a complete GameStore scenario in sequence:
1. test_connection — confirm service is up
2. create_manager — "Manager Dan", age 40
3. create_customer — "Eve", age 25
4. create_game — using Dan's manager ID: "God of War", "Action RPG", "RPG", "DISC"
5. get_all_stocks — find the stock ID for "God of War"
6. refill_stock — 5 units at price 2500.0 using Dan's manager ID
7. create_shelf — max_capacity 10
8. refill_shelf — move 3 units from stock to shelf using Dan as staff
9. add_product_to_customer — add "God of War" to Eve's cart
10. view_cart — show Eve's cart
11. view_product_detail — for the first serial_number in the cart
12. remove_item_from_cart — remove "God of War" from Eve's cart
13. subscribe — Eve subscribes via "PayPalGateway", info: "paypal_ref_abc"
14. unsubscribe — using the member_id from step 13

Report the result of every step clearly.
```