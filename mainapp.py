from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from logging import Formatter, StreamHandler
import logging

app = Flask(__name__)
app.config['SECRET_KET'] = 'secret!'
socketio = SocketIO(app)

log_handler = StreamHandler()
log_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

app.logger.info('*****\n\t\t\tAPP STARTED')

from pyaffective.agent import Agent
from pyaffective.emotions import OCC, OCEAN, PAD

agent = Agent()


@socketio.on('ocean', namespace='/socket')
def ocean_rcv(data):
    print 'socket recieved'
    print 'Data neuroticism: ' + str(data.get('neuroticism'))
    ocean = OCEAN(openness=float(data.get('openness')),
                  conscientiousness=float(data.get('conscientiousness')),
                  extraversion=float(data.get('extraversion')),
                  agreeableness=float(data.get('agreeableness')),
                  neuroticism=float(data.get('neuroticism')))
    agent.personality = ocean
    #print ocean.pad.state
    emit('ocean_updated', {'x':ocean.pad.state[0],
                           'y':ocean.pad.state[1],
                           'z':ocean.pad.state[2],
                           'mood':ocean.pad.mood().capitalize()}, broadcast=True)


@app.route('/affective')
def hello_world():
    return render_template('index.html')

@app.route('/canvas')
def canvas():
    return render_template('canvas.html')


if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', 5000)
