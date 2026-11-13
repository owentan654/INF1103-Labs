from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, 
                 supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)    # reuse Product's constructor
        self.__weight = weight

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return 5.00 + 2.50 * self.__weight                  # $5 + ($2.50 per kg)

    def display_information(self) -> None:
        super().display_information()
        print(f"{'':<10} Weight: {self.__weight} kg")

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
