# python

## jupyter notebook

<http://localhost:8888/tree?>

## supervisorの設定について

Linuxの文化に則るなら、以下の設定になる。  
正しい管理パスにファイルを配置してログを出力する。

```config
[supervisord]
pidfile=/var/run/supervisor/supervisord.pid
logfile=/var/run/log/supervisord.log
```

Dockerの文化では、状態はコンテナに格納せずに一時ディレクトリに保管する。  
よって、`pid`ファイルは`/var/run/supervisor`ではなく`/tmp`に格納されるし、  
ログはファイルではなくstdoutに出力して`docker log <container>`で確認する。

```config
[supervisord]
pidfile=/var/run/supervisor/supervisord.pid
logfile=/var/run/log/supervisord.log
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
