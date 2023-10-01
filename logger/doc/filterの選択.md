# Filterの選択

ログをフィルターしたいときに使われるオブジェクト。  

Filterは次のような時に使われる。

- ログレベルが一定以下ならドロップする
- メッセージ内に`password`があるから伏字にする。
- etc...

ログレベルのフィルターぐらいは、フィルター機能を使わなくてもでやれるようになっている。

## クラスで実装する

```python
import logging
import sys

class TextFilter:
    def __init__(self, text=""):
        self.text = text

    def filter(self, record):
        '''処理したい、したくないをTrue/Falseで表現する関数
        record: logging.LogRecordを受ける引数
        '''
        if self.text in record.getMessage():
            return True
        return False

logger = logging.getLogger(__name__)
h = logging.StreamHandler(sys.stdout)
h.setLevel(logging.INFO)
h.addFilter(TextFilter("password"))
logger.addHandler(h)

logger.info("password: hoge") # 出力されない。
logger.info("login success")
```

Filterクラスは、Formatterのように基本クラスを継承する必要はない。  
`filter()`メソッドが定義されていれば、ダックタイピングで実行されるようになっている。

## 簡単に実装する

フィルタオブジェクトが`filter(self, record)`メソッドを持たない場合、そのオブジェクトはcallableであると見なす仕組みがある。  
この機能により、ラムダ関数でも実装できる。

```python
import logging
import sys

logger = logging.getLogger(__name__)
h = logging.StreamHandler(sys.stdout)
h.setLevel(logging.INFO)
h.addFilter(lambda record: "password" in record.getMessage())
logger.addHandler(h)

logger.info("password: hoge")
logger.info("login success")
```
