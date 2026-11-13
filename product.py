from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    """Abstract base class: represents and manages ONE product."""

    def __init__(self, product_id: str, name: str, price: float, 
                 stock: int, supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    # Read-only access
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

    def update_stock(self, quantity) -> bool:
        if quantity < 0:
            return False        # Protects its own state
        self.__stock = quantity
        return True

    def display_information(self) -> None:
        print(f"{self.__product_id:<10} {self.__name:<20}"
              f"{self.__stock:<10} {self.__price:<10.2f}")

    def to_dict(self) -> dict[str, object]:
        return {"id": self.__product_id, "Product_name": self.__name,
                "Price": self.__price, "Stock": self.__stock, 
                "supplier":self.__supplier.to_dict}

    @abstractmethod
    def get_fulfilment_info(self):
        pass
