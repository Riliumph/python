# Djangoの依存度を下げる

- view（Djangoに依存する）
- usecase
  - inputport
  - interactor
- repository
- entity（Djangoに依存する）

## view層

Django依存の方法と変わらない。  
何度も言うが、ここをDjangoに頼らないならDjangoを選んだ理由が分からない。

## usecase層

### inputport

ビジネスロジックのIF。  

### interactor

inputportの実体。  
ここを作らなくて誰が作るんだ。

## repository層

自前でrepositoryクラスを実装することで、この部分をDjangoから解き放つ。  
ただし、解き放つといってもコストの問題がある。

正直、Djangoを使う理由の大きな部分は以下な気がする。

- HTTPのサーバー機能（view層）があること
- DBを制御する機能（ORM）があること

しかし、自前でrepositoryクラスを作って、`django.forms.models`を内部で使うという設計にするということは、repositoryの責任である「データへのアクセス方法」がentity層に移ってしまうということである。

確かに、Djangoから別のフレームワークに移行するとなった場合でも、このrepositoryクラスに直接DBアクセスの処理を書けばいい。  
それこそ、AWSのDynamoやmongoに移ったとしても、ここにAWSのSDKを埋め込めば済む。  

そういう意味では、repositoryとentityが非常に密接に繋がっているDjangoの都合を引き離す意味はある。

しかし、逆に言えば、それぐらいの意味しかない。  
どうせ、Djangoから離れるとなったらほとんど作り直しだろうに。
