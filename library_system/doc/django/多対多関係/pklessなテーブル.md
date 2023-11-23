# 多対多テーブルをPKレスで作りたい

答え：無理

book_idとgenre_idを紐づけるだけの関係テーブルにおいて、あまりPKは有用ではないと思える。  
また、`serial`型なPKを用意すると桁あふれの心配が出てくるため、「本当に必要ない」ならばPKは入れたくない。

> PKが必要ないケースなんて本当に稀で、やってることがしょうもない時ぐらいだと思うが

```sql
CREATE TABLE books_genres(
    -- id SERIAL PRIMARY KEY, これ要らなくない？
    book_id INT NOT NULL,
    genre_id INT NOT NULL,
    UNIQUE(book_id, genre_id)
);
```

ただ、SQLアンチパターンの第3章「IDリクワイアド」に以下の記述がある。

> id列以外の2列にUNIQUE制約が必要ならば、id列はただの無駄です

やっぱりそうやねやんけ！！！！！！！！！！！！！！！！！！！！！！！！！！

## [Options.managed](https://docs.djangoproject.com/ja/4.1/ref/models/options/#managed)

`django.db.models.Model`の内部には`Meta`クラスを定義できる。  
この`Meta`クラスに、`managed`というメンバが存在する。

この`maanaged`メンバのドキュメントとして以下があるの。

> 宣言しない場合、モデルに自動的なプライマリキーが追加されます。後のコードの読み手に混乱を避けるために、未管理のモデルを使用する際にモデル化するデータベーステーブルのすべての列を指定することが推奨されます。  
> managed=Falseのモデルには、別の未管理モデルを指すManyToManyFieldが含まれている場合、多対多の結合の中間テーブルも作成されません。ただし、管理されたモデルと未管理モデルの間の中間テーブルは作成されます。

うむ、まるで`False`を設定したらプライマリキーが存在しないテーブルを定義できそうな具合の書き方である。

残念ながら、この値はDjangoが適切なDBマイグレーション時にDBを構築するかしないかを決定するだけである。  
`Model`がDBを参照するときに勝手にPrimaryKeyを探しに行く仕様を制御する代物ではない。

結局、Djangoに従うしかないわけだが、DjangoはIDリクワイアドを解決する作りにはなっていないようだ。
