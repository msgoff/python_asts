zf = df.groupby("call", as_index=False)["fn"].agg(lambda x: list(x))
zf["fn"] = zf["fn"].apply(lambda x: list(x))
zf.sort_values("call_count", inplace=True)
zf["call_count"] = zf["fn"].apply(lambda x: len(x))
zf.sort_values("call_count", inplace=True)
zf["fn"] = zf.fn.apply(lambda x: [(y, x.count(y)) for y in set(x)])
