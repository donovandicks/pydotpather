# DotPather

Convert Python dictionaries to one-level objects with JMESPath-compatible  keys.

## Example

Convert this:

```python
my_dict = {
  "a": [1, 2, 3],
  "b": {
    "c": 4,
    "d": 5,
  }
}
```

to this:

```python
{
  "a[0]": 1,
  "a[1]": 2,
  "a[2]": 3,
  "b.c": 4,
  "b.d": 5
}
```

## Usage

*This library is currently not available on PyPI*

You can install the library by cloning the repository and running:

```shell
make install
```

Then you can use it in your project like so:

```python
from dotpather import build_paths

pathed = build_paths(my_dict)
```

### Python Compatibility

Python >= 3.7
