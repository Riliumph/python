# Djangoのサンプル

## Build

```console
$ docker compose build
```

## プロジェクト作成

```console
$ docker compose run -u django backend django-admin startproject <pj-name> .
```

## 実行

実行前にプロジェクトを始動するコマンドを有効にする。

```yaml
    command: python3 manage.py runserver 0.0.0.0:8000
```

```console
$ docker compose up -d
```

## 削除

```console
$ docker compose down
```

## DBへの接続

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
