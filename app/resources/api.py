
from venv import create
from flask_restful import Resource
from flask_cors import cross_origin
from flask import current_app as app

from app.models.response import error_response, ok_response
from app.utils.create_all_containers import *
from app.utils.utils import *
from sqlalchemy import text
import requests

# GET /test
class GETTest(Resource):
    @cross_origin()
    def get(self):
        
        try:
            results = app.database.execute(text('''
                SELECT * FROM cctv
            ''')).fetchall()

        except Exception as exc:
            return error_response(500, str(exc))
        
        for result in results:
            streamurl = f"rtsp://{result['user_id']}:{result['password']}@{result['streamurl'][7:]}"
            create_container(app, streamurl, result['abnormal_websocket_url'], result['cctv_id'])


            print(result['cctv_id'])


        return ok_response(None)

class POSTRegister(Resource):
    @cross_origin()
    def post(self):

        check_cctv()
        create_all_containers()

        return ok_response(None)

class POSTDelete(Resource):
    @cross_origin()
    def post(self):
        check_cctv()

        return ok_response(None)


class POSTAlert(Resource):
    @cross_origin()
    def post(self, content):
        app.alert.append(content)

        return ok_response(None)

class GETAlert(Resource):
    @cross_origin()
    def get(self):

        return ok_response(app.alert)