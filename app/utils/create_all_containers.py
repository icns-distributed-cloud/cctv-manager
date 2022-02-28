from flask import current_app as app

from app.utils.utils import *

from sqlalchemy import text


def create_all_containers():
    try:
        results = app.database.execute(text('''
            SELECT * FROM cctv
        ''')).fetchall()
    except Exception as exc:
        return exc

    for result in results:
        streamurl = f"rtsp://{result['user_id']}:{result['password']}@{result['streamurl'][7:]}"
        res = create_container(streamurl, result['abnormal_websocket_url'], result['cctv_id'])
        res = start_container(result['cctv_id'])






