#!/usr/bin/env python3
import json
import os
import codecs

import pandas as pd

from Lib.spacy_sent_connections import spacy_sent_connections

from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from werkzeug.wrappers import Response
from flask import Flask, render_template, request, flash, redirect, send_from_directory, make_response, Markup
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MONGO_URI'] = "mongodb://127.0.0.1:27019/NLP_db"
mongo = PyMongo(app)

ROOT = os.getcwd()
client = MongoClient("mongodb://127.0.0.1:27019")

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
            main_app.db.find_one_and_update({"username": main_app.username},
                                            {"$set": {"uploads": [text]}},
                                            return_document=ReturnDocument.AFTER)

            freeInputText = os.path.join(app.config['UPLOAD_FOLDER'])
            os.makedirs(freeInputText, exist_ok=True)
            with open(os.path.join(freeInputText, "data.txt"), "w") as outputPath:
                outputPath.write(text)
                outputPath.close()
        else:
            main_app.remove_upload_file()
            files = request.files.getlist('inputFileNames')
            for file in files:
                if file and allowed_file(file.filename):
                    if file.filename.rsplit('.')[-1] == 'json':
                        filename = secure_filename(file.filename)
                        new_file = file.stream.read()
                        text = json.loads(new_file.decode("utf-8"))
                        main_app.db.find_one_and_update({"username": main_app.username},
                                                        {"$set": {
                                                            "repository": [{"filename": filename, "text": text}]}},
                                                        return_document=ReturnDocument.AFTER)

                        # file.stream.seek(0)
                        # repo_user_dir = os.path.join(app.config['REPO_FOLDER'])
                        # os.makedirs(repo_user_dir, exist_ok=True)
                        # file.save(os.path.join(repo_user_dir, filename))
                        # file.close()

                    else:
                        filename = secure_filename(file.filename)
                        new_file = file.stream.read()
                        text = new_file.decode("utf-8")
                        main_app.db.find_one_and_update({"username": main_app.username},
                                                        {"$set": {"uploads": [{"filename": filename, "text": text}]}},
                                                        return_document=ReturnDocument.AFTER)

                        # file.stream.seek(0)
                        # upload_file_user_dir = os.path.join(app.config['UPLOAD_FOLDER'])
                        # os.makedirs(upload_file_user_dir, exist_ok=True)
                        # file.save(os.path.join(upload_file_user_dir, filename))
                        # file.close()

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
    main_app_user = spacy_sent_connections(username=cookie_name)
    html_in_browser = main_app_user.db.find({"username": main_app_user.username})[0]["downloads"][0]['data.html']
    userItems = main_app_user.db.find({"username": main_app_user.username})[0]["downloads"][0]['data_ents_list.json']

    # DOWNLOAD_FOLDER = spacy_sent_connections(username=cookie_name)
    # DOWNLOAD_FOLDER = DOWNLOAD_FOLDER.create_env_dir()[2]
    # userItems = codecs.open(os.path.join(DOWNLOAD_FOLDER, "data.html"), 'r', encoding='utf-8')
    # # html_in_browser = userItems.read()
    #
    # userItems_plotly = codecs.open(os.path.join(DOWNLOAD_FOLDER, "plot_data.html"), 'r', encoding='utf-8')
    # plotly_chart = userItems_plotly.read()
    # with open(os.path.join(DOWNLOAD_FOLDER, "data_ents_list.json"), 'r+') as userItems:
    #     userItems = json.load(userItems)

    all_items = []
    for i in userItems:
        all_items.append(list([i, userItems[i]]))

    html_in_browser = Markup(html_in_browser)
    if not app.config['RENDER_VIZ']:
        html_in_browser = None

    if app.config['ploty_viz']:
        plotly_chart = app.config['ploty_viz']

    user = mongo.db.users.find_one_or_404({"username": main_app_user.username})['downloads'][0]

    return render_template("app_finish.html", html_in_browser=html_in_browser, plotly_chart=plotly_chart,
                           json_ents_list=all_items, user=user)


@app.route('/out/<filename>')
def downloaded_file(filename):
    global main_app_user
    cookie_name = request.cookies.get('username')
    main_app_user = spacy_sent_connections(username=cookie_name)

    DOWNLOAD_FOLDER = main_app_user.create_env_dir()[2]
    return send_from_directory(os.path.join(DOWNLOAD_FOLDER), filename)


@app.route('/out/<filename>')
def downloaded_file_db(filename, file):
    global main_app_user
    cookie_name = request.cookies.get('username')
    main_app_user = spacy_sent_connections(username=cookie_name)
    file_out = main_app_user.download_file(filename=filename, file=file)

    response = Response(file_out, mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename=filename)

    return response
