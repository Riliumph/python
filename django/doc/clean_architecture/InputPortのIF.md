# InputPortのIF

InputPortはビジネスロジックのIFである。  
ここを考えるためには「何がしたいのか」を考えなければならない。

巷では、１つのクラスにメソッドですべてのことをさせるとか、やりたいこと一つに１つのInputPortを用意するとか、色んな方法が散見されるので、ここで整理しておきたい。

## 今まで見た中で良さそうな設計

ユースケースの種類に対して、１つのInputPortを定義する方法。  
例えば、以下のようなユースケース毎にInputPortとInteractorを構築する。

- UserCreate: ユーザー作成系のInputPort
  - CreateUser: 単一ユーザーを作成するユースケース
  - CreateUsers: 複数ユーザーを作成するユースケース
- UserRead: ユーザー取得系のInputPort
  - ReadUserById: user_idでユーザーを取得するユースケース
  - ReadUserByName: user_nameでユーザーを取得するユースケース
  - ReadUserByEmail: e-mailでユーザーを取得するユースケース

BaseInputPortなど、１ユースケース＝１クラスにする方法もある。  
しかし、ユーザーの作成を単一でやるかバルクでやるかの違いはあれど、その中には共通する処理がある場合がある。そうなるとそれはUserCreateInteractorでメソッド定義されて、両方のユースケースで共有されるべき処理である。  
ユーザーの取得を見ても、取得方法の違いはあれど、その中で共通する処理が出てくるかもしれない。その時には、UserReadInteractorで共通するメソッドとして定義されて、両方のユースケース（メソッド）で共有されるべきである。

```python
import abc
from typing import List, Dict, Any

class UserCreateInputPort(abc.ABC):
    '''Userの作成処理について責任を持つInputPort
    '''
    @abc.abstractmethod
    def __init__(self, repo: UserRepository) -> None:
        raise NotImplementedError()
    # Createの処理
    @abc.abstractmethod
    def CreateUser(self, data: Dict[str, Any]) -> Dict[str,Any]:
        '''単一のユーザーを作成するメソッド
        '''
        raise NotImplementedError()
    @abc.abstractmethod
    def CreateUsers(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        '''複数のユーザーを作成するメソッド
        bulk_createなどを用いて、１回の通信で複数のユーザーを作成する
        '''
        raise NotImplementedError()

class UserReadInputPort(abc.ABC):
    '''Userの取得処理について責任を持つInputPort
    '''
    @abc.abstractmethod
    def __init__(self, repo: UserRepository) -> None:
        raise NotImplementedError()
    # Readの処理
    @abc.abstractmethod
    def ReadUserById(self, data: Dict[str, Any]) -> Dict[str,Any]:
        '''UserIDによるユーザーを取得するメソッド
        '''
        raise NotImplementedError()
    @abc.abstractmethod
    def ReadUsersByName(self, data: Dict[str, Any]) -> Dict[str,Any]:
        '''ユーザー名でユーザを取得するメソッド
        '''
        raise NotImplementedError()
    @abc.abstractmethod
    def ReadUsersByEmail(self, data: Dict[str, Any]) -> Dict[str,Any]:
        '''メールアドレスでユーザを取得するメソッド
        '''
        raise NotImplementedError()
```

## ダメそうな設計

Userに関するすべてのユースケースをメソッドとして持つようなクラス設計。  
特にこれも嫌いじゃないが、あらゆるメソッドの共有メソッドをprivateに持つことになりそう。

総じて、巨大なInteractorができそうである。

```python
import abc
from typing import List, Dict, Any

class UserInputPort(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: UserRepository) -> None:
        raise NotImplementedError()
    @abc.abstractmethod
    def CreateUser(self, data: Dict[str, Any]) -> Dict[str,Any]:
        raise NotImplementedError()
    @abc.abstractmethod
    def CreateUsers(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError()
    @abc.abstractmethod
    def UpdateUser(self, data: Dict[str, Any]) -> Dict[str,Any]:
        raise NotImplementedError()
    @abc.abstractmethod
    def UpdateUsers(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError()
    @abc.abstractmethod
    def DeleteUser(self, data: Dict[str, Any]) -> Dict[str,Any]:
        raise NotImplementedError()
    @abc.abstractmethod
    def DeleteUsers(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError()
```

## よく見るけどダメそうな設計

超汎用なクラス設計で、コンストラクタと実行演算子しか持たない。  
そして、すべてのInteractorがこのIFを継承する。

つまり、FindByXX毎にGetInteractorができる。  
それも無限に。

……それ、便利かな？？  
いや、確かにIFをこれでもかというぐらい使ってるけどさ。。。

```python
import abc
from typing import List, Dict, Any

class BaseInputPort(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: BaseRepository) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()
```
