from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore

from backend.config import Config
from backend.database import *

from backend.models import User, Role
from backend.forms import CustomRegisterForm
from backend.api import *


app = Flask(__name__, template_folder='templates')
app.app_context().push()

app.config.from_object(Config)

db.init_app(app)

api = Api(app)
cors = CORS(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, confirm_register_form=CustomRegisterForm, register_form=CustomRegisterForm)

api.add_resource(TicketAPI, '/api/v1/tickets/', '/api/v1/tickets/<string:ticket_id>/')
api.add_resource(MessageAPI, '/api/v1/messages/', '/api/v1/messages/<string:message_id>/')
api.add_resource(ArticleAPI, '/api/v1/articles/', '/api/v1/articles/<string:article_id>/')
api.add_resource(CommentAPI, '/api/v1/comments/', '/api/v1/comments/<string:comment_id>/')
api.add_resource(NotificationAPI, '/api/v1/notifications/', '/api/v1/notifications/<string:notification_id>/')
api.add_resource(MyTicketsAPI, '/api/v1/mytickets/')
api.add_resource(TagAPI, '/api/v1/tags/','/api/v1/tags/<string:tag_id>')
api.add_resource(AnalyticsAPI, '/api/v1/analytics/')
api.add_resource(UserAPI, '/api/v1/users/')

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8000)
