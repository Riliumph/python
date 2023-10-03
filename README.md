# python

## jupyter notebookの起動

- コンテナはSystemdなどは使えない
- `postCreatedCommand`で実行すると、そのコマンドで以降が実行されないのでdotfilesがインストールされない。

```console
$ jupyter notebook --no-browser --allow-root --ip=0.0.0.0 --port=8888 --NotebookApp.token='' &
```
