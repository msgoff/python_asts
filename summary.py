import pandas as pd
from file_utils import read_file
from sys import argv
import re

df = pd.read_csv(argv[1])
counts = df[df.type == "call"].name.value_counts()
zf = pd.DataFrame(counts)
zf.reset_index(inplace=True)
# print(df.name)


def show_references(name):
    temp_df = df[
        df.name.apply(lambda x: True if re.findall(name, str(x), re.I) else False)
    ]
    print(temp_df)
    X = temp_df.itertuples()
    while True:
        try:
            resp = next(X)[1:]
            line_no, _, _, _, file_path = resp
            data = read_file(file_path)
            readlines = data.splitlines()
            for ix, xs in enumerate(readlines):
                if ix == line_no - 1:
                    print(xs.strip(), "\n", "*" * 50, "\n")
        except StopIteration:
            break


indicies = zf.index.tolist()
print(indicies)
while True:
    try:
        print(zf)
        print("input ")
        inp = input()
        show_references(inp)
    except Exception as e:
        print(e)
        break
