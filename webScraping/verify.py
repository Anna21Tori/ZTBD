import pandas as pd
from os import listdir
import os


def find_csv_filenames():
    suffix=".csv"
    filenames = listdir(os.getcwd())
    return [filename for filename in filenames if filename.endswith(suffix)]


def verify_length(filename):
    file = pd.read_csv(filename)
    length = len(file)
    if length != 1500:
        print(f"Number of lines: {length} in file: {filename}")


filenames = find_csv_filenames()
for name in filenames:
    verify_length(name)