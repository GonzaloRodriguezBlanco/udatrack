# This module contains the OrderTracker class, which encapsulates the core
# business logic for managing orders.
from typing import Final, List

from backend.exception.duplicate_order_error import DuplicateOrderError
from backend.exception.empty_order_id_error import EmptyOrderIdError
from backend.exception.invalid_initial_status_error import InvalidInitialStatusError
from backend.exception.invalid_status_error import InvalidStatusError
from backend.exception.minimum_order_quantity_error import MinimumOrderQuantityError
from backend.exception.order_not_found_error import OrderNotFoundError


class OrderTracker:
    """
    Manages customer orders, providing functionalities to add, update,
    and retrieve order information.
    """
    MIN_QUANTITY_ALLOWED: Final[int] = 1
    INITIAL_STATUS_ALLOWED: Final[List[str]] = ['pending', 'processing']
    VALID_STATUS_ALLOWED: Final[List[str]] = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

    def __init__(self, storage):
        required_methods = ['save_order', 'get_order', 'get_all_orders']
        for method in required_methods:
            if not hasattr(storage, method) or not callable(getattr(storage, method)):
                raise TypeError(f"Storage object must implement a callable '{method}' method.")
        self.storage = storage

    def add_order(self, order_id: str, item_name: str, quantity: int, customer_id: str, status: str = "pending"):
        if quantity < self.MIN_QUANTITY_ALLOWED:
            raise MinimumOrderQuantityError(self.MIN_QUANTITY_ALLOWED, quantity)

        if status not in self.INITIAL_STATUS_ALLOWED:
            raise InvalidInitialStatusError(self.INITIAL_STATUS_ALLOWED, status)

        if self.storage.get_order(order_id) is not None:
            raise DuplicateOrderError(order_id)

        order = {
            "order_id": order_id,
            "item_name": item_name,
            "quantity": quantity,
            "customer_id": customer_id,
            "status": status
        }

        self.storage.save_order(order_id, order)

        return order

    def get_order_by_id(self, order_id: str):
        if not order_id:
            raise EmptyOrderIdError()

        return self.storage.get_order(order_id)

    def update_order_status(self, order_id: str, new_status: str):
        if not order_id:
            raise EmptyOrderIdError()

        self.__validate_status(new_status)

        order = self.storage.get_order(order_id)

        if not order:
            raise OrderNotFoundError(order_id)

        order["status"] = new_status
        self.storage.save_order(order_id, order)
        return order

    def list_all_orders(self):
        return list(self.storage.get_all_orders().values())

    def list_orders_by_status(self, status: str):
        self.__validate_status(status)

        filtered_orders = {k: v for k, v in self.storage.get_all_orders().items() if status == v.get('status')}

        return list(filtered_orders.values())

    def __validate_status(self, status: str):
        if status not in self.VALID_STATUS_ALLOWED:
            raise InvalidStatusError(self.VALID_STATUS_ALLOWED, status)