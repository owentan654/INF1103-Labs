from product import Product

class Inventory:
    """Manages a collection of Product objects (it never looks inside them)."""

    MAX_UNITS = 500
    TAX_RATE = 0.1

    def __init__(self) -> None:
        self.__products = []

    def add_product(self, product: Product) -> bool:
        if self.search_product(product.get_product_id()) is not None:
            return False        # Dupe check
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        product = self.search_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def search_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product  # returns the Product object itself
        return None

    def display_all(self) -> None:
        if not self.__products:
            print("\nThe inventory is currently empty.")
            return
        print("\n" + "=" * 55)
        for product in self.__products:
            product.display_information()   # each Product shows itself
        print("=" * 55)

    def get_products(self) -> list[Product]:
        return self.__products

    def get_total_units(self) -> int:
        return sum(p.get_stock() for p in self.__products)

    def exceeds_limits(self, extra_units) -> bool:
        return self.get_total_units() + extra_units > self.MAX_UNITS

    def calculate_tax(self) -> float:
        return self.TAX_RATE * self.get_total_units()
