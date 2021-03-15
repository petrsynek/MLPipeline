import asyncio
from collections import Counter


def is_subset_of(is_this: list, in_that: list) -> bool:
    """checks if this is subset of that for lists"""
    count_in_this = Counter(is_this)
    count_in_that = Counter(in_that)

    # checking if element exists in second list
    for key in count_in_this:
        if key not in count_in_that:
            return False
    return True


def fire_and_forget(f):
    """self explaining wrapper"""

    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, *kwargs)

    return wrapped
