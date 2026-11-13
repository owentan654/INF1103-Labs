from product import Product

class OrderLine:
    """One product + quantity inside one order. 
        Created and managed by Order."""

    def __init__(self, product: Product, quantity: int) -> None:
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.get_name():<20} x {self.__quantity:<5} "
              f"@ {self.__product.get_price():>9.2f} = {self.calculate_subtotal():>10.2f}")