from flask_security import login_required,roles_required
from flask_login import current_user
from flask_restful import Resource,reqparse
from backend.models import *
from backend.utils import stringify_notifications

create_notification_parser=reqparse.RequestParser()
create_notification_parser.add_argument('sender_id',nullable=True)
create_notification_parser.add_argument('recipient_id',required=True,nullable=False)
create_notification_parser.add_argument('content',nullable=True)
create_notification_parser.add_argument('action_url',nullable=True)

class NotificationAPI(Resource):

    @login_required
    @roles_required('user')
    def get(self):
        unread_notifications = Notification.query.filter_by(read=False,recipient_id=current_user.id).all()
        return {
                'status':200,
                'message':'Request successful',
                'notifications': stringify_notifications(unread_notifications)
        },200
    
    @login_required
    @roles_required('user')
    def put(self,notification_id=None):
        if not notification_id:
            return {
                    "message":"Malformed request"
            },400
        
        notification = Notification.query.filter_by(id=notification_id,recipient_id=current_user.id).first()
        if not notification:
            return {
                    "message":"Notification not found"
            },404
        
        notification.read = True
        db.session.commit()
        return {
                "message":"Notification read"
        },200
    
    @login_required
    @roles_required('user')
    def post(self):
        args=create_notification_parser.parse_args()
        sender_id=args.get('sender_id',None)
        recipient_id=args.get('recipient_id',None)
        content=args.get('content',None)
        action_url=args.get('action_url',None)

        malformed=[None,'']
        if recipient_id in malformed or content in malformed:
            return {
                    "message":"Malformed request!"
            },400
        
        recipient = User.query.filter_by(id=recipient_id).first()
        if not recipient:
            return {
                    "message":"Notification recipient not found!"
            },404
        
        new_notification=Notification(
                                        sender_id=sender_id,
                                        recipient_id=recipient_id,
                                        content=content,
                                        action_url=action_url,
                                        read=False
        )
        
        db.session.add(new_notification)
        db.session.commit()

        return {
                "message":"Notification created succesfully!",
                "id":new_notification.id,
                "sender_id":new_notification.sender_id,
                "recipient_id":new_notification.recipient_id,
                "content":new_notification.content,
                "action_url":new_notification.action_url,
                "timestamp":str(new_notification.timestamp),
                "read":new_notification.read
        },201