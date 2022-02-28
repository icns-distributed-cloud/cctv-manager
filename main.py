from flask import Flask, jsonify
from flask_cors import CORS
from flask_script import Manager, Server

from app.api import build_api
from app.utils.create_all_containers import *
from app.utils.utils import *
from app.resources.api import *
from sqlalchemy import create_engine, text

import os
import json

def load_config(filename):
    config = {}
    with open(filename, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config

config = load_config('./config.json')


class MyFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
            with self.app_context():
                check_cctv()
                create_all_containers()
        super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)





if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    print('INIT')


# app = Flask(__name__)
app = MyFlaskApp(__name__)
cors = CORS(app)
app.config.config = config
app.config['CORS_HEADERS'] = 'Content-Type'

app.config.from_pyfile('config.py')
database = create_engine(app.config['DB_URL'], encoding='utf-8')
app.database = database
app.alert = []
build_api(app)


if __name__ == '__main__':
    
    app.run(host='0.0.0.0')