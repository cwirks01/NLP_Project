from main import app


if __name__ == '__main__':
    app.secret_key = "super secret key"
    app.run(host="0.0.0.0", port=5000, debug=True)