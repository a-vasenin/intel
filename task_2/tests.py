import pytest

from merge import merge


def make_generator(values):
    for i in values:
        yield i


@pytest.fixture()
def iterator_with_three_values():
    values = [1, 5, 9]
    return make_generator(values)


@pytest.fixture()
def iterator_with_two_values():
    values = [2, 5]
    return make_generator(values)


@pytest.fixture()
def iterator_with_four_values():
    values = [1, 6, 10, 11]
    return make_generator(values)


@pytest.fixture()
def iterator_with_one_value():
    values = [5, ]
    return make_generator(values)


@pytest.fixture()
def empty_iterator():
    values = []
    return make_generator(values)


def test_multiple_iterators(iterator_with_three_values, iterator_with_two_values, iterator_with_four_values):
    generator = merge(iterator_with_three_values, iterator_with_two_values, iterator_with_four_values)
    extracted_values = [i for i in generator]
    assert extracted_values == [1, 1, 2, 5, 5, 6, 9, 10, 11]


def test_one_iterator(iterator_with_four_values):
    generator = merge(iterator_with_four_values)
    extracted_values = [i for i in generator]
    assert extracted_values == [1, 6, 10, 11]


def test_iterator_with_one_value(iterator_with_one_value):
    generator = merge(iterator_with_one_value)
    extracted_values = [i for i in generator]
    assert extracted_values == [5]


def test_empty_iterator(empty_iterator):
    generator = merge(empty_iterator)
    extracted_values = [i for i in generator]
    assert extracted_values == [None]
