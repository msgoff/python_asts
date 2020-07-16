from sys import argv

import pandas as pd

#argv[1] filename of csv from ast_test.py
from file_utils import get_file_type

file_type = get_file_type(argv[1])
if file_type == b'application/csv':
    df = pd.read_csv(argv[1])
    function_names = set(df[df.type=='FunctionDef'].name.tolist())
    functions_called = set(df[df.type=='call'].name.tolist())
    len(function_names.difference(functions_called))
    for ix in function_names:
        if ix not in functions_called:
            if 'self.{}'.format(ix) not in functions_called:
                print(ix)
