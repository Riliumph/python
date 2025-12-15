# Clean Architecture Template

このディレクトリはClean Architectureを使う上で使い回せる汎用部分を抜き出したリポジトリだ。  
そのため、業務ロジックであるEntityやそれを使うUsecaseは含まれない。

ここでは、Frameworks&Driversを使うinterface adapter層などが主に含まれる。

これを管理することで、実際にUsecase以下を実装する際に、「これってUsecaseで実装すべきかな？」と悩まなくて済むようにするのが狙い。
