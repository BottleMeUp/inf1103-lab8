from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

# Adjust the import names above to match your file names.

supplier = Supplier("S001", "Acme Ltd", "acme@example.com")

# 1. Create products BEFORE any inventory exists
laptop = PhysicalProduct("P001", "Laptop", 1200.0, 10, 2.5, supplier)
ebook = DigitalProduct("D001", "Python Ebook", 25.0, 100, 5, supplier)
print("Step 1: Products created before any Inventory exists")
laptop.display_information()
ebook.display_information()

# 2. Add the laptop to Inventory A
inventory_a = Inventory()
inventory_b = Inventory()
inventory_a.add_product(laptop)
inventory_a.add_product(ebook)

print("\nStep 2: Inventory A after adding both products")
inventory_a.display_all_products()
print("Products in A:", len(inventory_a.get_all_products()))

# 3. Remove the laptop from Inventory A
inventory_a.remove_product("P001")

print("\nStep 3: Inventory A after removing the laptop")
inventory_a.display_all_products()
print("Products in A:", len(inventory_a.get_all_products()))
print("Laptop still in A?", inventory_a.find_product("P001") is not None)

# Confirm the removed Product still works
print("\nCheck if Laptop still usable after removal:")
laptop.display_information()
print("Fulfilment info:", laptop.get_fulfilment_info())
laptop.update_stock(8)
print("Stock is now:", laptop.get_stock())

# 4. Add the SAME object to Inventory B
inventory_b.add_product(laptop)

print("\nStep 4: Inventory B after adding the same laptop")
inventory_b.display_all_products()
print("Same object in B?", inventory_b.find_product("P001") is laptop)
print("Updated stock visible via B?", inventory_b.find_product("P001").get_stock() == 8)

# 5. Empty an inventory entirely
print("\nStep 5: Emptying Inventory A and B")
inventory_a.remove_product("D001")
inventory_b.remove_product("P001")
print("Products in A:", len(inventory_a.get_all_products()))
print("Products in B:", len(inventory_b.get_all_products()))

print("\nProducts still exist after both inventories are empty:")
laptop.display_information()
ebook.display_information()