from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask_jwt import JWT, jwt_required, current_identity
from flask import Flask, jsonify, request, make_response
import jwt 
import datetime
from functools import wraps

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


                                                                       
limiter = Limiter(app,
    key_func=get_remote_address,
    default_limits=["5 per minute"])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/protected')
@limiter.limit("5 per minute")
@token_required
def upload_form():
    return render_template('upload.html')

@app.route('/protected', methods=['POST'])
@limiter.limit("5 per minute")
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded and displayed')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route("/display/<filename>")
@limiter.limit("5 per minute")
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

app.config['SECRET_KEY'] = 'your-256-bit-secret'
if __name__ == "__main__":
    app.run()