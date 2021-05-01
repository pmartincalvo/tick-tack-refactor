from typing import Callable


def input_with_validation(prompt: str, validation_func: Callable, retry: bool) -> str:
    """
    Get input from CLI. Validate it with passed function, and on fail, either
    raise an error or try again.
    :param prompt: The prompt that will be shown in the CLI.
    :param validation_func: A function that takes the value and returns a bool
    value indicating if it's valid.
    :param retry: Whether to retry or not.
    :return: The received, valid value.
    :raises: ValueError if no retry is allowed and the value is not valid.
    """

    while True:
        received_value = input(__prompt=prompt)
        is_valid = validation_func(received_value)
        if is_valid:
            return received_value

        if not retry:
            raise ValueError(f"{received_value} is not valid.")

        print("Value is not valid. Please, try again.")
