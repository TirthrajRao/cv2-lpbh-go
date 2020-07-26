from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

# SCOPES = {
# 	'https://www.googleapis.com/auth/spreedsheets',
# 	'https://www.googleapis.com/auth/presentations',
# 	'https://www.googleapis.com/auth/drive'
# }

TMPLFILE = 'title slide template'  # use your own!
SCOPES = (
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/presentations',
)


HTTP = creds.authorize(Http())
DRIVE =  discovery.build('drive',  'v3', http=HTTP)
SLIDES = discovery.build('slides', 'v1', http=HTTP)


rsp = DRIVE.files().list(q="name='%s'" % TMPLFILE).execute().get('files')[0]
DATA = {'name': 'Google Slides API template DEMO'}
print('** Copying template %r as %r' % (rsp['name'], DATA['name']))
DECK_ID = DRIVE.files().copy(body=DATA, fileId=rsp['id']).execute().get('id')

print('** Replacing placeholder text and icon')
reqs = [
    {'replaceAllText': {
        'containsText': {'text': '{{NAME}}'},
        'replaceText': 'Hello World!'
    }},
    {'createImage': {
        'url': img_url,
        'elementProperties': {
            'pageObjectId': slide['objectId'],
            'size': obj['size'],
            'transform': obj['transform'],
        }
    }},
    {'deleteObject': {'objectId': obj['objectId']}},
]
SLIDES.presentations().batchUpdate(body={'requests': reqs},
        presentationId=DECK_ID).execute()
print('DONE')
# CLIENT_SECRET_FILE = r'/var/www/html/face-detection/ai-recognition/cv2/storage.json'
# store = file.Storage('storage.json')
# creds = store.get()

# if not creds or creds.invalid:
# 	flow = client.flow_from_clientsecrets('client-secrets.json', SCOPES)
# 	creds = tools.run_flow(flow, store)
