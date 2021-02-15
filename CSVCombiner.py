import pandas as pd
import os.path
from os import path


class CSVCombiner:
    def __init__(self, system_args=None):
        if system_args is None:
            self.system_args = []
        else:
            self.system_args = system_args[1:]

    # Validate correct arguments are getting passed.
    def validate_input(self):
        if len(self.system_args) < 1:
            return False
        else:
            return True

    # Validate the files passed as argument exists.
    # Doing this to check if all files exist before the program starts combining other files.
    # RETURN => (BOOLEAN, FILE_NAME)
    def validate_directory(self):
        for i in self.system_args:
            if not path.exists(i):
                return (False, i)
        return (True, None)

    # Combine CSV files together.
    def combine_csv(self):
        for index, files in enumerate(self.system_args):
            if index == 0:
                print('email_hash,category,filename')
            file_name = files.split('/')[-1]

            # Reference: https://pythonspeed.com/articles/chunking-pandas/
            for chunks in pd.read_csv(files, chunksize=100000):
                chunks[file_name] = file_name
                print(chunks.to_csv(header=False, index=False,
                                    chunksize=100000), end='')

    def csv_combine(self):
        if self.validate_input():
            dir_validation = self.validate_directory()

            if dir_validation[0]:
                self.combine_csv()
            else:
                print('File: ' + dir_validation[1] + ' not found.', end='')
        else:
            print('Please input correct arguments.', end='')
