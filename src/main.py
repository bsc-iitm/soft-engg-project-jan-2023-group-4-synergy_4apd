from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from backend.config import Config
from backend.database import *
from backend.models import *
from backend.api import *


app = Flask(__name__, template_folder='templates')
app.app_context().push()

app.config.from_object(Config)

db.init_app(app)

api = Api(app)
cors = CORS(app)

api.add_resource(TagAPI,'/api/v1/tags/')

api.add_resource(TicketsAPI,'/api/v1/tickets/','/api/v1/tickets/<int:ticket_id>/')
api.add_resource(MyTicketsAPI,'/api/v1/mytickets/')

api.add_resource(MessageAPI,'/api/v1/messages/','/api/v1/messages/<int:message_id>/')

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8000)

