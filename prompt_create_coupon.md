🧪 create_coupon Test Suite

⚙️ Setup (Prerequisites)

Call create_manager with name="ManagerMike", age=40 → save manager_id
Call create_customer with name="Alice", age=25 → save customer_id


✅ Happy Path
Test 1 – Valid coupon creation
Call create_coupon with:
manager_id={manager_id}, customer_id={customer_id}, minimum_amount=10.0, discount_amount=5.0, expire_date="2027-01-01T00:00:00"
→ Expect: coupon object returned, save as coupon_id
→ Expect: returned coupon has minimum_amount=10.0, discount_amount=5.0, expire_date="2027-01-01T00:00:00"
→ Expect: coupon is associated with Alice (i.e. appears in her coupon list)

❌ Fail Cases
Test 2 – Invalid manager_id (non-existent manager)
Call create_coupon with:
manager_id="INVALID_MANAGER_ID", customer_id={customer_id}, minimum_amount=10.0, discount_amount=5.0, expire_date="2027-01-01T00:00:00"
→ Expect: "Error: Manager not found"
(from: if not manager → raise ValueError("Manager not found"))

Test 3 – Invalid customer_id (non-existent customer)
Call create_coupon with:
manager_id={manager_id}, customer_id="INVALID_CUSTOMER_ID", minimum_amount=10.0, discount_amount=5.0, expire_date="2027-01-01T00:00:00"
→ Expect: "Error: Customer not found"
(from: if not customer → raise ValueError("Customer not found"))

Test 4 – Expired expire_date (date in the past)
Call create_coupon with:
manager_id={manager_id}, customer_id={customer_id}, minimum_amount=10.0, discount_amount=5.0, expire_date="2020-01-01T00:00:00"
→ Expect: "Error: ..." or coupon created (verify whether the system rejects past expiry dates)
(no guard exists in the current snippet — flag if past dates are silently accepted)

Test 5 – minimum_amount of zero or negative value
Call create_coupon with:
manager_id={manager_id}, customer_id={customer_id}, minimum_amount=0.0, discount_amount=5.0, expire_date="2027-01-01T00:00:00"
→ Expect: "Error: ..." or coupon created (verify whether zero/negative minimums are guarded)
(no guard exists in the current snippet — flag if minimum_amount <= 0 is silently allowed)

Test 6 – discount_amount of zero or negative value
Call create_coupon with:
manager_id={manager_id}, customer_id={customer_id}, minimum_amount=10.0, discount_amount=0.0, expire_date="2027-01-01T00:00:00"
→ Expect: "Error: ..." or coupon created (verify whether zero/negative discounts are guarded)
(no guard exists in the current snippet — flag if discount_amount <= 0 is silently allowed)