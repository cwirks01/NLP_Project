#!/usr/bin/env python3
from werkzeug.utils import secure_filename

from Lib.spacy_sent_connections import spacy_sent_connections
from flask import Flask, render_template, request, flash, redirect
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def main():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'inputFileNames' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['inputFileNames']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect(request.url)
        else:
            flash('Allowed file types are txt, pdf, and csv')
            return redirect('/')


@app.route("/processing/", methods=['POST'])
def process_files():
    main_app = spacy_sent_connections()
    main_app.read_file()
    return render_template("processing_file.html")


@app.route("/application_ran")
def complete_app():
    return render_template("")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
