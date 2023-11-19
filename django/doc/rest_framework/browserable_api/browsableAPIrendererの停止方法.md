# browsableAPIRendererの停止方法

Djangoのバックエンド開発において、便利なのはRESTul Frameworkである。  
このフレームワークはデフォルトでWEB UIをレンダリングする機能を持っており、フロントエンドの問題と切り離してAPIをデバッグすることができる。

> エンジニアは、フロントエンドのグラフィカルな部分を作れないもんなとか言うな！！

しかし、これをPRD環境にまでリリースしてしまうと、自由にPOSTメソッドが叩ける環境を公開してしまうことになる。  
あくまで、この機能を使うのは開発環境までにしたい。

だが、[ドキュメント](https://www.django-rest-framework.org/)を読む訳だが、なんと調べたらいいのか分からない。  
答えは、`BrowsableAPIRenderer`と言うらしく、[このページ](https://www.django-rest-framework.org/api-guide/settings/#default_renderer_classes)に記載があるが、検索できると思っているのだろうか。

ドキュメントには、デフォルトでは次が設定されると書いてあるが、項目なしでも勝手にデフォルト解釈されるとドキュメントも漁れないのでコメントアウトにしておくとかしてほしいものだ。

```python
[
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
]
```

settings.pyから当のRendererを停止させる。

```python

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    )
}
```

- DEFAULT_RENDERER_CLASSES：Responseオブジェクトを返すときに使用されるRendererの模様

> 参考：
>
> - [Django REST framework - Settings](https://www.django-rest-framework.org/api-guide/settings/#api-policy-settings)
> - [Django Rest FrameworkでAPIのURLにアクセスされた時の表示について](https://qiita.com/xKxAxKx/items/4e45eee70a260826b171)
> - [Python django-rest-framework How to disable admin-style browsable interface](https://www.youtube.com/watch?v=WKz5OXdfyMk)
