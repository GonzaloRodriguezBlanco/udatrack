from typing import Final


class DuplicateOrderError(ValueError):
    MESSAGE: Final[str] = "Order with ID '{}' already exists."
    def __init__(self, order_id, *args):
        self.message = self.MESSAGE.format(order_id)
        super(DuplicateOrderError, self).__init__(self.message, *args)