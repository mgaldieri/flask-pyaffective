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
    ocean = OCEAN(openness=float(data.get('openness')),
                  conscientiousness=float(data.get('conscientiousness')),
                  extraversion=float(data.get('extraversion')),
                  agreeableness=float(data.get('agreeableness')),
                  neuroticism=float(data.get('neuroticism')))
    agent.set_personality(ocean)
    emit('ocean_updated', {'x': ocean.pad.state[0],
                           'y': ocean.pad.state[1],
                           'z': ocean.pad.state[2],
                           'mood': ocean.pad.mood().capitalize()}, broadcast=True)


@socketio.on('occ', namespace='/socket')
def occ_rcv(data):
    occ = OCC(admiration=float(data.get('admiration')),
              gloating=float(data.get('gloating')),
              gratification=float(data.get('gratification')),
              gratitude=float(data.get('gratitude')),
              hope=float(data.get('hope')),
              happy_for=float(data.get('happy_for')),
              joy=float(data.get('joy')),
              liking=float(data.get('liking')),
              love=float(data.get('love')),
              pride=float(data.get('pride')),
              relief=float(data.get('relief')),
              satisfaction=float(data.get('satisfaction')),
              anger=float(data.get('anger')),
              disliking=float(data.get('disliking')),
              disappointment=float(data.get('disappointment')),
              distress=float(data.get('distress')),
              fear=float(data.get('fear')),
              fears_confirmed=float(data.get('fears_confirmed')),
              hate=float(data.get('hate')),
              pity=float(data.get('pity')),
              remorse=float(data.get('remorse')),
              reproach=float(data.get('reproach')),
              resentment=float(data.get('resentment')),
              shame=float(data.get('shame')))
    agent.put(occ)
    emit('occ_updated', {'x': occ.pad.state[0],
                         'y': occ.pad.state[1],
                         'z': occ.pad.state[2],
                         'mood': occ.pad.mood()}, broadcast=True)

@socketio.on('mood_get', namespace='/socket')
def mood_get_rcv():
    pass


@app.route('/affective')
def hello_world():
    return render_template('index.html')

@app.route('/canvas')
def canvas():
    return render_template('canvas.html')


if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', 5000)
