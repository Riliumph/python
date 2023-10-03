# Django Model

最もシンプルなモデルクラス。  

```python
class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
```

## テーブル名

### テーブル名は自動命名される

ルール：app名_モデルクラス名

djangoのmigration機能を使う場合、テーブル名は上記のルールで自動決定される。  
このappがsample_appであれば、テーブルには`samlple_app_usermodel`が名付けられる。

### テーブル名を自由に命名する

そうはいっても、既に動いていたサービスをDjangoに置き換えるなど、migrationに頼らない構成をする場合もある。  
その場合に備えて、Djangoはテーブル名をプログラマ側で設定できるIFを用意している。

`Meta`クラスの`db_table`変数に任意の値を入れることで、対象のテーブルとクラス定義をマッピングしてくれる。

## カラム名

### カラム名はメンバ変数名で命名される

このクラスはORMと呼ばれるクラスであるため、まるで１レコードであるかのように扱われる。  
どういうプログラムをしてるのかは謎だが、変数名と同じ名前のカラムを探して値を一致させてくれる。

今回のクラスであれば、`user_id`とカラム名の`user_id`が一致した定義でなければエラーとなる。

### カラム名を自由に命名する

```python
class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True, db_column="foo")
```

modelパッケージのフィールドクラスには、必ずカラム名を指定できる`db_column`引数が存在する。

## 制約もMeta情報なのでMetaクラスで

```python
class UserModel(models.Model):
    （略）
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["foo_id", "foo_key"],
                name="foo_id_foo_key"
            )
        ]
```

もし外部キーなどがあった場合、Metaクラス側で記載する。  

### 外部キーも自動命名される

ルール：対象のモデルクラス名_id

> なんか、このモデルクラス名はスネークケースになるらしい

`name`変数に名前を記載しない場合、自動的に決定される。
