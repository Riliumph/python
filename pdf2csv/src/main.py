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
# grep 普通株式
odf = odf[odf.iloc[:, 0].str.contains('普通株式', na=False)]
# 銘柄名カラムを分割
split_df = odf['銘柄名'].str.split('普通株式', expand=True)
split_df.columns = ["銘柄名", "旧コード"]  # カラム名変更
# 元カラム削除
odf = odf.drop('銘柄名', axis=1)
# DF結合
odf = pd.concat([split_df, odf], axis=1)
odf["銘柄名"] = odf["銘柄名"].str.replace("B\s*", "", regex=True)
odf["銘柄名"] = odf["銘柄名"].str.replace("\s.*$", "", regex=True)
# 不必要データの削除
odf = odf.drop('合計売残', axis=1)
odf = odf.drop('合計売残前週比', axis=1)
odf = odf.drop('合計買残', axis=1)
odf = odf.drop('合計買残前週比', axis=1)

odf.to_csv("output.csv", index=False)
