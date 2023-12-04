# モデルの注意点

## 同名は禁止

次のような管理だとする。

```bash
entity/
├ a.py
└ b.py
```

`a.py`は以下の内容とする

```python
class Model(models.Model):
    id = models.AutoField(primary_key=True)
    hoge = models.TextField(null=False)
    class Meta:
        db_table = "a"
```

`b.py`も以下の内容である

```python
class Model(models.Model):
    id = models.AutoField(primary_key=True)
    fuga = models.TextField(null=False)
    class Meta:
        db_table = "b"
```

この場合、以下のエラーが発生する。

```python
Exception has occurred: RuntimeError
Conflicting 'model' models in application 'sample': <class 'sample.entity.a.Model'> and <class 'sample.entity.b.Model'>.
```

パッケージが分かれていても同じクラス名はダメらしい
