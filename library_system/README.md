# Djangoのサンプル

以下の順番で実行する

- [環境の整備](#ライブラリのインストール)
- [環境の起動](#起動)
- [Djangoサーバーの実行](#プロジェクトの実行)
- [任意のAPI](http://localhost:8000/api/v1/users)にアクセスする。  

## ライブラリのインストール

```console
$ pip install -r requirements.txt
```

## Djangoコマンド

### プロジェクトの作成

```console
$ docker compose run -u django backend django-admin startproject <pj-name> .
```

### アプリの作成

```console
$ python manage.py startapp <app-name>
```

### プロジェクトの実行

> 実行する前にDBのコンテナを立ち上げておく必要がある

```console
$ python manage.py runserver 0.0.0.0:8000
```

もしくは

F5デバッグで起動可能

## Docker環境について

### ビルド

```console
$ docker compose build
```

### 起動

```console
$ docker compose up -d
```

### 削除

```console
$ docker compose down
```

### DBへの接続

直接DBコンテナに入る場合は、`-h`オプションを省略できる。

```console
$ docker compose exec -it db psql -U postgres
```

以下の環境変数がホスト側（psql実行側）に存在する場合、ユーザーなどの指定は必要ない。

環境変数名|例|説明
:--|:--|:--
`PGHOST`|localhost, 0.0.0.0|接続先IPやホスト名
`PGPORT`|5432|ポート番号
`PGDATABASE`|postgres|接続先DB名
`PGUSER`|postgres|ログインユーザー名
`PGPASSWORD`|postgres|ログインパスワード
