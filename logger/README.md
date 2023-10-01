# logger

Pythonのloggerについて遊んでみる場所。

Document群

- [Python](https://docs.python.org/ja/3/contents.html)
- [logging --- Python 用ロギング機能](https://docs.python.org/ja/3/library/logging.html)
- [logging.config --- ロギングの環境設定](https://docs.python.org/ja/3/library/logging.config.html)

## dictConfig

configは、色々な設定関数をコールしていって設定することもできる。  
しかし、それでは可搬性に難がある。（？）

そこでPythonは、辞書形式に設定が書かれていれば、その中から所定の設定項目を自動で当てはめてくれる機能を持っている。
それがdictConfigである。

この遊び場では、基本的にdictConfigによる設定を心がけている。
