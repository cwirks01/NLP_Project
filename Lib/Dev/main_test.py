#!/usr/bin/env python3
import json
import os
import codecs

from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, flash, redirect, send_from_directory, make_response, Markup

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ROOT = os.getcwd()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', "json"}

@app.route("/application_ran", methods=['GET', 'POST'])
def complete_app():
    
    DOWNLOAD_FOLDER = "C:\\Users\\wirksc\\NTC Tools\\NLP_Project\\data\\e2b9a4a429008824c88bb99f5a843a193047c3c7e173b14216f7b1690e45b581\\downloaded"
    userItems = codecs.open(os.path.join(DOWNLOAD_FOLDER, "data.html"), 'r')
    html_in_browser = userItems.read()
    html_in_browser = Markup(html_in_browser)
    if not True:
        html_in_browser = None
    
    if True:
        plotly_chart=True

    return render_template("app_finish.html", html_in_browser=html_in_browser, plotly_chart=plotly_chart)

@app.route('/out/<filename>')
def downloaded_file(filename):
    DOWNLOAD_FOLDER = "C:\\Users\\wirksc\\NTC Tools\\NLP_Project\\data\\e2b9a4a429008824c88bb99f5a843a193047c3c7e173b14216f7b1690e45b581\\downloaded"
    return send_from_directory(os.path.join(DOWNLOAD_FOLDER), filename)


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)