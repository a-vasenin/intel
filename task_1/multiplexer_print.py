from contextlib import ExitStack


def get_file_end_position(file_object):
    current_position = file_object.tell()

    file_object.seek(0, 2)
    file_end = file_object.tell()
    file_object.seek(current_position)

    return file_end


def generate_line(file_object):
    file_end_position = get_file_end_position(file_object)

    if file_object.tell() == file_end_position:
        file_object.seek(0)
    return file_object.readline().strip()


def multiplex_files(files_list, infinite=True, loops=5):
    with ExitStack() as stack:
        files = [stack.enter_context(open(filename)) for filename in files_list]

        def return_lines():
            for file_object in files:
                generated_line = generate_line(file_object)
                
                print(generated_line)

        if infinite:
            while True:
                return_lines()
        else:
            for i in range(loops):
                return_lines()


filenames = ['file_1', 'file_2', 'file_3']
if __name__ == '__main__':
    multiplex_files(filenames, infinite=False)
