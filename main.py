import json
import os

from Lib.spacy_sent_connections import spacy_sent_connections

from pymongo import MongoClient, ReturnDocument
from werkzeug.utils import secure_filename
from werkzeug.wrappers import Response
from flask import Flask, render_template, request, flash, redirect, Markup
from flask_pymongo import PyMongo

MONGO_DB_USERNAME = os.environ['MONGO_DB_USERNAME']
MONGO_DB_PASSWORD = os.environ['MONGO_DB_PASSWORD']

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MONGO_URI'] = "mongodb://%s:%s@mongodb:27017/NLP_db?authSource=admin" % (MONGO_DB_USERNAME,MONGO_DB_PASSWORD)
# app.config['MONGO_URI'] = 'mongodb://3.89.36.89:27019/NLP_db' # for debugging
mongo = PyMongo(app)

ROOT = os.getcwd()
user_db = MongoClient('mongodb://%s:%s@mongodb:27017/users_db?authSource=admin' % (MONGO_DB_USERNAME,MONGO_DB_PASSWORD))

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', "json"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/nlp_project")
def main():
    global main_app
    try:
        cookie_name = request.cookies.get('_cdub_app_username')
        cookie_username = user_db.users_db.user.find_one({"_cookies":cookie_name})

        if cookie_name is None:
            return redirect("/auth_app", code=302)
                
        else:
            main_app = spacy_sent_connections(username=cookie_username['email'])
            return render_template('index.html')

    except Exception as e:
        print("%s \n moving on" % e)
        pass
        return redirect("/auth_app", code=302)


@app.route('/nlp_project', methods=['GET', 'POST'])
def upload_file():
    global main_app
    if request.method == 'POST':
        cookie_name = request.cookies.get('_cdub_app_username')
        cookie_username = user_db.users_db.user.find_one({"_cookies":cookie_name})
        main_app = spacy_sent_connections(username=cookie_username['email'])
        # check if the post request has the file part
        app.config['createNewRepo'] = bool(request.form.get("createNewRepo"))
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
            for file in files:
                if file and allowed_file(file.filename):
                    if file.filename.rsplit('.')[-1] == 'json':
                        filename = secure_filename(file.filename)
                        new_file = file.stream.read()
                        text = json.loads(new_file.decode("utf-8"))
                        main_app.db.find_one_and_update({"username": main_app.username},
                                                        {"$set":{"repository":
                                                        [{"filename": filename, "text": text}]}},
                                                        return_document=ReturnDocument.AFTER)

                    else:
                        filename = secure_filename(file.filename)
                        new_file = file.stream.read()
                        text = new_file.decode("utf-8")
                        main_app.db.find_one_and_update({"username": main_app.username},
                                                        {"$set": {"uploads":
                                                        [{"filename": filename, "text": text}]}},
                                                        return_document=ReturnDocument.AFTER)

        flash('File(s) successfully uploaded')
        return redirect('/nlp_project/processing/')


@app.route("/nlp_project/processing/", methods=['GET', 'POST'])
def process_files():
    global main_app_user
    cookie_name = request.cookies.get('_cdub_app_username')
    cookie_username = user_db.users_db.user.find_one({"_cookies":cookie_name})
    main_app_user = spacy_sent_connections(username=cookie_username['email'])
    main_app_user.inBrowser = app.config['RENDER_VIZ']
    main_app_user.previousRun_repo = app.config['createNewRepo']
    main_app_user.run()
    return redirect("/nlp_project/application_ran")


@app.route("/nlp_project/application_ran", methods=['GET', 'POST'])
def complete_app():
    global main_app_user
    cookie_name = request.cookies.get('_cdub_app_username')
    cookie_username = user_db.users_db.user.find_one({"_cookies":cookie_name})
    main_app_user = spacy_sent_connections(username=cookie_username['email'])
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


@app.route('/nlp_project/out/filename/<filename>/file/<file>')
def downloaded_file_db(filename, file):
    cookie_name = request.cookies.get('_cdub_app_username')
    cookie_username = user_db.users_db.user.find_one({"_cookies":cookie_name})
    main_app_user_db = spacy_sent_connections(username=cookie_username['email'])

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
    response.headers["X-Accel-Redirect"] = "/downloads/" + filename

    return response
