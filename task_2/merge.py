def merge(*args):
    merged_list = []
    for arg in args:
        arg = [i for i in arg]
        merged_list.extend(arg)
    return sorted(merged_list)


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
    merged = merge(iterable_1(), iterable_2(), iterable_3())
    print(merged)
