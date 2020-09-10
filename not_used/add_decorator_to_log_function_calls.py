from ast_test import *
from file_utils import *
from sys import argv

file_name = argv[1]
x = FuncLister()

f = open(argv[1])
source_code = f.read()
f.close()


tree = ast.parse(source_code)
x.visit(tree)
df = x.output_DataFrame()
df = df[df.type == "FunctionDef"]
source_code = source_code.splitlines()
source_code.insert(0, "from logging_function_calls import *")

df.reset_index(inplace=True, drop=True)
counter = 1
for ix in range(len(df)):
    line = df.loc[ix]
    source_code.insert(line.line_no + ix, " " * line.col_offset + "@function_calls")


print("\n".join(source_code))
