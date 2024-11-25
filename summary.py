import pandas as pd
from file_utils import read_file
from sys import argv

df = pd.read_csv(argv[1])
counts = df[df.type == "call"].name.value_counts()
print(counts, "\n\n")


def show_references(name):

    X = df[df.name == name].itertuples()
    while True:
        try:
            resp = next(X)[1:]
            line_no, _, _, _, file_path = resp
            data = read_file(file_path)
            readlines = data.splitlines()
            for ix, xs in enumerate(readlines):
                if ix == line_no - 1:
                    print(xs.strip(), "\n\n", "*" * 50, "\n")
        except StopIteration:
            break


show_references("Config")
