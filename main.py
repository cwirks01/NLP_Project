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
from flask import Flask, render_template, request, flash, redirect, send_from_directory, make_response, Markup, url_for
from flask_pymongo import PyMongo

MONGO_DB_USERNAME = os.environ['MONGO_DB_USERNAME']
MONGO_DB_PASSWORD = os.environ['MONGO_DB_PASSWORD']

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# app.config['MONGO_URI'] = "mongodb://%s:%s127.0.0.1:27019/NLP_db" % (MONGO_DB_USERNAME,MONGO_DB_PASSWORD)
app.config['MONGO_URI'] = 'mongodb://mongodb:27017/NLP_db'
# app.config['MONGO_URI'] = 'mongodb://192.168.0.18:27019/NLP_db' # for debugging
mongo = PyMongo(app)

ROOT = os.getcwd()
# client = MongoClient("mongodb://%s:%s127.0.0.1:27019" % (MONGO_DB_USERNAME,MONGO_DB_PASSWORD))
client = MongoClient('mongodb://mongodb:27017')
# client = MongoClient('mongodb://192.168.0.18:27019')  # for debuging

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
            cookie_name = main_app.username
            resp = make_response(render_template('index.html'))
            resp.set_cookie('username', cookie_name)
            return resp

        else:
            main_app = spacy_sent_connections(username=cookie_name)
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

        else:
            files = request.files.getlist('inputFileNames')
            for file_item in files:
                if file_item and allowed_file(file_item.filename):
                    if file_item.filename.rsplit('.')[-1] == 'json':
                        filename = secure_filename(file_item.filename)
                        new_file = file_item.stream.read()
                        text = json.loads(new_file.decode("utf-8"))
                        main_app.db.find_one_and_update({"username": main_app.username},
                                                        {"$set":
                                                             {"repository":
                                                                  [{"filename": filename, "text": text}]}},
                                                        return_document=ReturnDocument.AFTER)

                    else:
                        filename = secure_filename(file_item.filename)
                        new_file = file_item.stream.read()
                        text = new_file.decode("utf-8")
                        main_app.db.find_one_and_update({"username": main_app.username},
                                                        {"$set": {"uploads": [{"filename": filename, "text": text}]}},
                                                        return_document=ReturnDocument.AFTER)

        flash('File(s) successfully uploaded')
        return redirect('/processing/')


@app.route("/processing/", methods=['GET', 'POST'])
def process_files():
    global main_app_user
    cookie_name = request.cookies.get('username')
    main_app_user = spacy_sent_connections(username=cookie_name)
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

    all_items = []
    for i in userItems:
        all_items.append(list([i, userItems[i]]))

    html_in_browser = Markup(html_in_browser)
    if not app.config['RENDER_VIZ']:
        html_in_browser = None

    if app.config['ploty_viz']:
        plotly_chart = app.config['ploty_viz']

    user_downloads = mongo.db.users.find_one_or_404({"username": main_app_user.username})['downloads'][0]
    plot_data = Markup(user_downloads['plot_data.html'])

    return render_template("app_finish.html", html_in_browser=html_in_browser, plotly_chart=plotly_chart,
                           json_ents_list=all_items, user=user_downloads, plot_data=plot_data)


@app.route('/out/filename/<filename>/file/<file>')
def downloaded_file_db(filename, file):
    cookie_name = request.cookies.get('username')
    main_app_user_db = spacy_sent_connections(username=cookie_name)

    file_out = main_app_user_db.download_file(filename=filename, file_in=file)

    if filename.endswith("html"):
        file_out = Markup(file)
    elif filename.endswith("json"):
        file_out = json.dumps(file_out)
    elif filename.endswith("anx"):
        file_out = file_out
    else:
        file_out = file_out

    response = Response(file_out, mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename=filename)

    return response
