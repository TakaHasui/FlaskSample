from flask import Flask, render_template, url_for, request, session, redirect
import random
import string
import json
import re
import pprint
from datetime import timedelta

import contentful_management
import contentful

import models.BookRegister as Book
import models.Token as Token


msg = ''
app = Flask(__name__)
app.secret_key = 'abcdefghijklmn'
app.permanent_session_lifetime = timedelta(minutes=60)

CONTENT_TYPE_ID = 'bookRegister'
SPACE_ID = "b7g4fw3k8d2t"
ENV_ID = 'master'
managementToken = ''
deliveryToken = ''
previewToken = ''


@app.route('/', methods=['GET'])
def index():
    sessionMsg = ''
    if 'id' in session:
        conditions = {
            'order': '-sys.createdAt',
        }
        entries = Book.getEntries(conditions)

        pprint.pprint('*** TEST **************************')
        booksData = []
        # pattern = "url='([a-zA-Z0-9./_]*)'"
        for item in entries:
            tmp = item.raw['fields']
            pprint.pprint('*** 通過1 ***')
            if 'imageM' in tmp:
                pprint.pprint('*** 通過2 ***')
                imageUrl = Book.getImage(tmp['imageM']['sys']['id'])
                tmp['imageUrl'] = imageUrl

            booksData.append(tmp)

        if 'msg' in session:
            sessionMsg = session['msg']
            del session['msg']
        pprint.pprint(booksData)

        return render_template('index.html', items=booksData, msg=sessionMsg)

    return redirect(url_for('login_'))


@ app.route('/login', methods=['GET', 'POST'])
def login_():
    sessionMsg = ''
    if request.method == 'GET':
        session.clear
        if 'msg' in session:
            sessionMsg = session['msg']
            del session['msg']
        return render_template('login.html', msg=sessionMsg)
    elif request.method == 'POST':
        session.permanent = True
        session['id'] = request.form.get('id')
        session['msg'] = 'ログインしました'
        session['dToken'] = request.form.get('password')

        tokens = Token.getLoginData()
        session['mToken'] = tokens[0].raw['fields']['managementToken']

        return redirect(url_for('index'))


@ app.route('/logout', methods=['GET'])
def logout():
    session.pop('id', None)
    session.clear()
    session['msg'] = 'ログアウトしました'
    return redirect('/login')


@ app.route('/detail/<id>')
def detail(id):
    entry = Book.getEntry(id)

    if entry:
        return render_template('detail.html', item=entry)
    else:
        return 'Item not found', 404


@ app.route('/add', methods=['POST'])
def addBook():
    # 登録済みチェック
    client = contentful.Client(
        SPACE_ID,
        session['dToken']
    )
    conditions = {
        # 'select': 'fields.isbn',
        'fields.isbn': request.form.get('isbn')
    }
    entries = Book.getEntries(conditions)
    pprint.pprint(entries)

    if len(entries):
        session['msg'] = '登録済みの本です'
        session['msgColor'] = 'msgAlert'
        return redirect(url_for('index'))

    client = contentful_management.Client(session['mToken'])
    imgSrc = request.form.get('image') if request.form.get(
        'image') else './static/image/common/noimageFull.png'

    entry_attributes = {
        'content_type_id': CONTENT_TYPE_ID,
        'fields': {
            'isbn': {
                'ja': request.form.get('isbn')
            },
            'title': {
                'ja': request.form.get('title')
            },
            'publisher': {
                'ja': request.form.get('publisher')
            },
            'author': {
                'ja': request.form.get('author')
            },
            'published': {
                'ja': request.form.get('published')
            },
            'description': {
                'ja': request.form.get('description')
            },
            'imageUrl': {
                'ja': imgSrc
            }
        }
    }
    newEntry = client.entries(SPACE_ID, ENV_ID).create(
        randomname(22),
        entry_attributes
    )
    newEntry.publish()
    # newEntry = Book.addEntry(request)

    # レスポンスの確認
    if newEntry.is_published:
        session['msg'] = 'エントリーが追加されました。'
        # print('エントリーID:', response.json()['sys']['id'])
    else:
        session['msg'] = 'エントリーの追加に失敗しました。'
        # print('ステータスコード:', response.status_code)
        # print('エラーメッセージ:', response.text)

    return redirect(url_for('index'))


def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
