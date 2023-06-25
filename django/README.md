# Djangoのサンプル

## Build

```console
$ docker compose build
```

## プロジェクト作成

```console
$ docker compose run backend django-admin startproject backend .
```

ただし、`backend`サービスが`root`ユーザーのため、作られるファイルも`root`権限となっている。

```console
sudo chown -R "$USER:$USER" .
```

## 実行

```console
$ docker compose up -d
```

## 削除

```console
$ docker compose down
```
