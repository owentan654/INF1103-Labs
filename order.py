from product import Product
from orderline import OrderLine

class Order:
    """Composition: An Order creates, manages and owns its OrderLine objects."""

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_lines(self, product_id: str) -> bool:
        for line in self.__order_lines:
            if line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(line)
                return True
        return False

    def get_orderlines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_information(self) -> None:
        print(f"\Order {self.__order_id}")
        print("-" * 55)
        for line in self.__order_lines:
            line.display_information()
        print("-" * 55)
        print(f"{'Total:':<38} {self.calculate_total():>10.2f}")