from flask import Flask
from flask_login import LoginManager
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = base_dir + '/upload/'
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = LoginManager()
login_manager.init_app(app)


from app import limsprocess