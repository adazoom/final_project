from flask import Flask
from flask_socketio import SocketIO
from flask_socketio import emit

app = Flask(__name__)
sockets = SocketIO(app)


@sockets.on('ping')
def echo_socket(ws):
    print("emit received")

@app.route('/refresh')
def refresh():
    print('refresh was req')
    sockets.emit('refresh')
    return 'refresh'

@app.route('/left')
def left():
    print('left was req')
    sockets.emit('left')
    return 'left'

@app.route('/center')
def center():
    print('center was req')
    return 'center'

@app.route('/right')
def right():
    print('right was req!')
    sockets.emit('right')
    return 'right'

if __name__ == "__main__":
    print("hi im here")
    server = sockets.run(app, host="localhost", port=5000, debug=True)

