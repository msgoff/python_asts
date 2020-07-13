import pygraphviz as pgv
import pandas as pd 

# read CSV file (argument 1) and produce DOT+PNG (argument 2)

df = pd.read_csv(argv[1])
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

G.write(argv[2] + ".dot")`b`
G.layout(prog='dot')
G.draw(argv[2] + '.png') 
