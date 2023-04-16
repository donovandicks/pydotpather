from enum import Enum
from typing import Dict


class DiffType(str, Enum):
    ADDED = "added"
    MODIFIED = "modified"
    REMOVED = "removed"


def get_diff(first: Dict, second: Dict) -> Dict:
    """
    Get the diff between two dot-pathed dictionaries.

    If a key does not appear in the output diff, then no chanegs were found for that key.

    Parameters
    ----------
    first: Dict
        a dot-pathed dictionary, referred to as "first" in the diff output
    second: Dict
        a dot-pathed dictionary, referred to as "second" in the diff output

    Returns
    -------
    Dict
        a dictionary containing the diff between the two objects in the form:
        {
            "key": {
                "first": value,
                "second": value,
                "diff_type": "added | modified | removed",
            },
        }

    Example
    -------
    ```py
    from dotpather import get_diff

    x = {
        "a": 1,
        "b[0]": 2,
        "c.d": 3,
    }

    y = {
        "a": 1,
        "b[0]": 8,
        "c": 9,
    }

    diff = get_diff(first=x, second=y)
    assert diff == {
        "b[0]": {
            "first": 2,
            "second": 8,
            "diff_type": "modified",
        },
        "c": {
            "first": None,
            "second": 9,
            "diff_type": "added",
        },
        "c.d": {
            "first": 3,
            "second": None,
            "diff_type": "removed",
        },
    }
    ```
    """
    diff = {}
    for key in set((*first.keys(), *second.keys())):
        if key in first and key not in second:
            diff_record = {
                "first": first[key],
                "second": None,
                "diff_type": DiffType.REMOVED,
            }
        elif key in second and key not in first:
            diff_record = {
                "first": None,
                "second": second[key],
                "diff_type": DiffType.ADDED,
            }
        elif first[key] != second[key]:
            diff_record = {
                "first": first[key],
                "second": second[key],
                "diff_type": DiffType.MODIFIED,
            }
        else:
            continue

        diff[key] = diff_record

    return diff
