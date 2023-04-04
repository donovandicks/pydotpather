"""Build dotpaths from dictionaries."""

from typing import Dict, List, Set, Union


def parse_seq(s: Union[List, Set], parent_key: str) -> Dict:
    output = {}
    for i, e in enumerate(s):
        new_key = f"{parent_key}[{i}]"
        if isinstance(e, Dict):
            output.update(parse_dict(e, parent_key=new_key))
        else:
            output[new_key] = e
    return output


def parse_dict(d: Dict, parent_key: str) -> Dict:
    output = {}
    for k, v in d.items():
        new_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, Dict):
            output.update(parse_dict(v, parent_key=new_key))
        elif isinstance(v, (List, Set)):
            output.update(parse_seq(v, parent_key=new_key))
        else:
            output[new_key] = v
    return output


def build_paths(d: Dict) -> Dict:
    output = {}
    for k, v in d.items():
        if isinstance(v, Dict):
            output.update(parse_dict(v, parent_key=k))
        elif isinstance(v, (List, Set)):
            output.update(parse_seq(v, parent_key=k))
        else:
            output[k] = v

    return output
