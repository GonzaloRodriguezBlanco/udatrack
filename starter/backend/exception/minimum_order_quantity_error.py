from typing import Final


class MinimumOrderQuantityError(ValueError):
    MESSAGE: Final[str] = 'Minimum quantity value allowed {}, {} given.'
    def __init__(self, min_allowed, quantity, *args):
        self.message = self.MESSAGE.format(min_allowed, quantity)
        super(MinimumOrderQuantityError, self).__init__(self.message, *args)
