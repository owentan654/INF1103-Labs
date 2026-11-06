from product import Product


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    def get_fulfilment_info(self):
        return "Delivered digitally via download link."

    def display_information(self):
        super().display_information()
        print(f"{'':<10} Download size: {self.__download_size} MB")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
