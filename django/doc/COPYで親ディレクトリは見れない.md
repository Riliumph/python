# Dockerの注意点

## 前提

プロジェクトのディレクトリツリーが以下としよう。

```bash
project/
 ├ doc/
 ├ dockerfiles/
 │  ├ backend.dockerfile
 │  └ db.dockerfile
 ├ init/
 │  └ init.sql
 ├ docker-compose.yaml
 └ requirements.txt
```

`backend.dockerfile`には以下の内容が記述されている。

```Dockerfile
FROM python:3.11.4-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /code
# ライブラリのインストールを行う
COPY ../requirements.txt /code/
RUN pip install -r --no-cache-dir requirements.txt
COPY . /code/
```

```yaml
version: '3.8'
services:
  db:
  （略）
  backend:
    container_name: backend
    build:
      context: ./dockerfiles
      dockerfile: backend.dockerfile
    stdin_open: true # -i
    tty: true # -t
    ports:
      - target: 8000    # container
        published: 8000 # host
    volumes:
      - type: bind
        source: ./
        target: /code
    # command: python3 manage.py runserver 0.0.0.0:8000
```

## ビルドエラー

これをビルドすると以下のエラーが発生する。

```console
$ docker compose build
[+] Building 0.0s (0/1)
[+] Building 2.3s (8/9)
 => [internal] load .dockerignore                                       0.0s
 => => transferring context: 2B                                         0.0s
 => [internal] load build definition from backend.dockerfile            0.0s
 => => transferring dockerfile: 205B                                    0.0s
 => [internal] load metadata for docker.io/library/python:3.11.4-slim   0.7s
 => [internal] load build context                                       0.0s
 => => transferring context: 350B                                       0.0s
 => [1/5] FROM docker.io/library/python:3.11.4-slim@sha256:xxx          0.0s
 => CACHED [2/5] WORKDIR /code                                          0.0s
 => [3/5] COPY requirements.txt /code/                                  0.0s
 => ERROR [4/5] RUN pip install -r --no-cache-dir requirements.txt      1.6s
------
 > [4/5] RUN pip install -r --no-cache-dir requirements.txt:
#0 1.425 ERROR: Could not open requirements file: [Errno 2] No such file or directory: '--no-cache-dir'
[+] Building 0.0s (0/0)
failed to solve: process "/bin/sh -c pip install -r --no-cache-dir requirements.txt" did not complete successfully: exit code: 1
```

`requirements.txt`が見つからないそうだ。  

COPYに失敗しても、共有ボリューム張ってるじゃん！！と思うかもしれないが、共有ボリュームはコンテナ実行時に張られるものでビルド時には張られない。

## 解決策

基本的に、`Dockerfile`内で`Dockerfile`があるパスよりも前のパスを相対パスで参照することはできない模様。

しかし、`docker-compose.yaml`を使うと回避できる可能性がある。  
Dockerは`docker-compose.yaml`の`context`に書かれたディレクトリを基にしてコマンドを実行する。  
そのため、`context`が`./dockerfiles`の場合には、`dockerfiles`のディレクトリでdockerコマンドを実行している。  
そして、`Dockerfile`の仕様上、親ディレクトリを見ることはできない。

そこで、`context`を`root`にしてしまい、`docker build`コマンド時に参照するDockerfileを相対パスで渡すことで回避することができる。

```yaml
version: '3.8'
services:
  db:
  （略）
  backend:
    container_name: backend
    build:
      context: ./ # あくまでrootディレクトリを指定
      dockerfile: ./dockerfiles/backend.dockerfile # rootよりも深いパスを指定
    stdin_open: true # -i
    tty: true # -t
    ports:
      - target: 8000    # container
        published: 8000 # host
    volumes:
      - type: bind
        source: ./
        target: /code
    # command: python3 manage.py runserver 0.0.0.0:8000
```

## 参考

- [【Docker】COPYで指定されたファイルは、Dockerfileが存在するディレクトリからの相対パスで、親ディレクトリを見れない](https://scrapbox.io/taka521-tech-notes/%E3%80%90Docker%E3%80%91COPY%E3%81%A7%E6%8C%87%E5%AE%9A%E3%81%95%E3%82%8C%E3%81%9F%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AF%E3%80%81Dockerfile%E3%81%8C%E5%AD%98%E5%9C%A8%E3%81%99%E3%82%8B%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA%E3%81%8B%E3%82%89%E3%81%AE%E7%9B%B8%E5%AF%BE%E3%83%91%E3%82%B9%E3%81%A7%E3%80%81%E8%A6%AA%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA%E3%82%92%E8%A6%8B%E3%82%8C%E3%81%AA%E3%81%84)
- [docker-composeでADDやCOPYをする際に注意すること](https://qiita.com/mk-tool/items/1c7e4929055bb3b7aeda)
