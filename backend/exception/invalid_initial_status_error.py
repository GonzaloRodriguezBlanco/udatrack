from typing import Final


class InvalidInitialStatusError(ValueError):
    MESSAGE: Final[str] = "Invalid initial status, allowed '{}' but  '{}' given."

    def __init__(self, initial_statuses_allowed, status, *args):
        self.message = self.MESSAGE.format(", ".join(initial_statuses_allowed), status)
        super(InvalidInitialStatusError, self).__init__(self.message, *args)

