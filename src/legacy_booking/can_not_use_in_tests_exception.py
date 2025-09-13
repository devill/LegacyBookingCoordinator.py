"""Exception for classes that cannot be used in tests."""


class CanNotUseInTestsException(Exception):
    """Exception thrown when attempting to use production classes in tests."""

    def __init__(self, class_name: str) -> None:
        super().__init__(f"Cannot use {class_name} in tests - this class has external dependencies!")
        self.class_name = class_name