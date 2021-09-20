#!/usr/bin/env python3
import json
import os
import codecs

from werkzeug.utils import secure_filename
from Lib.spacy_sent_connections import spacy_sent_connections
from flask import Flask, render_template, request, flash, redirect, send_from_directory, make_response, Markup

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ROOT = os.getcwd()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', "json"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/nlp_project")
def main():
    global main_app
    try:
        cookie_name = request.cookies.get('username')
        if cookie_name is None:
            main_app = spacy_sent_connections()
            main_app.create_env_dir()
            main_app.remove_old_files()
            cookie_name = main_app.username
            resp = make_response(render_template('index.html'))
            resp.set_cookie('username', cookie_name)
            return resp
        else:
            main_app = spacy_sent_connections(username=cookie_name)
            main_app.create_env_dir()
            main_app.remove_old_files()
            return render_template('index.html')

    except Exception as e:
        print("%s \n moving on" % e)
        pass
        return render_template('index.html')


@app.route('/nlp_project', methods=['GET', 'POST'])
def upload_file():
    global main_app
    if request.method == 'POST':
        cookie_name = request.cookies.get('username')
        main_app = spacy_sent_connections(username=cookie_name)
        app.config['UPLOAD_FOLDER'], app.config['REPO_FOLDER'], app.config[
            'DOWNLOAD_FOLDER'] = main_app.create_env_dir()
        # check if the post request has the file part
        app.config['RENDER_VIZ'] = bool(request.form.get("renderViz"))
        app.config['ploty_viz'] = bool(request.form.get("ploty_viz"))
        if (request.files['inputFileNames'].filename in ['', None]) and (request.form.getlist(
                "FreeInputText") in [[''], [None]]):
            flash('No files loaded!')
            return redirect('/nlp_project')

        if not request.form.getlist("FreeInputText") in [[''], None]:
            text = request.form.getlist("FreeInputText")[0]
            freeInputText = os.path.join(app.config['UPLOAD_FOLDER'])
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
                        repo_user_dir = os.path.join(app.config['REPO_FOLDER'])
                        os.makedirs(repo_user_dir, exist_ok=True)
                        file.save(os.path.join(repo_user_dir, filename))
                    else:
                        filename = secure_filename(file.filename)
                        upload_file_user_dir = os.path.join(app.config['UPLOAD_FOLDER'])
                        os.makedirs(upload_file_user_dir, exist_ok=True)
                        file.save(os.path.join(upload_file_user_dir, filename))

        flash('File(s) successfully uploaded')
        return redirect('/processing/')


@app.route("/processing/", methods=['GET', 'POST'])
def process_files():
    global main_app_user
    cookie_name = request.cookies.get('username')
    main_app_user = spacy_sent_connections(username=cookie_name)
    main_app_user.create_env_dir()
    main_app_user.inBrowser = app.config['RENDER_VIZ']
    main_app_user.run()
    return redirect("/application_ran")


@app.route("/application_ran", methods=['GET', 'POST'])
def complete_app():
    global main_app_user
    cookie_name = request.cookies.get('username')
    DOWNLOAD_FOLDER = spacy_sent_connections(username=cookie_name)
    DOWNLOAD_FOLDER = DOWNLOAD_FOLDER.create_env_dir()[2]
    userItems = codecs.open(os.path.join(DOWNLOAD_FOLDER, "data.html"), 'r')
    html_in_browser = userItems.read()
    userItems_plotly = codecs.open(os.path.join(DOWNLOAD_FOLDER, "plot_data.html"), 'r')
    plotly_chart = userItems_plotly.read()
    # userItems.close()

    html_in_browser = Markup(html_in_browser)
    if not app.config['RENDER_VIZ']:
        html_in_browser = None
    
    if app.config['ploty']:
        plotly_chart=app.config['ploty']

    return render_template("app_finish.html", html_in_browser=html_in_browser, plotly_chart=plotly_chart)


@app.route('/out/<filename>')
def downloaded_file(filename):
    cookie_name = request.cookies.get('username')
    DOWNLOAD_FOLDER = spacy_sent_connections(username=cookie_name)
    DOWNLOAD_FOLDER = DOWNLOAD_FOLDER.create_env_dir()[2]
    return send_from_directory(os.path.join(DOWNLOAD_FOLDER), filename)
