from flask_restful import Api
from flask_cors import CORS

from backend import app, user_datastore
from backend.database import db
from backend.controllers import *
from backend.api import *

from backend.utils import humanize_time

import flask_login


api = Api(app)
cors = CORS(app)

api.add_resource(TicketAPI, '/api/v1/tickets/', '/api/v1/tickets/<string:ticket_id>/')
api.add_resource(MessageAPI, '/api/v1/messages/', '/api/v1/messages/<string:message_id>/')
api.add_resource(ArticleAPI, '/api/v1/articles/', '/api/v1/articles/<string:article_id>/')
api.add_resource(CommentAPI, '/api/v1/comments/', '/api/v1/comments/<string:comment_id>/')
api.add_resource(NotificationAPI, '/api/v1/notifications/', '/api/v1/notifications/<string:notification_id>/')
api.add_resource(MyTicketsAPI, '/api/v1/mytickets/')
api.add_resource(TagAPI, '/api/v1/tags/','/api/v1/tags/<string:tag_id>')
api.add_resource(AnalyticsAPI, '/api/v1/analytics/')
api.add_resource(UserAPI, '/api/v1/users/')
api.add_resource(RoleAPI, '/api/v1/admin/users/<string:user_id>/')

@app.context_processor
def utility_functions():
    return dict(humanize_time=humanize_time)

def assign_default_role(app, user):
    if len(user.roles) == 0:
        default_role = user_datastore.find_role('user')
        user_datastore.add_role_to_user(user, default_role)

flask_login.user_logged_in.connect(assign_default_role)

if __name__ == '__main__':

    db.create_all()

    roles = Role.query.all()
    if len(roles) == 0:
        user_student = Role(name='user', description='Default users, mainly students')
        support_staff = Role(name='support_staff', description='Support Staff')
        admin = Role(name='admin', description='Administrator')
        superadmin = Role(name='superadmin', description='Super Administrator')

        db.session.add(user_student)
        db.session.add(support_staff)
        db.session.add(admin)
        db.session.add(superadmin)
        db.session.commit()

    app.run(host='0.0.0.0', port=8000)
