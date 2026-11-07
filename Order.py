from order_line import OrderLine
from product import Product

class Order:
    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id:str) -> None:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id().upper() == product_id.upper():
                self.__order_lines.remove(order_line)
                return
        print(f"No order line found for product {product_id}.")

    def calculate_total(self)-> float:
        grand_total: float = 0.0
        for order_line in self.__order_lines:
            grand_total += order_line.calculate_subtotal()
        return grand_total

    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    def display_order(self) -> None:
        print(f"Order {self.__order_id}")
        print("------------------------------------------------")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("------------------------------------------------")
        print(f"Total: {self.calculate_total()}")
        