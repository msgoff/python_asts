import pygraphviz as pgv
import pandas as pd 

df = pd.read_csv('/home/user/wipeq/output.csv')
G=pgv.AGraph(strict=False,directed=True)


for f_name in set(df['file_name'].tolist()):
    G.add_node(f_name)

for func_name in set(df['name'].tolist()):
    G.add_node(func_name)

X = df.itertuples()
while True:
    try:
        resp = next(X)[3:]
        G.add_edge(resp[2],resp[1],color=resp[0])
    except StopIteration:
        break

G.write("file.dot")`b`
G.layout(prog='dot')
G.draw('file.png') 
