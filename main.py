import json
import os
from inventory import Inventory
from order import Order
from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from interface import CanBeShipped

# Adjust the import names above to match your file names.

FILENAME = "inventory.json"

# One shared Supplier object per supplier ID, so products from the same
# supplier reference the same object (association, not copies).
suppliers: dict[str, Supplier] = {}


def get_or_create_supplier(supplier_id: str, name: str, email: str) -> Supplier:
    key = supplier_id.upper()
    if key not in suppliers:
        suppliers[key] = Supplier(supplier_id, name, email)
    return suppliers[key]


# ---------- Saving / loading ----------

def product_to_dict(product: Product) -> dict:
    supplier = product.get_supplier()
    data = {
        "ID": product.get_product_id(),
        "Name": product.get_name(),
        "Price": product.get_price(),
        "Stock": product.get_stock(),
        "Supplier ID": supplier.get_supplier_id(),
        "Supplier Name": supplier.get_name(),
        "Supplier Email": supplier.get_contact_email(),
    }
    if isinstance(product, PhysicalProduct):
        data["Type"] = "physical"
        data["Weight"] = product.get_weight()
    elif isinstance(product, DigitalProduct):
        data["Type"] = "digital"
        data["Download Size"] = product.get_download_size()
    return data


def dict_to_product(item: dict) -> Product:
    product_type = item["Type"]
    price = float(str(item["Price"]).replace("$", ""))

    # .get() with defaults keeps an old inventory.json (no supplier data) loading
    supplier = get_or_create_supplier(
        item.get("Supplier ID", "S000"),
        item.get("Supplier Name", "Unknown Supplier"),
        item.get("Supplier Email", "unknown@example.com"),
    )

    if product_type == "physical":
        return PhysicalProduct(item["ID"], item["Name"], price,
                               item["Stock"], item["Weight"], supplier)
    if product_type == "digital":
        return DigitalProduct(item["ID"], item["Name"], price,
                              item["Stock"], item["Download Size"], supplier)
    raise ValueError(f"Unknown product type: {product_type}")


def load_inventory(inventory: Inventory) -> None:
    if not os.path.exists(FILENAME):
        return
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Warning: inventory.json is empty or invalid. Starting with empty inventory.")
        return

    for item in data:
        try:
            inventory.add_product(dict_to_product(item))
        except (KeyError, ValueError) as e:
            print(f"Warning: skipped an invalid product entry ({e}).")


def save_inventory(inventory: Inventory) -> None:
    print("Saving inventory... ")
    data = [product_to_dict(p) for p in inventory.get_all_products()]
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)
    print("Inventory saved successfully to inventory.json.")


def exit_program(inventory: Inventory) -> None:
    save_inventory(inventory)
    print("Thank you for using Inventory Management System.\nProgram terminated.")


# ---------- Display helpers ----------

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    # if isinstance(product, CanBeShipped):
    #     print(f"Shipping cost: ${product.calculate_shipping_cost():.2f}")
    # print("Supplier:")
    # product.get_supplier().display_information()


def show_menu() -> None:
    print("""
----------- MENU -----------
1. Display All Products
2. Add Product
3. Update Stock
4. Search Product
5. Save Inventory
6. Test: Association (Supplier - Product)
7. Test: Aggregation (Inventory - Product)
8. Test: Composition (Order - OrderLine)
9. Test: LSP
10. Test: Polymorphism 
11. Exit
----------------------------
""")


# ---------- Adding products ----------

def prompt_supplier() -> Supplier:
    """Reuse an existing supplier by ID, or create a new one."""
    supplier_id = input("Enter Supplier ID: ").strip()
    key = supplier_id.upper()
    if key in suppliers:
        print("Existing supplier found:")
        suppliers[key].display_information()
        return suppliers[key]
    name = input("Enter Supplier Name: ").strip()
    email = input("Enter Supplier Email: ").strip()
    return get_or_create_supplier(supplier_id, name, email)


def prompt_new_product() -> Product | None:
    """Ask the user for product details and return the right subclass, or None."""
    print("Product type:\n1. Physical\n2. Digital")
    type_choice = input("Choose type (1-2): ").strip()
    if type_choice not in ("1", "2"):
        print("Invalid product type.")
        return None

    try:
        product_id = input("Enter Product ID: ").strip()
        name = input("Enter Name: ").strip()
        price = float(input("Enter Price: "))
        stock = int(input("Enter Stock: "))
        supplier = prompt_supplier()

        if type_choice == "1":
            weight = float(input("Enter Weight (kg): "))
            return PhysicalProduct(product_id, name, price, stock, weight, supplier)
        else:
            download_size = float(input("Enter Download Size (MB): "))
            return DigitalProduct(product_id, name, price, stock, download_size, supplier)
    except ValueError:
        print("Invalid numeric value.")
        return None


def run_association_test() -> None:
    print("\n=== ASSOCIATION TEST: Supplier and Product ===")
    supplier = Supplier("S900", "Test Supplier", "test@example.com")
    laptop = PhysicalProduct("T-P1", "Test Laptop", 1200.0, 10, 2.5, supplier)
    ebook = DigitalProduct("T-D1", "Test Ebook", 25.0, 100, 5.0, supplier)

    print("\nLaptop's supplier:")
    laptop.get_supplier().display_information()
    print("Ebook's supplier:")
    ebook.get_supplier().display_information()

    print("\nSupplier is a separate object from the products:",
          supplier is not laptop and supplier is not ebook)
    print("Both products reference the same Supplier object:",
          laptop.get_supplier() is ebook.get_supplier() is supplier)

    del supplier
    print("\nAfter 'del supplier', products can still show their supplier:")
    laptop.get_supplier().display_information()
    ebook.get_supplier().display_information()


def run_aggregation_test() -> None:
    print("\n=== AGGREGATION TEST: Inventory and Product ===")
    supplier = Supplier("S900", "Test Supplier", "test@example.com")
    laptop = PhysicalProduct("T-P1", "Test Laptop", 1200.0, 10, 2.5, supplier)
    inventory_a = Inventory()
    inventory_b = Inventory()

    print("\n1. Product created before any inventory:")
    laptop.display_information()

    inventory_a.add_product(laptop)
    print("\n2. Added to Inventory A. Products in A:",
          len(inventory_a.get_all_products()))

    inventory_a.remove_product("T-P1")
    print("\n3. Removed from Inventory A. Products in A:",
          len(inventory_a.get_all_products()))
    print("   Product still usable:")
    laptop.display_information()
    print("   Fulfilment:", laptop.get_fulfilment_info())

    inventory_b.add_product(laptop)
    print("\n4. Added the SAME object to Inventory B.")
    print("   Same object in B:", inventory_b.find_product("T-P1") is laptop)

    inventory_b.remove_product("T-P1")
    print("\n5. Inventory B emptied. Products in B:",
          len(inventory_b.get_all_products()))
    print("   Product still exists:")
    laptop.display_information()


def run_composition_test() -> None:
    print("\n=== COMPOSITION TEST: Order and OrderLine ===")
    supplier = Supplier("S900", "Test Supplier", "test@example.com")
    laptop = PhysicalProduct("T-P1", "Test Laptop", 1200.0, 10, 2.5, supplier)
    ebook = DigitalProduct("T-D1", "Test Ebook", 25.0, 100, 5.0, supplier)

    order_1 = Order("O001")
    order_1.add_order_line(laptop, 2)
    order_1.add_order_line(ebook, 3)
    print("\nOrder 1:")
    order_1.display_order()
    print("Expected total: 2475.0")

    order_2 = Order("O002")
    order_2.add_order_line(laptop, 1)
    print("\nOrder 2 (same laptop):")
    order_2.display_order()

    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print("\nSame Product object in both lines:",
          line_1.get_product() is line_2.get_product())
    print("Same OrderLine object in both orders:", line_1 is line_2)
    print("OrderLine ids:", id(line_1), id(line_2))
    print("Product ids:  ", id(line_1.get_product()), id(line_2.get_product()))
    print("Result: 2 OrderLine objects, 1 Product object")

    print("\nRemoving the ebook line from Order 1:")
    order_1.remove_order_line("T-D1")
    order_1.display_order()
    print("Ebook product still exists:")
    ebook.display_information()


def run_lsp_test() -> None:
    print("\n=== LSP TEST: Substitutability ===")
    supplier = Supplier("S900", "Test Supplier", "test@example.com")
    laptop = PhysicalProduct("T-P1", "Test Laptop", 1200.0, 10, 2.5, supplier)
    ebook = DigitalProduct("T-D1", "Test Ebook", 25.0, 100, 5.0, supplier)

    print("\n1. One function, both subclasses (no changes to the function):")
    show_product_details(laptop)
    print()
    show_product_details(ebook)

    print("\n2. Both types in the same Inventory:")
    test_inventory = Inventory()
    test_inventory.add_product(laptop)
    test_inventory.add_product(ebook)
    test_inventory.display_all_products()

    print("\n3. Normal Inventory operations work for both:")
    print("find_product('T-P1'):", test_inventory.find_product("T-P1").get_name())
    print("find_product('T-D1'):", test_inventory.find_product("T-D1").get_name())

    print("\n4. update_stock() keeps the same meaning for both:")
    laptop.update_stock(5)
    ebook.update_stock(50)
    laptop.update_stock(-1)   # rejected the same way for both
    ebook.update_stock(-1)
    print("Laptop stock:", laptop.get_stock(), "| Ebook stock:", ebook.get_stock())

    test_inventory.remove_product("T-D1")
    print("\n5. Remove works for either type. Products left:",
          len(test_inventory.get_all_products()))

def run_polymorphism_test() -> None:
    print("\n=== POLYMORPHISM TEST ===")
    supplier = Supplier("S900", "Test Supplier", "test@example.com")

    # Predict first (write these in your Word doc BEFORE running):
    #   Laptop -> "Product requires physical shipping"
    #   Ebook  -> "Product is delivered digitally"

    inventory = Inventory()
    inventory.add_product(PhysicalProduct("T-P1", "Test Laptop", 1200.0, 10, 2.5, supplier))
    inventory.add_product(DigitalProduct("T-D1", "Test Ebook", 25.0, 100, 5.0, supplier))
    inventory.add_product(PhysicalProduct("T-P2", "Test Keyboard", 80.0, 30, 0.8, supplier))

    print("\nOne loop over the Product collection, no isinstance():\n")
    for product in inventory.get_all_products():
        product.display_information()
        print(f"Fulfilment: {product.get_fulfilment_info()}")
        print()


# ---------- Main program ----------

main_inventory = Inventory()
load_inventory(main_inventory)

while True:
    show_menu()
    try:
        option = int(input("Enter option (1-10): "))
    except ValueError:
        print("Please enter a number from 1 to 10.")
        continue

    match option:
        case 1:
            main_inventory.display_all_products()
        case 2:
            product = prompt_new_product()
            if product is None:
                continue
            main_inventory.add_product(product)
            print("Product added.")
        case 3:
            product_id = input("Enter Product ID: ").strip()
            product = main_inventory.find_product(product_id)
            if product is None:
                print("Product not found.")
                continue
            try:
                new_quantity = int(input("Enter New Stock Quantity: "))
            except ValueError:
                print("Please enter a whole number.")
                continue
            product.update_stock(new_quantity)
        case 4:
            product_id = input("Enter Product ID: ").strip()
            product = main_inventory.find_product(product_id)
            if product:
                show_product_details(product)
            else:
                print("Product not found.")
        case 5:
            save_inventory(main_inventory)
        case 6:
            run_association_test()
        case 7:
            run_aggregation_test()
        case 8:
            run_composition_test()
        case 9:
            run_lsp_test()
        case 10:
            run_polymorphism_test()
        case 11:
            exit_program(main_inventory)
            break
        case _:
            print("Invalid choice, please try again.")