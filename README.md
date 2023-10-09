# python

## jupyter notebookの起動

- コンテナはSystemdなどは使えない
- `postCreatedCommand`で実行すると、そのコマンドで以降が実行されないのでdotfilesがインストールされない。

```console
$ jupyter notebook --no-browser --allow-root --ip=0.0.0.0 --port=8888 --NotebookApp.token='' &
```

## >>> ImportError: No module named xxx

jupyterを起動した後にpipでインストールした場合に上記エラーが発生する。  
jupyterは、kernelが起動されるときにライブラリのパスを読み込む。

### ライブラリパスの確認

```python
import sys
import pprint

pprint.pprint(sys.path)
```

- '/python/pdf2csv/src',
- '',
- '/usr/local/lib/python311.zip'
- '/usr/local/lib/python3.11'
- '/usr/local/lib/python3.11/lib-dynload'
- '/usr/local/lib/python3.11/site-packages'

`pip`したのがユーザーであるならば、以下のパスを組み込む必要がある。  

> `devcontainer.json`に記載している。
