from flask import Flask

# オブジェクトの生成
app = Flask(__name__)
# アプリを開始する前に、コンフィグ(設定)を読み込んで貰う.
app.config.from_object('testapp.config')

import testapp.views