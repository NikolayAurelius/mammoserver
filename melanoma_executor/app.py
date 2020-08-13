from flask import Flask, request, redirect, flash, url_for, jsonify
from models import model, runModel
import os
from datetime import datetime
import numpy as np

WORKDIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = f'{WORKDIR}/uploads'
ALLOWED_EXTENSIONS = {'jpg', }

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/melanoma', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'error': True, 'error_type': 'No file part'})

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)

        if file and allowed_file(file.filename):
            print(file.filename)
            filename = f'{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.jpg'
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            diagns = runModel(os.path.join(UPLOAD_FOLDER, filename), model)
            result = diagns
            return jsonify({'error': False, 'result': result})
        else:
            return jsonify({'error': True})

    return f'''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run()