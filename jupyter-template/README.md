# jupyter-notebook template

Pythonをjupyter-notebookで開発する際のテンプレートプロジェクト

## ビルド方法

```console
$ docker compose --build
```

## 実行方法

```console
$ docker compose up -d
```

## jupyter-serverへのアクセス

### DockerDesktopからアクセスする

`Port(s)`の8888:8888からアクセスする。  

![Containers](./doc/docker_desktop/containers.png)

ただし、トークンが付与されていないのでログインページに飛ばされる。

![login](./doc/docker_desktop/login.png)

### DockerDesktopからURLを取得する

jupyter-notebookを立ち上げた際にはトークン付きのURLが取得できる。

![Logs](./doc/docker_desktop/note_contaiener_log.png)
