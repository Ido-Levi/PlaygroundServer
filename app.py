from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from datetime import datetime
import json


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'howdy'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

channels = {
    "foods" : ['foods','Start of history (yes, even before the big bang)'],
    "drinks" : ['drinks','Start of history (yes, even before the big bang)'],
    "tech" : ['tech','Start of history (yes, even before the big bang)']
}



msgs_history = ['Start of history (yes, even before the big bang)']

@socketio.on('message')
def handleMessage(msg):
    if msg != "User has connected!":
        channels[msg['channel']].append(datetime.now().strftime('%H:%M:%S')+': '+msg['message'])
        send(channels[msg['channel']], broadcast=True)
    else:
        send(channels['foods'], broadcast=True)
    

@app.route('/<name>')
def getMsgs(name):
    msgs = channels[name]
    return json.dumps(msgs)

if __name__ == '__main__':
    socketio.run(app, host="localhost")
