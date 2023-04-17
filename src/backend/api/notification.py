from flask_security import login_required
from flask_login import current_user
from flask_restful import Resource
from backend.models import *
from backend.utils import stringify_notifications

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
        

