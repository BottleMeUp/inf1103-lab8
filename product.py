from abc import ABC, abstractmethod 
from supplier import Supplier

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier):
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    def update_stock(self, quantity) -> None:
        print("Update Stock")
        if quantity < 0:
            print("Stock cannot be negative.")
            return
    
        self.__stock = quantity
        print(f"\nNew Stock Quantity: {self.__stock}")
        print("\nStock updated successfully! ")

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: {self.__price} | Stock: {self.__stock}")

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price
    
    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass




            







    