# 起動構成

## 実行コマンドで指定する

```console
$ jupyter notebook --NotebookApp.token=''
```

## Dockerfileとcomposeどっちに書く？

`Dockerfile`と`docker-compose.yaml`のどちらに書くべきだろうか？

### Dockerfile

Dockerfileは、コンテナの起動構成を構成管理する。  
認証系やネットワーク系も起動構成といえば起動構成だが、インフラや利用構成が変わるたびに無関係なDockerfileは修正したくない。

そこで、Dockerfileに書くべきは「**アプリケーションに閉じた設定**」のみとする

#### --no-browser

jupyter notebook起動時にブラウザを立ち上げるかどうかの設定。  
ローカル開発環境だと、jupyterを立ち上げたときにブラウザが立ち上がってくれると便利だが、サーバーとして利用したいのでオフにする。  

これはコンテナの起動方法に関わる設定のためDockerfile側に記載する。

#### --allow-root

jupyterをroot起動するのは非推奨であるため、オプションで明示しなければならない。  
rootユーザを用いるのか、専用ユーザを用いるのかはDockerfile（特に`USER`コマンド）に依存する内容である。

これはコンテナの起動方法に関わる設定のためDockerfile側に記載する。

### docker-compose.yaml

docker-compose.yamlは、インフラに関わる設定や実際の利用構成を管理する。

#### --ip

jupyterサーバーへの接続元IPアドレスを指定する。  
`--ip=*`は、すべてのリモートアクセスを許可する設定になる。  
`--ip=0.0.0.0`は、ローカルアクセスのみを許可する設定になる。

これはコンテナの利用設定のためdocker-compose.yaml側に記載する。

#### --NotebookApp.token

jupyterサーバのアクセスに必要なアクセストークンを指定する。  
`--NotebookApp.token=''`はトークンレスなサーバーを構築する。

これはコンテナの利用設定のためdocker-compose.yaml側に記載する。
