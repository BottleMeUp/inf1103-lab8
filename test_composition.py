from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order

# Adjust the import names above to match your file names.

supplier = Supplier("S001", "Acme Ltd", "acme@example.com")
laptop = PhysicalProduct("P001", "Laptop", 1200.0, 10, 2.5, supplier)
ebook = DigitalProduct("D001", "Python Ebook", 25.0, 100, 5, supplier)

# 1. Create an Order and add two products using add_order_line()
order_1 = Order("O001")
order_1.add_order_line(laptop, 2)
order_1.add_order_line(ebook, 3)

# 2. Display each order line and calculate the total
print("Step 1-2: Order 1")
order_1.display_order()
print("Expected total: 2475.0 (2 x 1200 + 3 x 25)")

# 3. Add the SAME products to a different Order
order_2 = Order("O002")
order_2.add_order_line(laptop, 1)

print("\nStep 3: Order 2 (same laptop, different quantity)")
order_2.display_order()

# Check identity: how many OrderLines vs Products?
line_1 = order_1.get_order_lines()[0]   # laptop line in order 1
line_2 = order_2.get_order_lines()[0]   # laptop line in order 2

print("\n--- Identity checks ---")
print("Both lines refer to the same Product object:",
      line_1.get_product() is line_2.get_product())
print("Both lines are the same OrderLine object:", line_1 is line_2)
print("OrderLine ids:", id(line_1), id(line_2))
print("Product ids:  ", id(line_1.get_product()), id(line_2.get_product()))

# 4. Remove an order line through an Order method
print("\nStep 4: Remove the ebook line from Order 1")
order_1.remove_order_line("D001")
order_1.display_order()
print("Expected total: 2400.0")

# The Product is unaffected by the removal
print("\nEbook still exists and works after its line was removed:")
ebook.display_information()

# 5. Remove an entire Order from the scenario
print("\nStep 5: Delete Order 2 entirely")
del order_2
print("Order 1 is unaffected:")
order_1.display_order()
print("Laptop (the Product) is unaffected:")
laptop.display_information()