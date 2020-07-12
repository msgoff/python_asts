# https://greentreesnakes.readthedocs.io/en/latest/manipulating.html
import ast
from sys import argv
import pandas as pd
from os import listdir


class FuncLister(ast.NodeVisitor):
    lst = []

    def visit_ImportFrom(self, node):
        resp = (
            node.lineno,
            node.col_offset,
            "importFrom",
            (node.module, node.names[0].name),
        )
        self.lst.append(resp)
        self.generic_visit(node)

    def visit_Import(self, node):
        print(node.names[0].__dict__)
        if node.names[0].asname:
            resp = (
                node.lineno,
                node.col_offset,
                "import",
                node.names[0].name + " as " + node.names[0].asname,
            )
        else:
            resp = (node.lineno, node.col_offset, "import", node.names[0].name)
        self.lst.append(resp)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        resp = (
            node.__dict__["lineno"],
            node.__dict__["col_offset"],
            "ClassDef",
            node.name,
        )
        self.lst.append(resp)
        docstring = self.get_docstring(node)
        if docstring:
            self.lst.append(docstring)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        resp = (
            node.__dict__["lineno"],
            node.__dict__["col_offset"],
            "FunctionDef",
            node.name,
        )
        self.lst.append(resp)
        docstring = self.get_docstring(node)
        if docstring:
            self.lst.append(docstring)
        self.generic_visit(node)

    def visit_Call(self, node):
        dct = node.__dict__["func"].__dict__
        if "id" in dct.keys():
            resp = (dct["lineno"], dct["col_offset"], "call", dct["id"])
            self.lst.append(resp)
        elif "value" in dct.keys():
            dct_v1 = dct["value"].__dict__
            if "id" in dct_v1.keys():
                if "attr" in dct.keys():
                    resp = (
                        dct_v1["lineno"],
                        dct_v1["col_offset"],
                        "call",
                        dct_v1["id"] + "." + dct["attr"],
                    )
                else:
                    resp = (
                        dct_v1["lineno"],
                        dct_v1["col_offset"],
                        "call",
                        dct_v1["id"],
                    )
                self.lst.append(resp)
        self.generic_visit(node)

    def get_docstring(self, node):
        "get the docstrings"
        if (
            isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module))
            and node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Str)
        ):
            return (
                node.lineno,
                node.col_offset,
                "docstring",
                node.body[0].value.s,
            )

    def filters(self, df, column, pattern):
        import pandas as pd
        import re

        df.loc[:, column] = df.loc[:, column][
            df.loc[:, column].apply(
                lambda x: True if not re.findall(pattern, str(x)) else False
            )
        ]
        df.dropna(subset=[column], inplace=True)
        return df

    def output_DataFrame(self):
        import pandas as pd

        df = pd.DataFrame(self.lst)
        df.columns = ["line_no", "col_offset", "type", "name"]
        return df


def read_file(file_name):
    with open(file_name, "r") as f:
        data = f.read()
    return data


data = read_file(argv[1])
tree = ast.parse(data)
X = FuncLister()
X.visit(tree)
df = X.output_DataFrame()
# df = X.filters(df, "name", "")
df["file_name"] = str(argv[1])
df.sort_values("line_no", inplace=True)
print(df)

try:
    temp_df = pd.read_csv("output.csv")
except:
    temp_df = pd.DataFrame()
temp_df = pd.concat([df, temp_df])
temp_df.to_csv("output.csv", index=False)
