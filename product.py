from abc import ABC, abstractmethod


class Product(ABC):
    """Abstract base class: represents and manages ONE product."""

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # Read-only access
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        if quantity < 0:
            return False        # Protects its own state
        self.__stock = quantity
        return True

    def display_information(self):
        print(f"{self.__product_id:<10} {self.__name:<20}"
              f"{self.__stock:<10} {self.__price:<10.2f}")

    def to_dict(self):
        return {"id": self.__product_id, "Product_name": self.__name,
                "Price": self.__price, "Stock": self.__stock}

    @abstractmethod
    def get_fulfilment_info(self):
        pass
