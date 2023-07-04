from typing import Union


def retrieve_first_item_otherwise_itself(target: Union[str, Union[tuple, list]]):
    if isinstance(target, str):
        return target
    else:
        return target[0]
