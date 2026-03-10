ช่วยทดสอบการเชื่อมต่อกับร้านค้าให้หน่อย

สร้างลูกค้าชื่อ Alice อายุ 25 และผู้จัดการชื่อ ManagerMike อายุ 40
ManagerMike ต้องการสร้างเกมชื่อ Chess มีรายระเอียดคือ Classic strategy game มีแนวเป็น Strategy ระบุให้มีชนิดเป็นแผ่นเกม



```
🛒 Purchase Function Test Prompt
Prerequisites (run first to get required IDs):
1. `test_connection` → verify connection
2. `create_customer` name="Alice", age=25 → save `customer_id`
3. `create_manager` name="ManagerMike", age=40 → save `manager_id`
4. `create_game` manager_id={manager_id}, name="Chess", description="Classic strategy game", genre="Strategy", game_type="DISC" → save `game_id`
5. `get_all_stocks` → save `stock_id`
6. `refill_stock` manager_id={manager_id}, stock_id={stock_id}, quantity=10, sell_price=29.99
7. `create_shelf` max_capacity=5 → save `shelf_id`
8. `refill_shelf` staff_id=any, shelf_id={shelf_id}, stock_id={stock_id}, quantity=3
9. `add_product_to_cart` customer_id={customer_id}, product_id={game_id}
10. `view_cart` customer_id={customer_id} → save `serial_number`
11. `set_cart_item_buy` customer_id={customer_id}, serial_number={serial_number}, is_buy=true
✅ Happy Path Tests:
* `purchase` customer_id={customer_id}, payment_method_name="QRCode", payment_information=["500"], coupon_id=null → expect `bill_id` and `product_serials` returned
* (With coupon) `create_coupon` manager_id={manager_id}, customer_id={customer_id}, minimum_amount=10.0, discount_amount=5.0, expire_date="2020-01-01T00:00:00" → save `coupon_id`; re-add product, mark is_buy=true, then `purchase` with coupon_id={coupon_id} → expect discounted bill
❌ Error / Edge Case Tests:
* `purchase` with invalid customer_id → expect `"Error: Customer doesn't exist"`
* `purchase` with invalid payment_method_name (e.g. "CASH") → expect `"Error: Payment method not found"`
* `purchase` with empty cart (no items marked is_buy=true) → expect empty bill or zero total
* `purchase` with an expired coupon (expire_date in the past) → expect `"Error: Error while applying coupon"`
* `purchase` with a coupon where total < minimum_amount → expect `"Error: Error while applying coupon"`
* `purchase` the same product twice (already SOLDED status) → expect `"Error: Product is unavailable"`

🛒 Purchase Function Test Prompt
Prerequisites (run first to get required IDs):
1. `test_connection` → verify connection
2. `create_customer` name="Alice", age=25 → save `customer_id`
3. `create_manager` name="ManagerMike", age=40 → save `manager_id`
4. `create_game` manager_id={manager_id}, name="Chess", description="Classic strategy game", genre="Strategy", game_type="DISC" → save `game_id`
5. `get_all_stocks` → save `stock_id`
6. `refill_stock` manager_id={manager_id}, stock_id={stock_id}, quantity=10, sell_price=29.99
7. `create_shelf` max_capacity=5 → save `shelf_id`
8. `refill_shelf` staff_id=any, shelf_id={shelf_id}, stock_id={stock_id}, quantity=3
9. `add_product_to_cart` customer_id={customer_id}, product_id={game_id}
10. `view_cart` customer_id={customer_id} → save `serial_number`
11. `set_cart_item_buy` customer_id={customer_id}, serial_number={serial_number}, is_buy=true
✅ Happy Path Tests:
* `purchase` customer_id={customer_id}, payment_method_name="QRCode", payment_information=["500"], coupon_id=null → expect `bill_id` and `product_serials` returned
* (With coupon) `create_coupon` manager_id={manager_id}, customer_id={customer_id}, minimum_amount=10.0, discount_amount=5.0, expire_date="2020-01-01T00:00:00" → save `coupon_id`; re-add product, mark is_buy=true, then `purchase` with coupon_id={coupon_id} → expect discounted bill
❌ Error / Edge Case Tests:
* `purchase` with invalid customer_id → expect `"Error: Customer doesn't exist"`
* `purchase` with invalid payment_method_name (e.g. "CASH") → expect `"Error: Payment method not found"`
* `purchase` with empty cart (no items marked is_buy=true) → expect empty bill or zero total
* `purchase` with an expired coupon (expire_date in the past) → expect `"Error: Error while applying coupon"`
* `purchase` with a coupon where total < minimum_amount → expect `"Error: Error while applying coupon"`
* `purchase` the same product twice (already SOLDED status) → expect `"Error: Product is unavailable"`

🛒 Purchase Function Test Prompt
Prerequisites (run first to get required IDs):
1. `test_connection` → verify connection
2. `create_customer` name="Alice", age=25 → save `customer_id`
3. `create_manager` name="ManagerMike", age=40 → save `manager_id`
4. `create_game` manager_id={manager_id}, name="Chess", description="Classic strategy game", genre="Strategy", game_type="DISC" → save `game_id`
5. `get_all_stocks` → save `stock_id`
6. `refill_stock` manager_id={manager_id}, stock_id={stock_id}, quantity=10, sell_price=29.99
7. `create_shelf` max_capacity=5 → save `shelf_id`
8. `refill_shelf` staff_id=any, shelf_id={shelf_id}, stock_id={stock_id}, quantity=3
9. `add_product_to_cart` customer_id={customer_id}, product_id={game_id}
10. `view_cart` customer_id={customer_id} → save `serial_number`
11. `set_cart_item_buy` customer_id={customer_id}, serial_number={serial_number}, is_buy=true
✅ Happy Path Tests:
* `purchase` customer_id={customer_id}, payment_method_name="QRCode", payment_information=["500"], coupon_id=null → expect `bill_id` and `product_serials` returned
* (With coupon) `create_coupon` manager_id={manager_id}, customer_id={customer_id}, minimum_amount=10.0, discount_amount=5.0, expire_date="2020-01-01T00:00:00" → save `coupon_id`; re-add product, mark is_buy=true, then `purchase` with coupon_id={coupon_id} → expect discounted bill
❌ Error / Edge Case Tests:
* `purchase` with invalid customer_id → expect `"Error: Customer doesn't exist"`
* `purchase` with invalid payment_method_name (e.g. "CASH") → expect `"Error: Payment method not found"`
* `purchase` with empty cart (no items marked is_buy=true) → expect empty bill or zero total
* `purchase` with an expired coupon (expire_date in the past) → expect `"Error: Error while applying coupon"`
* `purchase` with a coupon where total < minimum_amount → expect `"Error: Error while applying coupon"`
* `purchase` the same product twice (already SOLDED status) → expect `"Error: Product is unavailable"`
```