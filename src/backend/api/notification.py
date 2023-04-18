from flask_security import login_required
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

    def get(self):
        unread_notifications = Notification.query.filter_by(read=False,recipient_id=current_user.id).all()
        return {
                'status':200,
                'message':'Request successful',
                'notifications': stringify_notifications(unread_notifications)
        },200
    
    def put(self,notification_id=None):
        if not notification_id:
            return {"message":"Malformed request"},400
        
        notification = Notification.query.filter_by(id=notification_id,recipient_id=current_user.id).first()
        if not notification:
            return {"message":"Notification not found"},404
        
        notification.read = True
        db.session.commit()
        return {"message":"Notification read"},200
    
    def post(self):
        
        args=create_notification_parser.parse_args()
        sender_id=args.get('sender_id',None)
        recipient_id=args.get('recipient_id',None)
        content=args.get('content',None)
        action_url=args.get('action_url',None)

        malformed=[None,'']
        if recipient_id in malformed or content in malformed:
            return {"status":400,"message":"Malformed request!"},400
        
        RecipientExistsCheck=User.query.filter_by(id=recipient_id).first()
        if RecipientExistsCheck is None:
            return {"status":404,"message":"Notification recipient not found!"},404
        
        newNotification=Notification(sender_id=sender_id,
                                     recipient_id=recipient_id,
                                     content=content,
                                     action_url=action_url,
                                     read=False)
        
        db.session.add(newNotification)
        db.session.commit()

        output=[]
        output.append(newNotification)

        return {"status":201,"message":"Notification created succesfully!",
                "notification":stringify_notifications(output)},201





        

