# requirements.txtの内容

## インストール場所

```console
root@84cb5cbb5e9e:/code# pip show Django
Name: Django
Version: 4.1.2
Summary: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
Home-page: <https://www.djangoproject.com/>
Author: Django Software Foundation
Author-email: <foundation@djangoproject.com>
License: BSD-3-Clause
Location: /usr/local/lib/python3.11/site-packages
Requires: asgiref, sqlparse
Required-by: djangorestframework
```

`/usr/local/lib/python3.11/site-packages`であることが確認できた。  
特に、共有ボリュームが汚されることはない

## インストールライブラリ

- autopep8
- Django  
  バックエンドフレームワーク
- djangorestframework  
  REST API用ライブラリ
- python-json-logger  
  構造化ログ用のライブラリ
-
