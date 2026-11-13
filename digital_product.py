from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, 
                 supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size = download_size

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via download link."

    def display_information(self) -> None:
        super().display_information()
        print(f"{'':<10} Download size: {self.__download_size} MB")

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
