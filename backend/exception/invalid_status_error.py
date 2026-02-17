from typing import Final


class InvalidStatusError(ValueError):
    MESSAGE: Final[str] = "Not a valid status. Allowed values '{}' but '{}' given."

    def __init__(self, initial_statuses_allowed, status, *args):
        self.message = self.MESSAGE.format(", ".join(initial_statuses_allowed), status)
        super(InvalidStatusError, self).__init__(self.message, *args)

