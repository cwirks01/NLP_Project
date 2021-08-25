from Lib.spacy_sent_connections import spacy_sent_connections
from flask import Flask, Response

app = Flask(__name__)


@app.route("/")
def main():
    Response("Running Application...", mimetype='text/plain')
    print("Running Application...")
    main_app = spacy_sent_connections()
    main_app.read_file()
    return "Document Successfully Processed!"


if __name__ == '__main__':
    app.run(debug=True)
