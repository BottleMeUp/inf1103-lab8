from product import Product

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.__product: Product = product
        self.__quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.get_name()} | Qty: {self.__quantity} | "
              f"Unit Price: {self.__product.get_price()} | "
              f"Subtotal: {self.calculate_subtotal()}")