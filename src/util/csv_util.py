import csv


def get_reader(filepath: str, delim: str):
    """It returns the file handler and a csv reader using the input delimiter."""
    file = open(filepath, 'r', newline='')
    reader = csv.reader(file, delimiter=delim)
    return file, reader


def get_writer(filepath: str, delim: str, write_mode: str):
    """It returns the file handler and a csv writer using the input delimiter."""
    file = open(filepath, write_mode, newline='')
    writer = csv.writer(file, delimiter=delim, dialect='excel')
    return file, writer
