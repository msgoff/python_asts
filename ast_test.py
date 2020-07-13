#!/usr/bin/env python3

# https://greentreesnakes.readthedocs.io/en/latest/manipulating.html
import ast
from sys import argv
import pandas as pd
from os import listdir

#def visit_alias(self,node): pass
#def visit_arg(self,node): pass
#def visit_arguments(self,node): pass
#def visit_Assert(self,node): pass
#def visit_Assign(self,node): pass
#def visit_AsyncFor(self,node): pass
#def visit_AsyncFunctionDef(self,node): pass
#def visit_AsyncWith(self,node): pass
#def visit_Attribute(self,node): pass
#def visit_AugAssign(self,node): pass
#def visit_Await(self,node): pass
#def visit_BinOp(self,node): pass
#def visit_BoolOp(self,node): pass
#def visit_Bytes(self,node): pass
#def visit_Call(self,node): pass
#def visit_ClassDef(self,node): pass
#def visit_Compare(self,node): pass
#def visit_comprehension(self,node): pass
#def visit_Constant(self,node): pass
#def visit_Delete(self,node): pass
#def visit_DictComp(self,node): pass
#def visit_Dict(self,node): pass
#def visit_ExceptHandler(self,node): pass
#def visit_Exec(self,node): pass
#def visit_Expression(self,node): pass
#def visit_Expr(self,node): pass
#def visit_ExtSlice(self,node): pass
#def visit_For(self,node): pass
#def visit_FunctionDef(self,node): pass
#def visit_GeneratorExp(self,node): pass
#def visit_Global(self,node): pass
#def visit_IfExp(self,node): pass
#def visit_If(self,node): pass
#def visit_ImportFrom(self,node): pass
#def visit_Import(self,node): pass
#def visit_Index(self,node): pass
#def visit_Interactive(self,node): pass
#def visit_keyword(self,node): pass
#def visit_Lambda(self,node): pass
#def visit_ListComp(self,node): pass
#def visit_List(self,node): pass
#def visit_Module(self,node): pass
#def visit_NameConstant(self,node): pass
#def visit_Name(self,node): pass
#def visit_Nonlocal(self,node): pass
#def visit_Num(self,node): pass
#def visit_Print(self,node): pass
#def visit_Raise(self,node): pass
#def visit_Repr(self,node): pass
#def visit_Return(self,node): pass
#def visit_SetComp(self,node): pass
#def visit_Set(self,node): pass
#def visit_Slice(self,node): pass
#def visit_Starred(self,node): pass
#def visit_Str(self,node): pass
#def visit_Subscript(self,node): pass
#def visit_Suite(self,node): pass
#def visit_TryExcept(self,node): pass
#def visit_TryFinally(self,node): pass
#def visit_Try(self,node): pass
#def visit_Tuple(self,node): pass
#def visit_UnaryOp(self,node): pass
#def visit_While(self,node): pass
#def visit_With(self,node): pass
#def visit_YieldFrom(self,node): pass
#def visit_Yield(self,node): pass


class FuncLister(ast.NodeVisitor):
    lst = []

    def visit_Name(self, node):
        self.generic_visit(node)

    def visit_Attribute(self, node):
        self.generic_visit(node)

    def visit_Constant(self, node):
        self.generic_visit(node)

    def visit_arguments(self, node):
        self.generic_visit(node)

    def visit_arg(self, node):
        self.generic_visit(node)

    def visit_If(self, node):
        self.generic_visit(node)

    def visit_Try(self, node):
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.generic_visit(node)

    def visit_With(self, node):
        self.generic_visit(node)

    def visit_Call(self, node):
        self.generic_visit(node)

    def visit_alias(self, node):
        self.generic_visit(node)

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

def df_query(query_string, df):
    df[
        df.apply(
            lambda row: True
            if re.findall(query_string, str(row.astype(str)), re.IGNORECASE)
            else False,
            axis=1,
        )
    ]

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
    temp_df = pd.read_csv(argv[2])
except:
    temp_df = pd.DataFrame()
temp_df = pd.concat([df, temp_df])
temp_df.to_csv(argv[2], index=False)


