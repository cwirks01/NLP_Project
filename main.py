#!/usr/bin/env python3
from werkzeug.utils import secure_filename

from Lib.spacy_sent_connections import spacy_sent_connections
from flask import Flask, render_template, request, flash, redirect
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ROOT = os.getcwd()

# file Upload
UPLOAD_FOLDER = os.path.join(ROOT, 'uploads')
# file repository
REPO_FOLDER = os.path.join(UPLOAD_FOLDER, 'repo')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# file Download
DOWNLOAD_FOLDER = os.path.join(ROOT, 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPO_FOLDER'] = REPO_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', "json"}


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
        files = request.files.getlist('inputFileNames')
        for file in files:
            if file and allowed_file(file.filename):
                if file.filename.rsplit('.')[-1] == 'json':
                    file.save(os.path.join(app.config['REPO_FOLDER'], filename))
                else:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File(s) successfully uploaded')
        return redirect('/processing/')


# @app.route("/processing/")
# def process_files_page():
#     return render_template("processing_file.html")


@app.route("/processing/", methods=['GET', 'POST'])
def process_files():
    main_app = spacy_sent_connections()
    main_app.read_file()
    return redirect("/application_ran")


@app.route("/application_ran")
def complete_app():
    return render_template("app_finish.html")


if __name__ == '__main__':
    app.secret_key = "super secret key"
    app.run(host="0.0.0.0", port=8000, debug=True)
