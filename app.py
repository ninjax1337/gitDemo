from flask import Flask, request, jsonify
import hashlib
from random import randint
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials


import os
key = '9f0e675419104696beef510b9b81f1d6'
endpoint = 'https://cv-pfe7472.cognitiveservices.azure.com/'
m_endpoint = 'http://54.91.73.112/static/'

credentials = CognitiveServicesCredentials(key)
client = ComputerVisionClient(
    endpoint=endpoint,
    credentials=credentials
)

def get_fn():
    q = ''
    for i in range(64):
        q += chr(randint(0, 9) + ord('0'))
    return (hashlib.sha256(q.encode()).hexdigest()+'.jpg')

def describe_image(filename):
    try:
        url = m_endpoint + filename; print('1++')
        analysis = client.describe_image(url, 1, 'en'); print('2++')
        caption = analysis.captions[0]
        return {
            'success': True,
            'text': caption.text,
            'confidence': caption.confidence
        }
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    if 'q' not in request.files:
        return jsonify({'success': False, 'message':'No file part'})
    q = request.files['q']
    if q.filename == '':
        return jsonify({'success': False, 'message':'No file selected'})
    fn = get_fn()
    q.save(os.path.join('./static', fn))
    res = describe_image(fn)
    return jsonify(res)



app.run(host='0.0.0.0', port=80)
