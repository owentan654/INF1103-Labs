from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style contract: anything that can be shipped must price its shipping."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass
