import os
import pytest

from multiplexer import multiplex_files


def write_file(tmp_path, filename, content):
    filename = os.path.join(tmp_path, filename)
    with open(filename, 'w') as file:
        for line in content:
            file.write(line + '\n')
    return filename


@pytest.fixture
def file_with_numbers(tmp_path):
    filename = 'file_with_numbers'
    content = ['1', '2', '3']
    return write_file(tmp_path, filename, content)


@pytest.fixture
def file_with_letters(tmp_path):
    filename = 'file_with_letters'
    content = ['A', 'B', 'C', 'D']
    return write_file(tmp_path, filename, content)


@pytest.fixture
def file_with_symbols(tmp_path):
    filename = 'file_with_symbols'
    content = ['-', '+']
    return write_file(tmp_path, filename, content)


@pytest.fixture
def file_with_one_line(tmp_path):
    filename = 'file_with_one_line'
    content = ['line', ]
    return write_file(tmp_path, filename, content)


@pytest.fixture
def empty_file(tmp_path):
    filename = 'empty_file'
    content = ['', ]
    return write_file(tmp_path, filename, content)


@pytest.fixture
def file_with_empty_lines(tmp_path):
    filename = 'file_with_empty_lines'
    content = ['', 'line1', '', 'line2']
    return write_file(tmp_path, filename, content)


def test_one_file(file_with_letters):
    filenames = [file_with_letters, ]
    generator = multiplex_files(filenames, infinite=False, loops=5)
    extracted_values = [[i for i in j] for j in generator]
    assert extracted_values == [['A'], ['B'], ['C'], ['D'], ['A']]


def test_multiple_files(file_with_numbers, file_with_letters, file_with_symbols):
    filenames = [file_with_numbers, file_with_letters, file_with_symbols]
    generator = multiplex_files(filenames, infinite=False, loops=5)
    extracted_values = [[i for i in j] for j in generator]
    assert extracted_values == [['1', 'A', '-'], ['2', 'B', '+'], ['3', 'C', '-'], ['1', 'D', '+'], ['2', 'A', '-']]


def test_file_with_one_line(file_with_one_line):
    filenames = [file_with_one_line, ]
    generator = multiplex_files(filenames, infinite=False, loops=5)
    extracted_values = [[i for i in j] for j in generator]
    assert extracted_values == [['line'], ['line'], ['line'], ['line'], ['line']]


def test_file_with_empty_lines(file_with_empty_lines):
    filenames = [file_with_empty_lines, ]
    generator = multiplex_files(filenames, infinite=False, loops=5)
    extracted_values = [[i for i in j] for j in generator]
    assert extracted_values == [[''], ['line1'], [''], ['line2'], ['']]


def test_empty_file(empty_file):
    filenames = [empty_file, ]
    generator = multiplex_files(filenames, infinite=False, loops=5)
    extracted_values = [[i for i in j] for j in generator]
    assert extracted_values == [[''], [''], [''], [''], ['']]


def test_loops_number(file_with_one_line):
    filenames = [file_with_one_line, ]
    generator = multiplex_files(filenames, infinite=False, loops=10)
    extracted_values = [[i for i in j] for j in generator]
    assert extracted_values == [['line']] * 10


def test_no_file():
    try:
        filenames = ['file_not_exists', ]
        generator = multiplex_files(filenames, infinite=False, loops=10)
        extracted_values = [[i for i in j] for j in generator]
    except FileNotFoundError:
        pass
