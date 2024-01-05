from flask import session
import contentful

CONTENT_TYPE_ID = 'tokens'
SPACE_ID = "b7g4fw3k8d2t"
ENV_ID = 'master'
managementToken = ''
deliveryToken = ''
previewToken = ''


def getLoginData():
    client = contentful.Client(
        SPACE_ID,
        session['dToken']
    )
    tokens = client.entries({
        'content_type': CONTENT_TYPE_ID,
        'fields.deliveryToken': session['dToken']
    })

    return tokens
