from testapp import app
from flask import render_template 

# ルートにアクセスした時に表示するページの処理
@app.route('/')
def index():
    # 複数のデータをまとめてTemplatesに送りたい場合はdictで！
    my_dict = {
        'insert_something1':'views.pyのinsert_something1部分です。',
        'insert_something2':'views.pyのinsert_something2部分です。',
        'test_titles':['title1', 'title2', 'title3']
    }
    return render_template('testapp/index.html', my_dict=my_dict)

# 他のページも作ってみる
@app.route('/test')
def other1():
    return 'this is test page!'
