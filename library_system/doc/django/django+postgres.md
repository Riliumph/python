# DjangoとPostgreSQLをつなぐには

## Djangoの設定

`setting.py`からDBの接続方法を変更する。

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'database_name',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'hostname',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}
```

## psycopg2のインストール

`psycopg2`は`libpq`のラッパーとして実装されている。  
よって、子のライブラリを使うには`libpq`が必要となる。

PostgreSQLがインストールされている環境では、自動的に所持しているので心配ない。  
PostgreSQLが別サーバーになっているような環境だと、別途インストールが必要である。

また、このライブラリをビルドする必要があるため、`gcc`も必要になる。

```console
$ sudo apt get install libpq-dev gcc
```

### psycopg2-binary

`psycopg2-binary`は、`psycopg2`と`libpq`などを静的リンクをして単体で動作できるようにしたバイナリライブラリである。  
インストールするだけで使えて便利だが、本番環境は非推奨らしい。

> [psycopg2 2.9.8](https://pypi.org/project/psycopg2/)  
> `$ pip install psycopg2-binary`  
> The binary package is a practical choice for development and testing but in production it is advised to use the package built from sources.
