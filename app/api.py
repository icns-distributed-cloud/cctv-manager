from flask_restful import Api

from app.resources.api import GETTest
from app.resources.api import POSTRegister
from app.resources.api import POSTDelete
from app.resources.api import POSTAlert
from app.resources.api import GETAlert

def build_api(app):
    api = Api()

    api.add_resource(GETTest, '/api/test')

    api.add_resource(POSTRegister, '/api/register')
    api.add_resource(POSTDelete, '/api/delete')
    api.add_resource(POSTAlert, '/api/alert/<path:content>')
    api.add_resource(GETAlert, '/api/alert')

    api.init_app(app)

    return api