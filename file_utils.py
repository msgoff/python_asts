def listfiles(folder):
    import os

    for root, folders, files in os.walk(folder):
        for filename in folders + files:
            if filename.endswith(".py"):
                yield os.path.join(root, filename)


def read_file(filename):
    # https://github.com/jendrikseipp/vulture
    # vulture - Find dead code.
    # Python >= 3.2
    import tokenize

    try:
        # Use encoding detected by tokenize.detect_encoding().
        with tokenize.open(filename) as f:
            return f.read()
    except (SyntaxError, UnicodeDecodeError) as err:
        print(err)


def get_file_type(filename):
    # https://stackoverflow.com/a/24073625
    import subprocess
    import shlex

    cmd = shlex.split("file --mime-type {0}".format(filename))
    result = subprocess.check_output(cmd)
    mime_type = result.split()[-1]
    return mime_type


def process_file(file_name, output_file):
    import ast
    from ast_test import FuncLister
    import pandas as pd

    data = read_file(file_name)
    tree = ast.parse(data)
    X = FuncLister()
    X.visit(tree)
    df = X.output_DataFrame()
    if len(df) > 0:
        # df = X.filters(df, "name", "")
        df["file_name"] = str(file_name)
        df.sort_values("line_no", inplace=True)
        print(df)
        try:
            temp_df = pd.read_csv(output_file)
        except:
            temp_df = pd.DataFrame()
            temp_df = pd.concat([df, temp_df])
            temp_df.sort_values(["file_name", "line_no", "col_offset"], inplace=True)
            temp_df.to_csv(output_file, index=False)
