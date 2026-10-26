class Product: 
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    #Read-only access
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def update_stock(self,quantity):
        if quantity < 0:
            return False        #Protects its own state
        self.__stock = quantity
        return True

    def display_information(self):
        print(f"{self.__product_idK:<10} {self.__name:<20}"
              f"{self.__stock:<10} {self.__price:<10.2f}")

    def to_dict(self):
        return {"id": self.__product_id, "Product_name": self.__name, 
                "Price": self.__price, "Stock": self.__stock}

class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False        #Dupe Check
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product      #returns the Product object itself
        return None
    def display_all(self):
        if not self.__products:
            print("\nThe inventory is currently empty.")
            return
        print("\n" + "=" * 55)      #Makes lines
        for product in self.__products:
            product.display_information()       #Inventory asks each Product to show itself
        print("=" * 55)

    def get_products(self):
        return self.__products

import json, os

FILE_NAME = "inventory.json"
failed_entries = 0
inventory = 0

def load_inventory():
    inventory = Inventory()
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                for item in json.load(file):
                    inventory.add_product(Product(
                        item["id"], item["Product_name"],
                        item["Price"], item["Stock"]
                    ))
        except (json.JSONDecodeError, IOError, KeyError):
            print("Error loading file. Starting empty.")