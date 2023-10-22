# serializerのコンストラクタ

一番小さなシリアライザである`GenreSerializer`を例題にする。

## 誤った実装

基本的にseiralizerのコンストラクタはオーバーライドする必要はない。  
特殊な実験例として、`read_only`をインスタンス変数にする必要があった。  
そこで以下のような実装を行った。

```python
class GenreSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=..., **kwargs):
        # BookSerializerから参照できるようにインスタンス変数に登録する
        if "read_only" in kwargs.keys():
            self.read_only = kwargs.get("read_only")
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = GenreEntity
        fields = '__all__'
```

この実装は、継承元の`serializers.ModelSerializer`からコードスニペット補完で自動で作成している。  
引数が具体的過ぎて、そぐわないケースがあれば動かなくなってしまう模様。

### serializes

```python
    def __init__(self, instance=None, data=empty, **kwargs):
        self.instance = instance
        if data is not empty:
            self.initial_data = data
        self.partial = kwargs.pop('partial', False)
        self._context = kwargs.pop('context', {})
        kwargs.pop('many', None)
        super().__init__(**kwargs)
```

## 正しい実装

```python
class GenreSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # BookSerializerから参照できるようにインスタンス変数に登録する
        if "read_only" in kwargs.keys():
            self.read_only = kwargs.get("read_only")
        super().__init__(*args, **kwargs)

    class Meta:
        model = GenreEntity
        fields = '__all__'
```
