from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)

app.secret_key = "super-secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024