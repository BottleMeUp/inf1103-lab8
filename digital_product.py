from product import Product
from supplier import Supplier

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)

        self.__download_size = download_size

    # Override the parent method
    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size}")

    def get_fulfilment_info(self) -> None:
        return "Product is delivered digitally"

    def get_download_size(self) -> float:
        return self.__download_size
    