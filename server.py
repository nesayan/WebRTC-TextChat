from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

ROOM = "room"

app = Flask(__name__)
socket = SocketIO(app)

clients = []

@app.route('/')
def index():
    return render_template('client.html')

@socket.on('connect')
def conn():
    clients.append(request.sid)
    emit('sid', request.sid, broadcast=False)
    emit('ready', room=ROOM, skip_sid=request.sid)
    join_room(room=ROOM,sid=request.sid)
    print("[ CLIENT CONNECTED ]", request.sid)

@socket.on('disconnect')
def disconn():
    clients.remove(request.sid)
    leave_room(room=ROOM, sid=request.sid)
    print("[ CLIENT DISCONNECTED ]", request.sid)

@socket.on('data')
def emitData(data):
    print('Message from {}: {}'.format(request.sid, data))
    emit('data', data, room=ROOM, skip_sid=request.sid)

if __name__ == "__main__":
    socket.run(app)