from flask_restful import Api
from flask_cors import CORS

from backend import app
from backend.database import db
from backend.controllers import *
from backend.api import *

from humanize import naturaltime


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

api.add_resource(RoleAPI, '/api/v1/admin/users/<string:user_id>/')

@app.context_processor
def utility_functions():
    return dict(naturaltime=naturaltime)

if __name__ == '__main__':

    db.create_all()
    app.run(host='0.0.0.0', port=8000)
