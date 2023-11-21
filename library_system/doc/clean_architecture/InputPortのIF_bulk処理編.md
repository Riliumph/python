# InputPortのIF

InputPortはInteractorのIFである。  
Interactorがビジネスロジックの実装が行われている。

このInteractorのためのIFをどうするべきだろうか？

## UseCaseを包括するIF

たとえば、すべてのUseCaseで使えるIFを考えよう。  

```python
class BaseInputPort(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: BaseRepository) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()
```

もう、すべての情報を辞書形式にして送ってもらうという方法である。  
確かに、これだと名前被りさえ気を付ければ特に問題ない。

本当に？

## バルク処理したい場合

一括にUserを登録したいなどのビジネスロジックがあったら対応できなくない？  

### controller側でforする？

Controller側で登録のInteractorを無限に叩くでもいいけど。。。

SQLでの処理は、こんな感じで無数のSQLが実行されるんだよね。  

```sql
insert into users (user_name) values ('user1');
insert into users (user_name) values ('user2');
insert into users (user_name) values ('user3');
```

N回のTCP通信が行われるのでトラフィック量もN倍だよね。  
もちろん、そもそもの通信料が低いからN倍されてもしょっぱいけどさ。。。

### バルク処理の価値はある？

こんな風に一回のinsertでいけるなら、トラフィック了も減るから高速化しそうじゃない？

```sql
insert into users (user_name) values
('user1'),
('user2'),
('user3');
```

つまり、「バルク処理」というものに価値自体はあるわけだ。

## どうする？

### 一つのInputPortクラスでやる

IFの意味があるか微妙だが、一つのクラスIFにするというのはある。  
User系のビジネスロジック用にクラスを定義する。  
そのクラスが各メソッドとしてそれぞれのビジネスロジックを実行できる。

```python
class UserInputPort(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: BaseRepository) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_user(self, request: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_users(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def update_user(self, request: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()

    @abc.abstractmethod
    def update_users(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError()
```

やりたいことを全部メソッドにしてしまって、一つのInputPortと一つのInteractorの関係にしよう！！  
クリーンアーキテクチャの保守性の高さに関しても、

- UserInputPort
  - UserInteractor
  - UserInteractorMock

と、することができるので、テスト容易性は高い。

### UseCase毎にInputPortを作る

```python
class UserCreateInputPort(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: BaseRepository) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_user(self, request: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_users(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError()

class UserUpdateInputPort(abc.ABC):
    @abc.abstractmethod
    def update_user(self, request: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()

    @abc.abstractmethod
    def update_users(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError()
```

こういうクラス設計だと、IFには無い専用メソッドが定義できるので、「`create_user`でも`create_users`でも共通して行いたい」処理が定義しやすい。

ああ、つまり、BaseInputPortを継承する`UserCreateInteractor`が単一用とバルク用の二つのメソッドを持てばよくね？

1用のメソッドとN用のメソッド、1はNに含まれてるんだから、そもそもリストで処理しろという意見も分からなくはない。。。  
いや、でも、「単一で飛んできたリクエストをリスト化する」処理は誰にやらせるの？  
controllerは明らかに越権行為じゃね？  
それだったらメソッドが分かれている方がいいのでは。。。
