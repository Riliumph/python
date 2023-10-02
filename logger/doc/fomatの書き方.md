# formatの書き方

次のようなdictConfigを書くわけだが、いくつかの書き方が存在する。  
特に、`format`と`style`の部分に注目したい。

```python
log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "custom_template": {
            "class": "logging.Formatter",
            "format": ?????,
            "style": ?????,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "custom_template",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
```

以降のサンプルコードでは、`formatters`の部分だけ表記する。

## printスタイル

Pythonの最初期の頃の書式を使うことができる。

```python
log_config = {
    "formatters": {
        "percent_style_formatter": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "style": "%",
        },
    },
}
```

## string.Template

Python2.4で導入された`string.Template`の書式を使うことができる。

```python
log_config = {
    "formatters": {
        "dollar_style_formatter": {
            "format": "${levelname} ${message}",
            "style": "$"
        },
    },
}
```

## str.format

Python2.6で導入された`str.format`の書式を使うことができる。

```python
log_config = {
    "formatters": {
        "curly_style_formatter": {
            "format": "{asctime} - {levelname} - {message}",
            "style": "{",
        },
    },
}
```

## 参考

- [Logging クックブック](https://docs.python.org/ja/3/howto/logging-cookbook.html#logging-cookbook)
