#coding:UTF-8
__author__ = 'dj'
from flask_socketio import SocketIO
from app import app

socketio = SocketIO(app, async_mode="gevent")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True, use_debugger=use_debugger, use_reloader=use_debugger)