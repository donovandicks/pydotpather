"""Build dotpaths from dictionaries."""

from typing import Dict, List, Set, Union


def parse_seq(seq: Union[List, Set], parent_key: str) -> Dict:
    """
    Parse a sequence of items recursively.

    Parameters
    ----------
    seq: List | Set
        a sequence of items which may themselves be sequences or dictionaries
    parent_key: str
        the key of the current sequence

    Return
    ------
    Dict
        a dictionary where the keys begin with `parent_key[index]` and map to the values
        within the sequence

    Examples
    --------
    ```py
    from dotpather.builder import parse_seq

    assert parse_seq(seq=[1, 2, 3], parent_key="items") == {
        "items[0]": 1,
        "items[1]": 2,
        "items[2]": 3
    }
    ```
    """
    output = {}
    for idx, elm in enumerate(seq):
        new_key = f"{parent_key}[{idx}]"
        if isinstance(elm, Dict):
            output.update(parse_dict(elm, parent_key=new_key))
        else:
            output[new_key] = elm
    return output


def parse_dict(map: Dict, parent_key: str) -> Dict:
    """
    Parse a dictionary of items recursively.

    Parameters
    ----------
    map: Dictionary
        a dictionary of items which may have values of any type
    parent_key: str
        the key of the current sequence

    Return
    ------
    Dict
        a dictionary where the keys begin with `parent_key` and map to the values within
        the dictionary

    Examples
    --------
    ```py
    from dotpather.builder import parse_dict

    assert parse_dict(map={"a": 1, "b": 2, "c": 3}, parent_key="items") == {
        "items.a": 1,
        "items.b": 2,
        "items.c": 3
    }
    ```
    """
    output = {}
    for key, val in map.items():
        new_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(val, Dict):
            output.update(parse_dict(val, parent_key=new_key))
        elif isinstance(val, (List, Set)):
            output.update(parse_seq(val, parent_key=new_key))
        else:
            output[new_key] = val
    return output


def build_paths(map: Dict) -> Dict:
    """
    Produce a dictionary with 0 depth mapping dotpaths to their nested values.

    Parameters
    ----------
    map: Dict
        a dictionary to be converted into dotpath notation

    Returns
    -------
    Dict
        a 0-depth dictionary with keys in dot notation

    Examples
    --------
    ```py
    from dotpather import build_paths

    obj = {
        "a": 1,
        "b": [2, 3, 4],
        "c": {
            "d": 5,
            "e": [6],
        }
    }

    assert build_paths(obj) == {
        "a": 1,
        "b[0]": 2,
        "b[1]": 3,
        "b[2]": 4,
        "c.d": 5,
        "c.e[0]": 6,
    }
    ```
    """
    output = {}
    for key, val in map.items():
        if isinstance(val, Dict):
            output.update(parse_dict(val, parent_key=key))
        elif isinstance(val, (List, Set)):
            output.update(parse_seq(val, parent_key=key))
        else:
            output[key] = val

    return output
