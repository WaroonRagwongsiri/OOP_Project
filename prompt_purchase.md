✅ Happy Path Tests
Test 1 – Basic purchase (no coupon)
Call purchase with customer_id={customer_id}, payment_method_name="QRCode", payment_info=["500"], no coupon_id
→ Expect: returns a bill_id and a non-empty product_sn_list
→ Expect: product status changes to SOLDED
→ Expect: cart no longer contains the purchased item
Test 2 – Purchase with a valid coupon

Call create_coupon with minimum_amount=10.0, discount_amount=5.0, expire_date="2027-01-01T00:00:00" → save coupon_id
Re-add product to cart and mark is_buy=true
Call purchase with coupon_id={coupon_id}
→ Expect: bill total is reduced by 5.0
→ Expect: valid bill_id and product_sn_list returned

Test 3 – Member discount applied

Subscribe customer_id to membership before purchasing
Call purchase normally
→ Expect: total_pricing reflects membership discount via apply_discount_benefit()


❌ Error / Edge Case Tests
Test 4 – Invalid customer ID
Call purchase with customer_id="nonexistent_id", valid payment info
→ Expect: Exception("Customer doesn't exist")
Test 5 – Invalid payment method
Call purchase with valid customer_id, payment_method_name="INVALID_METHOD"
→ Expect: Exception("Payment method not found")
Test 6 – No items marked is_buy=true in cart
Call purchase with a customer whose cart items all have is_buy=false
→ Expect: returns an empty product_sn_list and a bill with total=0
Test 7 – Product becomes unavailable before purchase

Add product to cart, mark is_buy=true
Manually set product status to something other than SELLING (e.g. already SOLDED)
Call purchase
→ Expect: Exception("Product is unavailable")

Test 8 – Expired coupon

Create a coupon with expire_date in the past (e.g. "2020-01-01T00:00:00")
Call purchase with that coupon_id
→ Expect: Exception("Error while applying coupon")

Test 9 – Coupon minimum amount not met

Create a coupon with minimum_amount=9999.0
Call purchase on a cheap item with that coupon_id
→ Expect: Exception("Error while applying coupon")

Test 10 – Payment failure

Simulate a payment gateway that returns False on start_payment
Call purchase with that payment method
→ Expect: Exception("Payment Failed.")