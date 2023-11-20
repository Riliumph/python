# Serializerのdataが取れる取れない

## 実装

```python
class BaseSerializer(Field):
    """
    The BaseSerializer class provides a minimal class which may be used
    for writing custom serializer implementations.

    Note that we strongly restrict the ordering of operations/properties
    that may be used on the serializer in order to enforce correct usage.

    In particular, if a `data=` argument is passed then:

    .is_valid() - Available.
    .initial_data - Available.
    .validated_data - Only available after calling `is_valid()`
    .errors - Only available after calling `is_valid()`
    .data - Only available after calling `is_valid()`

    If a `data=` argument is not passed then:

    .is_valid() - Not available.
    .initial_data - Not available.
    .validated_data - Not available.
    .errors - Not available.
    .data - Available.
    """
    def __init__(self, instance=None, data=empty, **kwargs):
        self.instance = instance
        if data is not empty:
            self.initial_data = data
        self.partial = kwargs.pop('partial', False)
        self._context = kwargs.pop('context', {})
        kwargs.pop('many', None)
        super().__init__(**kwargs)
    @property
    def data(self):
        if hasattr(self, 'initial_data') and not hasattr(self, '_validated_data'):
            msg = (
                'When a serializer is passed a `data` keyword argument you '
                'must call `.is_valid()` before attempting to access the '
                'serialized `.data` representation.\n'
                'You should either call `.is_valid()` first, '
                'or access `.initial_data` instead.'
            )
            raise AssertionError(msg)

        if not hasattr(self, '_data'):
            if self.instance is not None and not getattr(self, '_errors', None):
                self._data = self.to_representation(self.instance)
            elif hasattr(self, '_validated_data') and not getattr(self, '_errors', None):
                self._data = self.to_representation(self.validated_data)
            else:
                self._data = self.get_initial()
        return self._data
```

コンストラクタを読めばわかるが、引数`data`は`initial_data`に格納される。  
そして、`data`プロパティをコールした場合、「`initial_data`を持っていて`_validated_data`を持たない」場合には例外を創出してしまって、取り出すことはできない。  
`_validated_data`が生成されるのは、`is_valid`を読んだときである。

## 基本的な使い方

```python
serializer = UserSerializer(target, data=data)
serializer.is_valid(raise_exception=True)
serializer.save()
```

## 解説

docstringにも書いてあるが、`data`に値を与えるか与えないかで参照できるタイミングが異なる。  

### CRUDのCreateの用法

この用法はデータを作成する時に使われる用法である。  
serializerの引数`data`に値を与えることで、serializer内部では`initial_data`に格納させる。  
その後、明示的に`is_valid`を呼ぶことで`_validated_data`を生成する。  
これにより、`data`プロパティをコールしても例外を送出させずに値を取得できる。  

まぁ、この場合、`save`でmodelを取得したいことが多いか。

```python
serializer = UserSerializer(data=data)
serializer.is_valid(raise_exception=True)
serializer.save()
```

### CRUDのReadの用法

この用法はデータを取得するときに使われる用法である。  

serializerの引数`data`には値を与えずに生成する。  
9割、一行目の`Model`を取り出したところで十分な処理ができるだけのデータが揃うので実装するケースは少ない。  

> どうやら、`Model`型を`model_to_dict`を介して`dict`を生成しても、返せないデータがあるらしい。  
> Browsable API Rendererがもっとも正しく動作するには`rest_framework.utils.serializer_helpers.ReturnDict`型を返す必要があるために実装した。

```python
data = User.objects.all().order_by(User._meta.pk.name)
serializer = UserSerializer(data)
serializer.data
```

### CRUDのUpdateの用法

この用法はデータを更新するときに使われる用法である。

serializerの引数`instance`と`data`の両方に値を与えて生成する。  
`instance`側には更新する対象のデータを、`data`側には更新後のデータを与える。

```python
target = User.objects.get(user_id=user_id)
serializer = UserSerializer(target, data=data)
serializer.is_valid(raise_exception=True)
serializer.save()
```

### CRUDのDeleteの用法

残念ながら、Deleteの際にserializerを使う必要はない。

```python
deleted_info = User.objects.filter(or_condition).delete()
```
