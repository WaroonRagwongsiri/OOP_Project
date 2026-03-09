🔌 Phase 0 – Connection

Call test_connection → expect {"message": "Hello World"}


👥 Phase 1 – People Setup

Call create_customer with name="Alice", age=25 → save customer_id
Call create_customer with name="Bob", age=17 → save customer_id_2
Call get_all_customers → expect both Alice and Bob appear
Call create_staff with name="StaffJohn", age=30 → save staff_id
Call create_manager with name="ManagerMike", age=40 → save manager_id


🏠 Phase 2 – Room Setup

Call create_room with max_customer=4, rate_price=100.0 → save room_id
Call get_available_rooms → expect the room created above appears


🎮 Phase 3 – Product & Inventory Setup

Call create_game with manager_id={manager_id}, name="Chess", description="Classic strategy game", genre="Strategy", game_type="DISC" → save game_id
Call create_machine with manager_id={manager_id}, name="Arcade1", machine_type="PLAYSTATION" → save machine_id
Call get_all_stocks → save a stock_id from the list
Call refill_stock with manager_id={manager_id}, stock_id={stock_id}, quantity=10, sell_price=29.99 → expect success message
Call create_shelf with max_capacity=5 → save shelf_id
Call get_all_shelves → expect the shelf above appears
Call refill_shelf with staff_id={staff_id}, shelf_id={shelf_id}, stock_id={stock_id}, quantity=3 → expect current_amount=3


🎟️ Phase 4 – Membership

Call subscribe with customer_id={customer_id}, payment_gateway_name="QRCode", payment_information="0812345678" → save member_id
Call unsubscribe with member_id={member_id} → expect success message


📅 Phase 5 – Reservation Lifecycle

Call create_reservation with customer_id={customer_id}, room_id={room_id}, start_time="2026-03-10T10:00:00", end_time="2026-03-10T12:00:00" → save reservation_id
Call extend_time with customer_id={customer_id}, reservation_id={reservation_id}, additional_hours=1.0 → expect end_time extended by 1 hour
Call check_in with customer_id={customer_id}, reservation_id={reservation_id} → expect status change
Call request_item_for_room with customer_id={customer_id}, reservation_id={reservation_id}, product_id={game_id}, quantity=1 → expect total_items_in_room >= 1
Call check_out with customer_id={customer_id}, reservation_id={reservation_id} → expect status change

📅 Phase 5b – Reservation Cancellation

Call create_reservation (new one) → save reservation_id_2
Call cancel_reservation with customer_id={customer_id}, reservation_id={reservation_id_2} → expect status=cancelled


🛒 Phase 6 – Cart & Purchase

Call view_product_detail with a serial_number from a shelf item (use one from refill_shelf result) → expect status/price/condition fields
Call add_product_to_cart with customer_id={customer_id}, product_id={game_id} → expect total_items increases
Call view_cart with customer_id={customer_id} → save serial_number from result
Call set_cart_item_buy with customer_id={customer_id}, serial_number={serial_number}, is_buy=true → expect is_buy=true
Call set_cart_item_buy again with is_buy=false → expect is_buy=false, then set back to true
Call remove_item_from_cart with customer_id={customer_id}, product_id={game_id} → expect total_items decreases
Re-add product and mark is_buy=true

🎫 Phase 6b – Coupon & Purchase with Coupon

Call create_coupon with manager_id={manager_id}, customer_id={customer_id}, minimum_amount=10.0, discount_amount=5.0, expire_date="2027-01-01T00:00:00" → save coupon_id
Call purchase with customer_id={customer_id}, payment_method_name="QRCode", payment_information=["500"], coupon_id={coupon_id} → save bill_id and product_serials

💸 Phase 6c – Refund

Call refund with customer_id={customer_id}, bill_id={bill_id}, product_serial_numbers={product_serials} → expect refund coupon returned


❌ Phase 7 – Error / Edge Cases

Call create_reservation with an invalid customer_id → expect "Error: ..." string
Call cancel_reservation on an already-cancelled reservation → expect "Error: ..."
Call check_in on a non-existent reservation → expect "Error: ..."
Call refill_shelf with quantity exceeding shelf capacity → expect "Error: ..."
Call set_cart_item_buy with a serial number not in cart → expect "Error: Item not found in cart"
Call unsubscribe with an invalid member_id → expect "Error: ..."