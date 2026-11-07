from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

# 1. Create a Supplier independently
supplier = Supplier("S001", "Acme Ltd", "acme@example.com")

# 2. Create both product types using that supplier
laptop = PhysicalProduct("P001", "Laptop", 1200.0, 10, 2.5, supplier)
ebook = DigitalProduct("D001", "Python Ebook", 25.0, 100, 10, supplier)  # adjust to YOUR DigitalProduct args

# 3. Display supplier info through each product
print("--- Laptop's supplier ---")
laptop.get_supplier().display_information()

print("\n--- Ebook's supplier ---")
ebook.get_supplier().display_information()

# 4. Confirm they are separate objects
print("\n--- Independence checks ---")
print("Supplier is not the product:", supplier is not laptop and supplier is not ebook)
print("Both products share the same Supplier object:",
      laptop.get_supplier() is ebook.get_supplier() is supplier)

# Predict first: delete the supplier variable
del supplier
print("\n--- After del supplier ---")
laptop.get_supplier().display_information()  
ebook.get_supplier().display_information()