from flask import Flask, request
import logging
import json
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

translator_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
translator_api_key = 'trnsl.1.1.20190414T112602Z.28565479fb179187.ee436856ac2d0c7e02e4a62e755a4fffa15baa95'


@app.route('/post', methods=['POST'])
def main4():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    if req['session']['new']:
        res['response']['text'] = 'Привет! Я могу переводить слова!'
    else:
        word = req['request']['nlu']['tokens'][-1]
        res['response']['text'] = translate(word)


def translate(word):
    params = {
        'key': translator_api_key,
        'text': word,
        'lang': 'ru-en'
    }
    data = requests.get(translator_url, params).json()
    return data['text'][0]


if __name__ == '__main__':
    app.run()
