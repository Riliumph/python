# Djangoを極力使う場合の設計

- view（Djangoに依存する）
- usecase
  - inputport
  - interactor
- repository（Djangoに依存する）
- entity（Djangoに依存する）

## view層

リクエストを受け付けて、セキュリティ的な判断を行う層。

ここで、

- 飛んできたリクエストは正しいか？
- 要求してきたユーザーアカウントは越権していないか？

たとえば、飛んできたリクエストが正しいかは`rest_framework.serializer`を使えば省略できる。  

DjangoのView機能をふんだんに使おう。  
ここを使わないならDjangoを選んだ理由は、今の僕には分からない

## usecase層

### inputport

ビジネスロジックのIF。

### interactor

inputportの実体。  
これがビジネスロジックを担当するので必ず必要。

Ａのデータを触った後にＢのデータを触るとか、色々行う。

## repository層

データベースなどのストレージにアクセスする層。  
PostgreSQLなのか、MySQLなのかを吸収する層である。

ここは、DjangoのORMである`Django.forms.models`を用いることで省略できる。  

## entity層

実際のデータクラスを表現する層。  
ここもDjangoのORMである`Django.forms.models`がそれを担ってくれる。
