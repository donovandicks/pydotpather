"""Build dotpaths from dictionaries."""

from typing import Any, Dict, Iterable, List, Set, Tuple, Union


def _iter_map(obj: Dict) -> Iterable[Tuple[Any, Any]]:
    for key, val in obj.items():
        yield (key, val)


def _make_map_key(parent_key: str, key: str) -> str:
    return f"{parent_key}.{key}"


def _iter_seq(obj: Union[List, Set]) -> Iterable[Tuple[int, Any]]:
    for idx, elm in enumerate(obj):
        yield (idx, elm)


def _make_seq_key(parent_key: str, idx: int) -> str:
    return f"{parent_key}[{idx}]"


def _build_paths(obj: Union[Dict, List, Set], parent_key: str) -> Dict:
    output = {}
    if isinstance(obj, Dict):
        iterator = _iter_map
        key_maker = _make_map_key
    else:
        iterator = _iter_seq
        key_maker = _make_seq_key

    for key, val in iterator(obj):
        new_key = key_maker(parent_key, key)
        if isinstance(val, Dict):
            output.update(_build_paths(val, parent_key=new_key))
        elif isinstance(val, (List, Set)):
            output.update(_build_paths(val, parent_key=new_key))
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
        if not isinstance(val, (Dict, List, Set)):
            output[key] = val
        else:
            output.update(_build_paths(val, parent_key=key))

    return output
