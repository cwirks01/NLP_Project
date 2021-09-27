import threading

from main import app

app = app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)

if __name__ == '__main__':
    threading.Thread(target=lambda: app).start()
