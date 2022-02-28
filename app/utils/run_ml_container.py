from sqlalchemy import text

from flask import current_app as app


def run_container():
    try:
        result = app.database.execute(text(''' 
            INSERT INTO articles (title, content, views)
            VALUES (:id, :password, :name)
        '''), {
            'title': 'sd',
            'content': 'fdfd',
            'views': 0

        }).fetchall()
        return result
    except Exception as exc:
        return 'fail'




