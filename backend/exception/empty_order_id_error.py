from typing import Final


class EmptyOrderIdError(ValueError):
    MESSAGE: Final[str] = "'order_id' cannot be empty."
    def __init__(self, *args):
        super(EmptyOrderIdError, self).__init__(self.MESSAGE, *args)