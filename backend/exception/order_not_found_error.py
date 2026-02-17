from typing import Final


class OrderNotFoundError(ValueError):
    MESSAGE: Final[str] = "Order with ID '{}' not found."
    def __init__(self, order_id, *args):
        self.message = self.MESSAGE.format(order_id)
        super(OrderNotFoundError, self).__init__(self.message, *args)