from abc import ABC, abstractmethod
from typing import List, Dict, Any
from entity.user import User
from entity.product import Product
from exception.ordernotfound import OrderNotFoundException
from exception.usernotfoundexception import UserNotFoundException

class OrderManagementRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> bool:
        pass

    @abstractmethod
    def create_product(self, user: User, product: Product) -> bool:
        pass

    @abstractmethod
    def create_order(self, user: User, products: List[Product]) -> bool:
        pass

    @abstractmethod
    def cancel_order(self, user_id: int, order_id: int) -> bool:
        pass

    @abstractmethod
    def get_all_products(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_order_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        pass