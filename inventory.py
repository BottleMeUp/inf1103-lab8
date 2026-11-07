class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id().upper() == product_id.upper():
                return product
        return None

    def display_all(self):
        print("Current Inventory\n")
        print("------------------------------------------------")
        for product in self.__products:
            product.display_information()
        print("------------------------------------------------")

    def get_all_products(self):
        return list(self.__products)