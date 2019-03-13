from flask import Flask
from flask_socketio import SocketIO
from flask import render_template

app = Flask(__name__, template_folder='turn')
app.config['STATIC_FOLDER'] = None
app.pupil_event_queue = None

sockets = SocketIO(app)


@sockets.on('recenter')
def recenter():
    print('Recenter queued')
    if app.pupil_event_queue:
        app.pupil_event_queue.put({
            'id': 'recenter',
        })


@sockets.on('align_left')
def align_left():
    print('Align Left queued')
    if app.pupil_event_queue:
        app.pupil_event_queue.put({
            'id': 'align_left',
        })


@sockets.on('align_right')
def align_right():
    print('Align Right queued')
    if app.pupil_event_queue:
        app.pupil_event_queue.put({
            'id': 'align_right',
        })


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

@app.route('/')
def index():
    return render_template('index.html')


def webserver(event_queue):
    app.pupil_event_queue = event_queue
    sockets.run(app, host="localhost", port=5000, debug=False)

if __name__ == "__main__":
    sockets.run(app, host="localhost", port=5000, debug=True)

