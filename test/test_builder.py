import pytest
from pytest_examples import CodeExample, EvalExample, find_examples


def test_builder_one_layer(pb):
    d = {"a": 1, "b": 2, "c": 3}

    assert pb.build_paths(d) == d


def test_builder_two_layers(pb):
    d = {"a": {"b": 2}}

    assert pb.build_paths(d) == {"a.b": 2}


def test_builder_three_layers(pb):
    d = {"a": {"b": {"c": 3}}}

    assert pb.build_paths(d) == {"a.b.c": 3}


def test_builder_eight_layers(pb):
    d = {"a": {"b": {"c": {"d": {"e": {"f": {"g": {"h": 8}}}}}}}}

    assert pb.build_paths(d) == {"a.b.c.d.e.f.g.h": 8}


def test_builder_with_sequence(pb):
    d = {"a": [0, 1, 2]}

    assert pb.build_paths(d) == {"a[0]": 0, "a[1]": 1, "a[2]": 2}


def test_builder_with_subsurface_sequence(pb):
    d = {"a": {"b": [0, 1, 2]}}

    assert pb.build_paths(d) == {"a.b[0]": 0, "a.b[1]": 1, "a.b[2]": 2}


def test_builder_with_sequence_of_dicts(pb):
    d = {"a": [{"b": 0}, {"c": 1}]}

    assert pb.build_paths(d) == {"a[0].b": 0, "a[1].c": 1}


def test_builder_with_sequence_of_sequence(pb):
    d = {"a": [0, [1], [2, [3]]]}

    assert pb.build_paths(d) == {"a[0]": 0, "a[1][0]": 1, "a[2][0]": 2, "a[2][1][0]": 3}


def test_builder_with_multiple_sub_structures(pb):
    d = {
        "a": [
            {
                "b": 1,
                "c": {
                    "d": 2,
                    "e": [
                        3,
                        {"f": 4},
                    ],
                },
            }
        ],
        "b": 5,
        "c": {
            "d": {
                "e": {
                    "f": [
                        "g",
                        {
                            "i": 6,
                            "j": [7, 8, 9],
                        },
                    ],
                },
            },
        },
    }

    assert pb.build_paths(d) == {
        "a[0].b": 1,
        "a[0].c.d": 2,
        "a[0].c.e[0]": 3,
        "a[0].c.e[1].f": 4,
        "b": 5,
        "c.d.e.f[0]": "g",
        "c.d.e.f[1].i": 6,
        "c.d.e.f[1].j[0]": 7,
        "c.d.e.f[1].j[1]": 8,
        "c.d.e.f[1].j[2]": 9,
    }


@pytest.mark.examples
@pytest.mark.parametrize(
    "example",
    find_examples("src/dotpather"),
    ids=str,
)
def test_docstrings(example: CodeExample, eval_example: EvalExample):
    eval_example.run(example)
