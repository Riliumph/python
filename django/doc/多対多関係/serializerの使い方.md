# 多対多でのserializerの使い方

このシリアライザの実装だとする。

```python
class BookSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = BookEntity
        fields = '__all__'
```

BookからGenreのテーブルを更新をかけようとした場合、次のエラーページに遷移する。

要約すると、  
デフォでネストされたモデルは更新できねぇんだな。  
`BookSerializer#update()`にそういう実装をするか、ネストされるシリアライザに`read_only=True`の設定をしろ

```
AssertionError at /api/v1/books/1

The `.update()` method does not support writable nested fields by default.
Write an explicit `.update()` method for serializer `sample_app.books.entity.BookSerializer`, or set `read_only=True` on nested serializer fields.

Request Method:  PUT
Request URL:  http://localhost:8000/api/v1/books/1
Django Version:  4.1.2
Exception Type:  AssertionError
Exception Value:  

The `.update()` method does not support writable nested fields by default.
Write an explicit `.update()` method for serializer `sample_app.books.entity.BookSerializer`, or set `read_only=True` on nested serializer fields.

Exception Location:  /home/vscode/.local/lib/python3.11/site-packages/rest_framework/serializers.py, line 813, in raise_errors_on_nested_writes
Raised during:  sample_app.books.controller.GetUpdateDestroy
Python Executable:  /usr/local/bin/python
Python Version:  3.11.6
Python Path:  

['/python/django/src',
 '/home/vscode/.vscode-server/extensions/ms-python.python-2023.18.0/pythonFiles/lib/python/debugpy/_vendored/pydevd',
 '/home/vscode/.local/lib/python3.11/site-packages',
 '/usr/local/lib/python311.zip',
 '/usr/local/lib/python3.11',
 '/usr/local/lib/python3.11/lib-dynload',
 '/usr/local/lib/python3.11/site-packages']

Server time:  Mon, 16 Oct 2023 18:36:40 +0000
```
