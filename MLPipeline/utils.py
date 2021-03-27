import asyncio
from collections import Counter
from typing import List


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


def list_of_dicts_to_dict(my_list: List[dict]) -> dict:
    """Voodoo magic which fixes weirdly defined yaml in assignment. """

    return {list(item.keys())[0]: item[list(item.keys())[0]]
            for item in my_list if type(item) is dict and len(list(item.keys())) == 1}
