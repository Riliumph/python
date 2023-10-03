import sys
import pandas as pd
import tabula

args = sys.argv

if len(args) != 2:
    print("args error")
    exit()

dfs = tabula.read_pdf(args[1], lattice=True, pages='all')
odf = pd.DataFrame()
for df in dfs:
    odf = pd.concat([odf, df.dropna()])

cols = ["銘柄名", "新証券コード", "合計売残", "合計売残前週比", "合計買残", "合計買残前週比", "一般売残",
        "一般売残前週比", "制度売残", "制度売残前週比", "一般買残", "一般買残前週比", "制度買残", "制度買残前週比"]
odf.columns = cols

odf = odf.map(lambda x: x.replace('▲ ', '-'))
odf = odf.map(lambda x: x.replace(',', ''))

odf = odf[odf.iloc[:, 0].str.contains('普通株式', na=False)]
odf["銘柄名"] = odf["銘柄名"].str.replace("B\s*", "", regex=True)
odf["銘柄名"] = odf["銘柄名"].str.replace("\s.*$", "", regex=True)

odf.to_csv("output.csv", index=False)
