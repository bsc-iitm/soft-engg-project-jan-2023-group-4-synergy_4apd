from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from backend.config import Config
from backend.database import *
from backend.models import *


app = Flask(__name__, template_folder='templates')
app.app_context().push()

app.config.from_object(Config)

db.init_app(app)

api = Api(app)
cors = CORS(app)


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8000)
