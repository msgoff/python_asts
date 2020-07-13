import pandas as pd 
df = pd.read_csv('output.csv')
df.head()
function_names = set(df[df.type=='FunctionDef'].name.tolist())
functions_called = set(df[df.type=='call'].name.tolist())
len(function_names.difference(functions_called))
for ix in function_names:
    if ix not in functions_called:
        if 'self.{}'.format(ix) not in functions_called:
            print(ix)
