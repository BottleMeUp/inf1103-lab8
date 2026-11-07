import json
import os
from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from interface import CanBeShipped

FILENAME = "inventory.json"


def product_to_dict(product):
    data = {
        "ID": product.get_product_id(),
        "Name": product.get_name(),
        "Price": product.get_price(),
        "Stock": product.get_stock(),
    }
    if isinstance(product, PhysicalProduct):
        data["Type"] = "physical"
        data["Weight"] = product.get_weight()
    elif isinstance(product, DigitalProduct):
        data["Type"] = "digital"
        data["Download Size"] = product.get_download_size()
    return data


def dict_to_product(item):
    product_type = item["Type"]
    price = float(str(item["Price"]).replace("$", ""))

    if product_type == "physical":
        return PhysicalProduct(item["ID"], item["Name"], price,
                               item["Stock"], item["Weight"])
    if product_type == "digital":
        return DigitalProduct(item["ID"], item["Name"], price,
                              item["Stock"], item["Download Size"])
    raise ValueError(f"Unknown product type: {product_type}")


def load_inventory(inventory):
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


def save_inventory(inventory):
    print("Saving inventory... ")
    data = [product_to_dict(p) for p in inventory.get_all_products()]
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)
    print("Inventory saved successfully to inventory.json.")


def exit_program(inventory):
    save_inventory(inventory)
    print("Thank you for using Inventory Management System.\nProgram terminated.")

def show_product_details(product):
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"Shipping cost: ${product.calculate_shipping_cost():.2f}")


def show_menu():
    print("""
----------- MENU -----------
1. Display All Products
2. Add Product
3. Update Stock
4. Search Product
5. Save Inventory
6. Exit
----------------------------
""")


def prompt_new_product():
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

        if type_choice == "1":
            weight = float(input("Enter Weight (kg): "))
            return PhysicalProduct(product_id, name, price, stock, weight)
        else:
            download_size = float(input("Enter Download Size (MB): "))
            return DigitalProduct(product_id, name, price, stock, download_size)
    except ValueError:
        print("Invalid numeric value.")
        return None


main_inventory = Inventory()
load_inventory(main_inventory)

while True:
    show_menu()
    try:
        option = int(input("Enter option (1-6): "))
    except ValueError:
        print("Please enter a number from 1 to 6.")
        continue

    match option:
        case 1:
            main_inventory.display_all()
        case 2:
            product = prompt_new_product()
            if product is None:
                continue
            main_inventory.add_product(product)
            print("Product added.")
        case 3:
            product_id = input("Enter Product ID: ").strip()
            product = main_inventory.search_product(product_id)
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
            product = main_inventory.search_product(product_id)
            if product:
                show_product_details(product)
            else:
                print("Product not found.")
        case 5:
            save_inventory(main_inventory)
        case 6:
            exit_program(main_inventory)
            break
        case _:
            print("Invalid choice, please try again.")