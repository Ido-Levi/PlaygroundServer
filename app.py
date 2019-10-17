from flask import Flask, request, url_for
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from flask_pymongo import PyMongo
import asyncio
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'howdy'
app.config['MONGO_URI'] = 'mongodb://IdosSide:1234567p@cluster0-shard-00-00-nwwjr.mongodb.net:27017,cluster0-shard-00-01-nwwjr.mongodb.net:27017,cluster0-shard-00-02-nwwjr.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority'
mongo = PyMongo(app)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

def getChannelMessages(channelName):
    if channelName == 'foods': 
        return [i['time']+ ': ' + i['message'] for i in list(mongo.db.foods.find({}))]
    elif channelName == 'drinks':
        return [i['time']+ ': ' + i['message'] for i in list(mongo.db.drinks.find({}))]
    elif channelName == 'tech':
        return [i['time']+ ': ' + i['message'] for i in list(mongo.db.tech.find({}))]

def writeMessage(message, channel):
    if channel == 'foods':    
        mongo.db.foods.insert({'message':message, 'time': datetime.now().strftime('%H:%M:%S')})
    elif channel == 'drinks':
        mongo.db.drinks.insert({'message':message, 'time': datetime.now().strftime('%H:%M:%S')})
    elif channel == 'tech':
        mongo.db.tech.insert({'message':message, 'time': datetime.now().strftime('%H:%M:%S')})
    
@socketio.on('message')
def handleMessage(msg):
    if msg != "User has connected!":
        writeMessage(msg['message'], msg['channel'])
        send(getChannelMessages(msg['channel']), broadcast=True)
    else:
        send(getChannelMessages('foods'), broadcast=True)
    
@app.route('/<name>')
def getMsgs(name):
    msgs = getChannelMessages(name)
    return json.dumps(msgs)

if __name__ == '__main__':
    socketio.run(app, host="localhost")
