# Minstrel_JP
Minstrelの実装

### run.py
これを実行することで作動します。

### showcases/generate.py
これが一番始めのページの設計です。
モジュール設定・生成するフェーズです。
入力を受け付けて、modules/get_modules.pyにモジュール設定を託します。
モジュール設定がされたらmodules/○○.pyにモジュール内容作成を託します。
終わりにモジュールを合成してプロンプトにします。

### showcases/test.py
これが次のページの設計です。
合成したプロンプトをAIモデルにテストするフェーズです。



### modules/get_modules.py
入力文から、必要なモジュールを設定します。

### modules/○○.py（get_modules.py以外）
モジュールの内容を作成します。



### models/openai.py & models/transformer.py
AIモデルからの応答を生成するクラスを持っています。
