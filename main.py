from flask import Flask, render_template, url_for, request, session, redirect
import random
import string
import json
import pprint
import requests
from datetime import timedelta

import contentful_management
import contentful

# Flask
# https://shigeblog221.com/flask-nyumon/

# ログ
# https://qiita.com/KWS_0901/items/7163e52b4041b909f5bc

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

# deliveryAPI
# https://www.contentful.com/developers/docs/references/content-delivery-api/


@app.route('/', methods=['GET'])
def index():
    sessionMsg = ''
    if 'id' in session:
        client = contentful.Client(
            SPACE_ID,
            session['dToken']
        )

        entries = client.entries(
            {'content_type': CONTENT_TYPE_ID})

        if 'msg' in session:
            sessionMsg = session['msg']
            del session['msg']

        return render_template('index.html', items=entries, msg=sessionMsg)

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
        client = contentful.Client(
            SPACE_ID,
            session['dToken']
        )
        tokens = client.entries({
            'content_type': 'tokens',
            'fields.deliveryToken': session['dToken']
        })
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
    client = contentful.Client(
        SPACE_ID,
        session['dToken']
    )
    entry = client.entry(id)

    if entry:
        return render_template('detail.html', item=entry)
    else:
        return 'Item not found', 404


@ app.route('/add', methods=['POST'])
def addBook():
    print('****** ADD ******')
    # Contentful Management API
    # https://github.com/contentful/contentful-management.py?tab=readme-ov-file#client
    client = contentful_management.Client(session['mToken'])

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
            # 'image': {
            #     'ja': request.form.get('image')
            # }
        }
    }
    newEntry = client.entries(SPACE_ID, ENV_ID).create(
        randomname(22),
        entry_attributes
    )
    newEntry.publish()

    pprint.pprint(newEntry)

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
