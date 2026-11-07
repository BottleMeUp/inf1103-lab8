from product import Product
from interface import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight = weight

    # Override the parent method
    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_weight(self):
        return self.__weight

    def get_fulfilment_info(self):
        return "Product requires physical shipping"

    def calculate_shipping_cost(self):
        return self.__weight * 10