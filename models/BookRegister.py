from flask import request, session
import random
import string
import json
import pprint
from dictknife import deepmerge

import contentful_management
import contentful

CONTENT_TYPE_ID = 'bookRegister'
SPACE_ID = "b7g4fw3k8d2t"
ENV_ID = 'master'
managementToken = ''
deliveryToken = ''
previewToken = ''


def getEntries(myConditions={}):
    print('getEntries')
    client = contentful.Client(
        SPACE_ID,
        session['dToken']
    )

    conditions = {
        'content_type': CONTENT_TYPE_ID,
        # 'select': 'sys.id,fields.title',  # フィールドの指定
        'limit': 100,
        'skip': 0,
        'order': 'sys.createdAt',  # 'fields.price' priceフィールドの降順ソート
        # 'fields.title[in]': 'example' #titleフィールドに'example'文字列が含む
    }

    if len(myConditions):
        conditions = deepmerge(conditions, myConditions)

    entries = client.entries(conditions)

    return entries


def getEntry(entryId):
    print('getEntry')
    client = contentful.Client(
        SPACE_ID,
        session['dToken']
    )
    entry = client.entry(entryId)
    return entry


def addEntry():
    print('addEntry')
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
            'thumbnail': {
                'ja': request.form.get('image')
            }
        }
    }
    newEntry = client.entries(SPACE_ID, ENV_ID).create(
        randomname(22),
        entry_attributes
    )
    newEntry.publish()
    return newEntry

def getImage(assetId):
    client = contentful.Client(
        SPACE_ID,
        session['dToken']
    )
    asset = client.asset(assetId)
    return asset.url()


def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))
