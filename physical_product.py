from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)    # reuse Product's constructor
        self.__weight = weight

    def get_fulfilment_info(self):
        return "Requires physical shipping."

    def calculate_shipping_cost(self):
        return 5.00 + 2.50 * self.__weight                  # $5 + ($2.50 per kg)

    def display_information(self):
        super().display_information()
        print(f"{'':<10} Weight: {self.__weight} kg")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
