🧪 subscribe Test Suite
⚙️ Setup
Call create_customer with name="Alice", age=25 → save customer_id

✅ Happy Path
Test 1 – Valid subscription
Call subscribe with:

customer_id={customer_id}, payment_gateway_name="QRCode", payment_information="0812345678"

→ Expect: member object returned, save as member_id

❌ Fail Cases
Test 2 – Invalid customer_id
Call subscribe with:

customer_id="INVALID_ID", payment_gateway_name="QRCode", payment_information="0812345678"

→ Expect: "Error: Customer not found"

Test 3 – Invalid payment gateway
Call subscribe with:

customer_id={customer_id}, payment_gateway_name="BITCOIN", payment_information="0812345678"

→ Expect: "Error: Payment gateway not found"

Test 4 – Already an active member (duplicate subscribe)
(Alice is already ACTIVE from Test 1)
Call subscribe again with:

customer_id={customer_id}, payment_gateway_name="QRCode", payment_information="0812345678"

→ Expect: "Error: Fail already be a member"

🔁 Bonus – Re-subscribe after unsubscribe
Test 5 – Unsubscribe then re-subscribe (should succeed)
Call unsubscribe with member_id={member_id} → expect success
Call subscribe again with same customer_id, payment_gateway_name="QRCode", payment_information="0812345678"
→ Expect: member object returned with status=ACTIVE (hits the if member: branch, reactivating the existing member rather than creating a new one)
