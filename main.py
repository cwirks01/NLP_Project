import json
import os
import jsonify

from Lib.spacy_sent_connections import spacy_sent_connections
from Lib.wordCloudApp import cloud_app

from pymongo import MongoClient, ReturnDocument
from werkzeug.utils import secure_filename
from werkzeug.wrappers import Response
from flask import Flask, render_template, request, flash, redirect, Markup
from flask_pymongo import PyMongo

MONGO_DB_USERNAME = os.environ['MONGO_DB_USERNAME']
MONGO_DB_PASSWORD = os.environ['MONGO_DB_PASSWORD']
MONGO_HOST = os.environ['MONGO_HOST']
MONGO_PORT = os.environ['MONGO_PORT']

MONGO_NLP_DB = "NLP_db"
MONGO_USER_DB = "users_db"
MONGODB_NLP_URI = 'mongodb://%s:%s@%s:%s/%s?authSource=admin'% (MONGO_DB_USERNAME,
                                                                MONGO_DB_PASSWORD,
                                                                MONGO_HOST,
                                                                MONGO_PORT,
                                                                MONGO_NLP_DB)
                                                                                    
MONGODB_USER_URI = 'mongodb://%s:%s@%s:%s/%s?authSource=admin'%(MONGO_DB_USERNAME,
                                                                MONGO_DB_PASSWORD,
                                                                MONGO_HOST,
                                                                MONGO_PORT,
                                                                MONGO_USER_DB)
                                                                
app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['MONGO_URI'] = MONGODB_NLP_URI
user_db = MongoClient(MONGODB_USER_URI)
NLP_db = MongoClient(MONGODB_NLP_URI)
mongo = PyMongo(app)

ROOT = os.getcwd()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', "json"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/nlp_project")
def main():
    global main_app
    try:
        cookie_name = request.cookies.get('_cdub_app_username')
        cookie_username = user_db.users_db.user.find_one({"_cookies":cookie_name})
        try:
            text = cookie_username[0]["downloads"][0]['data.csv']
            text = text['']
            image = appWordCloud(text=text)
        except Exception as e:
            print("%s \n moving on" % e)
            text=None
            pass

        if cookie_username is None:
            return redirect("/auth_app", code=302)
                
        else:
            try:
                plot_url = cloud_app(username=cookie_username['email'],db=NLP_db)
            except Exception as e:
                print(e+"\nNew User, Repository has not been established yet.")
                plot_url = False
                pass

            main_app = spacy_sent_connections(username=cookie_username['email'], db=NLP_db.NLP_db)
            return render_template('index.html', plot_url=plot_url, main_app=main_app)

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
        main_app = spacy_sent_connections(username=cookie_username['email'], db=NLP_db.NLP_db)
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
                        if filename.endswith("txt"):
                            text = new_file.decode("utf-8")
                        else:
                            text = main_app.read_in_pdf(file_in=file)
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
    main_app_user = spacy_sent_connections(username=cookie_username['email'], db=NLP_db.NLP_db)
    main_app_user.inBrowser = app.config['RENDER_VIZ']
    main_app_user.previousRun_repo = app.config['createNewRepo']
    main_app_user.run()
    return redirect("/nlp_project/application_ran")

@app.route("/nlp_project/application_ran", methods=['GET', 'POST'])
def complete_app():
    global main_app_user
    cookie_name = request.cookies.get('_cdub_app_username')
    cookie_username = user_db.users_db.user.find_one({"_cookies":cookie_name})
    main_app_user = spacy_sent_connections(username=cookie_username['email'], db=NLP_db.NLP_db)
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
                           json_ents_list=all_items, user=user_downloads, plot_data=plot_data, main_app=main_app_user)


@app.route('/nlp_project/out/<filename>/file', methods=['GET','POST'])
def downloaded_file_db(filename):
    cookie_name = request.cookies.get('_cdub_app_username')
    cookie_username = user_db.users_db.user.find_one({"_cookies":cookie_name})
    main_app_user_db = spacy_sent_connections(username=cookie_username['email'], db=NLP_db.NLP_db)
    
    file_out = main_app_user_db.download_file(filename=filename)

    if filename.endswith("html"):
        file_out = Markup(file_out)

    # elif filename.endswith("json"):
    #     response = jsonify(file_out)
    #     response.headers['Content-Disposition'] = 'attachment;filename=%s'% filename
    #     return response

    elif filename.endswith("anx"):
        file_out = file_out
    else:
        file_out = file_out

    response = Response(file_out, mimetype='text/csv', direct_passthrough=True)
    response.headers.set("Content-Disposition", "attachment", filename=filename)

    return response
