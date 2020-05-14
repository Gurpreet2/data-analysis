from model.datasets import DataCollection
from config.settings import max_directory_traverse
import csv
from pathlib import Path, PosixPath
from os.path import normpath
import hashlib


def get_all_data_files(root_data_dir: str = '../data'):
    """
    This piece code retrieves all the files that may be used for analysis. It searches recursively for all files
    in the `root_data_dir` directory. Additionally, a dictionary with id->file is created for quick file lookup.
    Returns two things:
        a list of the files in dictionary format (let's call it file_object)
        a dictionary of the files, where key=id, and value=file_object
    Where file_object = {
        "id" -> file id, currently just a hash of the filename
        "name" -> filename, includes path to file from data dictionary
        "path" -> actual path to file
        "data_collection" -> data that was in the file
    }
    """
    root_data_dir = normpath(root_data_dir)
    files = []
    files_dict = {}
    for x in get_every_file_in_dir(root_data_dir):
        file_obj = {
            "id": hashlib.sha256(str(x).encode()).hexdigest(),
            "name": str(Path(*x.parts[root_data_dir.count('/') + 1:])),
            "path": str(x),
            "data_collection": read_csv_file_into_json(str(x))
        }
        files.append(file_obj)
        files_dict[file_obj['id']] = file_obj
    return files, files_dict


def get_every_file_in_dir(root_directory: str) -> [PosixPath]:
    """
    Returns a list of all the files in the specified directory as `Path` objects.
    Includes files in child directories, and uses breadth-first traversal to search directories.
    """
    directories = [Path(root_directory)]
    files = []
    i = 0
    while i < len(directories):
        if i > max_directory_traverse:
            raise RecursionError(f'Maximum allowed directory count traversed ({max_directory_traverse}). '
                                 f'At least {len(directories) - i} more directories remaining.')
        for item in directories[i].iterdir():
            if item.is_dir():
                directories.append(item)
            else:
                files.append(item)
        i += 1
    return files


def read_csv_file_into_json(file: str) -> [{}]:
    """
    Reads a csv file, and converts each row into a json object, with the header row being the keys.
    Returns the data in a `DataCollection` object.
    """
    contents = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = next(csv_reader)
        data_obj = {}
        for column_name in header:
            data_obj[column_name] = ''
        for row in csv_reader:
            copy_obj = data_obj.copy()
            for i in range(len(header)):
                copy_obj[header[i]] = row[i]
            contents.append(copy_obj)
    return DataCollection(header, contents)
