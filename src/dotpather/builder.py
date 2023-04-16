"""Build dotpaths from dictionaries."""

from typing import Any, Dict, Iterable, List, Set, Tuple, TypeVar, Union

K = TypeVar("K")
V = TypeVar("V")


class PathBuilder:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _make_map_iter(map: Dict[K, V]) -> Iterable[Tuple[K, V]]:
        for key, val in map.items():
            yield (key, val)

    @staticmethod
    def _make_map_key(parent_key: str, key: str) -> str:
        return f"{parent_key}.{key}"

    @staticmethod
    def _make_seq_iter(seq: Union[List, Set]) -> Iterable[Tuple[int, Any]]:
        for idx, elm in enumerate(seq):
            yield (idx, elm)

    @staticmethod
    def _make_seq_key(parent_key: str, idx: int) -> str:
        return f"{parent_key}[{idx}]"

    def _build_paths(self, obj: Union[Dict, List, Set], parent_key: str) -> Dict:
        output = {}
        if isinstance(obj, Dict):
            iterator = self._make_map_iter
            key_maker = self._make_map_key
        else:
            iterator = self._make_seq_iter
            key_maker = self._make_seq_key

        for key, val in iterator(obj):
            new_key = key_maker(parent_key, key)
            if isinstance(val, Dict):
                output.update(self._build_paths(val, parent_key=new_key))
            elif isinstance(val, (List, Set)):
                output.update(self._build_paths(val, parent_key=new_key))
            else:
                output[new_key] = val

        return output

    def build_paths(self, map: Dict) -> Dict:
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
        from dotpather import PathBuilder

        obj = {
            "a": 1,
            "b": [2, 3, 4],
            "c": {
                "d": 5,
                "e": [6],
            }
        }

        pb = PathBuilder()
        assert pb.build_paths(obj) == {
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
                output.update(self._build_paths(val, parent_key=key))

        return output
