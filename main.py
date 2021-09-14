#!/usr/bin/env python3
import os

from werkzeug.utils import secure_filename
from Lib.spacy_sent_connections import spacy_sent_connections
from flask import Flask, render_template, request, flash, redirect, send_from_directory

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ROOT = os.getcwd()

# file Upload
UPLOAD_FOLDER = os.path.join(ROOT, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# file repository
REPO_FOLDER = os.path.join(UPLOAD_FOLDER, 'repo')
os.makedirs(REPO_FOLDER, exist_ok=True)

# file Download
DOWNLOAD_FOLDER = os.path.join(ROOT, 'downloaded')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPO_FOLDER'] = REPO_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', "json"}

# main_app = spacy_sent_connections(downloads=app.config['DOWNLOAD_FOLDER'], upload_dir=app.config['UPLOAD_FOLDER'],repo=app.config['REPO_FOLDER'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/nlp_project")
def main():
    global main_app
    main_app = spacy_sent_connections(downloads=app.config['DOWNLOAD_FOLDER'], upload_dir=app.config['UPLOAD_FOLDER'],repo=app.config['REPO_FOLDER'])
    return render_template("index.html")


@app.route('/nlp_project', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        app.config['RENDER_VIZ'] = bool(request.form.get("renderViz"))
        if ('inputFileNames' not in request.files) and not bool(request.form.getlist("FreeInputText")):
            flash('No files loaded!')
            return redirect(request.url)

        if not request.form.getlist("FreeInputText") in [[''], None]:
            text = request.form.getlist("FreeInputText")[0]
            freeInputText = os.path.join(app.config['UPLOAD_FOLDER'], main_app.user_dir)
            os.makedirs(freeInputText, exist_ok=True)
            with open(os.path.join(freeInputText, "data.txt"), "w") as outputPath:
                outputPath.write(text)
                outputPath.close()
        else:
            files = request.files.getlist('inputFileNames')
            for file in files:
                if file and allowed_file(file.filename):
                    if file.filename.rsplit('.')[-1] == 'json':
                        filename = secure_filename(file.filename)
                        repo_user_dir = os.path.join(app.config['REPO_FOLDER'], main_app.user_dir)
                        os.makedirs(repo_user_dir, exist_ok=True)
                        file.save(os.path.join(repo_user_dir, filename))
                    else:
                        filename = secure_filename(file.filename)
                        upload_file_user_dir = os.path.join(app.config['UPLOAD_FOLDER'], main_app.user_dir)
                        os.makedirs(upload_file_user_dir, exist_ok=True)
                        file.save(os.path.join(upload_file_user_dir, filename))

        flash('File(s) successfully uploaded')
        return redirect('/processing/')


# @app.route("/processing/")
# def process_files_page():
#     return render_template("processing_file.html")



@app.route("/processing/", methods=['GET', 'POST'])
def process_files():
    if (os.path.exists(os.path.join(app.config['DOWNLOAD_FOLDER'], main_app.user_dir))):
        for f in os.listdir(os.path.join(app.config['DOWNLOAD_FOLDER'], main_app.user_dir)):
            try:
                os.remove(os.path.join(app.config['DOWNLOAD_FOLDER'], f))
            except:
                continue
    else:
        os.makedirs(os.path.join(app.config['DOWNLOAD_FOLDER'], main_app.user_dir))
    processing_template()
    main_app.inBrowser = app.config['RENDER_VIZ']
    main_app.read_file()
    return redirect("/application_ran")


def processing_template():
    return render_template("processing_file.html")


@app.route("/application_ran", methods=['GET', 'POST'])
def complete_app():
    return render_template("app_finish.html")


@app.route('/out/<filename>')
def downloaded_file(filename):
    return send_from_directory(os.path.join(app.config["DOWNLOAD_FOLDER"], main_app.user_dir), filename)


