from contextlib import ExitStack


def get_file_end_position(file_object):
    """
    Returns end file position.
    How it works:
    Well, I dont know how to get the length of the file while I dont read it all in memory,
    so here is some again invented wheels :)
    We remember the current position in file. We will return to it after we done here.
    We then get to the end of the file and remember this position too. This position will be used as file end position.
    Then we return to original remembered position in file, as nothing has happened :)
    """
    current_position = file_object.tell()

    file_object.seek(0, 2)
    file_end = file_object.tell()
    file_object.seek(current_position)

    return file_end


def generate_line(file_object):
    """Return next line from file."""
    file_end_position = get_file_end_position(file_object)

    if file_object.tell() == file_end_position:
        file_object.seek(0)

    return file_object.readline().strip()


def return_lines(files: list):
    """Yield next line for each file in the 'files' list."""
    for file_object in files:
        generated_line = generate_line(file_object)
        
        yield generated_line


def multiplex_files(filenames: list, infinite=True, loops=5):
    """
    :param filenames: list with filenames.
    :param infinite: if True, invokes infinite loop.
    :param loops: if infinite=False, invokes as much loops as passed in parameter.

    Open files from the list 'filenames' in context manager. Multiplex lines from these files one-by-one.
    """
    with ExitStack() as stack:
        files = [stack.enter_context(open(filename)) for filename in filenames]

        if infinite:
            while True:
                yield return_lines(files)
        else:
            for i in range(loops):
                yield return_lines(files)


if __name__ == '__main__':
    filenames = ['file_1', 'file_2', 'file_3']
    multiplexed_lines = [[k for k in i] for i in multiplex_files(filenames, infinite=False)]
    
    print(multiplexed_lines)
