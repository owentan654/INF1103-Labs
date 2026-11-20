from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    #Strategy interface: every dicount turns an order total into a discounted total.
    def apply(self, total: float) -> float:
        return total

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float) -> None:
        if not 0 <= percent <= 100:
            raise ValueError("Percentage must be between 0 & 100.")
        self.__percent: float = percent

    def apply(self,total: float) -> float:
        return total * (1 - self.__percent/100)

class BulkDiscount(DiscountStrategy):
    #Takes amount off any total that reaches threshold
    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.__threshold = threshold
        self.__amount = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        else:
            return total

class StudentDiscount(DiscountStrategy):
    #added without touching order
    def apply(self, total: float) -> float:
        return total * 0.95