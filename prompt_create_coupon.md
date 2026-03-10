Execute the following scenario step by step using MCP tools. Always call the appropriate MCP tool when possible and clearly show the result.

-------------------------------- Phase 0 : Setup Environment --------------------------------

Create a Manager — name: ManagerOne, age: 30

Create two customers
Customer 1 — name: Bob, age: 25
Customer 2 — name: Alice, age: 22

Remember all generated IDs because they will be used in the next steps.

-------------------------------- Phase 1 : Good Test (Create Coupon Success) --------------------------------

ManagerOne creates a coupon for Bob — minimum_amount: 500, discount_amount: 100, expire_date: 31 December 2027
Expected Result — Coupon is created successfully; Coupon is assigned to Bob; System returns coupon information including coupon id, type, minimum_amount, discount_amount, expire_date

ManagerOne creates another coupon for Alice — minimum_amount: 1000, discount_amount: 250, expire_date: 31 December 2027
Expected Result — Coupon created successfully; Coupon belongs to Alice

-------------------------------- Phase 2 : Bad Test (Error Handling) --------------------------------

ManagerOne tries to create a coupon with invalid minimum amount — minimum_amount: -500, discount_amount: 100, expire_date: 31 December 2027
Expected Result — system returns error; "Invalid minimum amount"

ManagerOne tries to create a coupon with invalid discount amount — minimum_amount: 500, discount_amount: -100, expire_date: 31 December 2027
Expected Result — system returns error; "Invalid discount amount"

ManagerOne tries to create a coupon with expire date in the past — minimum_amount: 500, discount_amount: 100, expire_date: 1 January 2020
Expected Result — system returns error; "Invalid Expire date"

Unknown manager tries to create coupon — manager_id: Mamba, customer_id: Bob, minimum_amount: 500, discount_amount: 100, expire_date: 31 December 2027
Expected Result — system returns error; "Manager not found"

ManagerOne tries to create coupon for customer that does not exist — manager_id: ManagerOne, customer_id: Ghost, minimum_amount: 500, discount_amount: 100, expire_date: 31 December 2027
Expected Result — system returns error; "Customer not found"
