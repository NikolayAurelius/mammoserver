from flask import Flask, request, redirect, flash, url_for, jsonify
from models import model_1, model_2, model_3, model_4, bad, stranger
import os
from datetime import datetime
import numpy as np
from mammo_packets import read_from_file_binary, parse_mammograph_raw_data, parse_uncompressed_mammograph_packets
from amplitude import meas_to_x

WORKDIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = f'{WORKDIR}/uploads'
ALLOWED_EXTENSIONS = {'bin', 'biz'}

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app = Flask(__name__)
models = [model_1, model_2, model_3, model_4]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
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
            extention = file.filename.rsplit('.', 1)[1].lower()
            filename = f'{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.{extention}'
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
            parser = parse_mammograph_raw_data

            # TODO: Из-за того, что утилита сохраняет всё под одним файлом можем работать только с одним воркером
            if extention == 'biz':
                parser = parse_uncompressed_mammograph_packets
                raise NotImplementedError()

            data = read_from_file_binary(path)
            arr = parser(data)
            x = meas_to_x(arr)

            result = {'bad': bad(x)}

            for model in models:
                result[model.name] = int(model(x)[0].item() * 1000)

            result['result'] = result['torch_model_2']

            result['stranger'] = stranger(np.array([[1000 - result['result'], result['result']]]) / 1000)
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
