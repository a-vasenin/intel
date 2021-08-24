def merge_sorted(*args):
    """Haha, that's probably not what you want :)"""
    merged_list = []
    for arg in args:
        arg = [i for i in arg]
        merged_list.extend(arg)
    return sorted(merged_list)


def merge(*args):
    """
    Get multiple sorted iterables, merge them into one (also sorted).
    How it works:
    We compare first (lesser) value from one iterator with first value from another.
    Then we return the lesser value and keep the greater.
    The greater we will compare with next element from another iterator.
    After all iterators are exhausted, we return the last (also greater) element.

    :param args: iterators with sorted numbers
    :return: generator with sorted numbers from multiple iterators
    """
    number_of_iterators = len(args)
    number_of_exhausted_generators = 0

    prev_value = None
    curr_value = None

    while True:
        for arg in args:
            try:
                if prev_value is None:
                    prev_value = next(arg)
                    continue
                else:
                    curr_value = next(arg)

                if prev_value <= curr_value:
                    yield prev_value
                    prev_value = curr_value
                else:
                    yield curr_value

            except StopIteration:
                number_of_exhausted_generators += 1
                pass
        # Well, its one of the ways to determine when all generators are exhausted
        if number_of_exhausted_generators == number_of_iterators:
            break
    # After all generators are exhausted, we should return the last (also the greater) element
    yield prev_value


if __name__ == '__main__':
    def iterable_1():
        for i in [1, 5, 9]:
            yield i

    def iterable_2():
        for i in [2, 5]:
            yield i

    def iterable_3():
        for i in [1, 6, 10, 11]:
            yield i

    merge_sorted = merge_sorted(iterable_1(), iterable_2(), iterable_3())
    print("merge_sorted: ", merge_sorted)

    merge = merge(iterable_1(), iterable_2(), iterable_3())
    print("merge: ", [i for i in merge])
