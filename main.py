#!/usr/bin/env python3
from werkzeug.utils import secure_filename

from Lib.spacy_sent_connections import spacy_sent_connections
from flask import Flask, render_template, request, flash, redirect, send_from_directory
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
DOWNLOAD_FOLDER = os.path.join(ROOT, 'downloaded')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
print(os.listdir(ROOT))

app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPO_FOLDER'] = REPO_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', "json"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/nlp_project")
def main():
    print(os.listdir(os.getcwd()))
    return render_template("index.html")


@app.route('/nlp_project', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        app.config['RENDER_VIZ'] = bool(request.form.get("renderViz"))
        if ('inputFileNames' not in request.files) and not bool(request.form.getlist("FreeInputText")):
            flash('No file part')
            return redirect(request.url)

        if not request.form.getlist("FreeInputText") in [[''], None]:
            text = request.form.getlist("FreeInputText")[0]
            with open(os.path.join(app.config['UPLOAD_FOLDER'], "data.txt"), "w") as outputPath:
                outputPath.write(text)
                outputPath.close()
        else:
            files = request.files.getlist('inputFileNames')
            for file in files:
                if file and allowed_file(file.filename):
                    if file.filename.rsplit('.')[-1] == 'json':
                        filename = secure_filename(file.filename)
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
    processing_template()
    viz_display = app.config['RENDER_VIZ']
    main_app = spacy_sent_connections(inBrowser=viz_display)
    main_app.read_file()
    return redirect("/application_ran")


def processing_template():
    return render_template("processing_file.html")


@app.route("/application_ran", methods=['GET', 'POST'])
def complete_app():
    return render_template("app_finish.html")


@app.route('/out/<filename>')
def downloaded_file(filename):
    print(filename)
    return send_from_directory(app.config["DOWNLOAD_FOLDER"], filename)


if __name__ == '__main__':
    app.secret_key = "super secret key"
    app.run(host="0.0.0.0", port=80, debug=True)
