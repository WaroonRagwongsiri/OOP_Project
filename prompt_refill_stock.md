📦 Refill Stock Function – Test Prompt
Phase Setup (Prerequisites)

Call test_connection → expect {"message": "Hello World"}
Call create_manager with name="ManagerMike", age=40 → save manager_id
Call create_game with manager_id={manager_id}, name="Chess", description="Classic strategy game", genre="Strategy", game_type="DISC" → save game_id
Call get_all_stocks → save a valid stock_id from the list


✅ Happy Path Tests
Test 1 – Basic refill
Call refill_stock with manager_id={manager_id}, stock_id={stock_id}, quantity=10, sell_price=29.99
→ Expect: returns updated StockProduct object
→ Expect: stock quantity increases by 10
→ Expect: sell_price is updated to 29.99
→ Expect: a REFILL_STOCK manager log entry is created
Test 2 – Refill with quantity=1 (minimum valid)
Call refill_stock with quantity=1, sell_price=9.99
→ Expect: stock quantity increases by 1
→ Expect: success with updated stock returned
Test 3 – Refill with a high quantity
Call refill_stock with quantity=9999, sell_price=49.99
→ Expect: stock quantity increases by 9999 without error
Test 4 – Refill updates sell_price correctly
Call refill_stock twice with different sell_price values (e.g. 19.99 then 39.99)
→ Expect: second call's sell_price=39.99 is reflected in the stock

❌ Error / Edge Case Tests
Test 5 – Invalid manager ID
Call refill_stock with manager_id="nonexistent_id", valid stock_id, quantity=10, sell_price=29.99
→ Expect: ValueError("Manager Not found")
Test 6 – Invalid stock ID
Call refill_stock with valid manager_id, stock_id="nonexistent_id", quantity=10, sell_price=29.99
→ Expect: ValueError("Stock Not found")
Test 7 – Refill with quantity=0
Call refill_stock with quantity=0, valid manager_id and stock_id
→ Expect: either stock quantity unchanged or an appropriate error raised by stock.refill_stock()
Test 8 – Refill with negative quantity
Call refill_stock with quantity=-5
→ Expect: error raised — stock quantity should never decrease via refill
Test 9 – Refill with negative sell_price
Call refill_stock with sell_price=-1.0
→ Expect: error raised — sell price should never be negative
Test 10 – Non-manager staff attempting refill
Call refill_stock using a staff_id in place of manager_id
→ Expect: ValueError("Manager Not found")