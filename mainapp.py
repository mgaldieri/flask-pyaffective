from flask import Flask, render_template
from flask.ext.socketio import SocketIO
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


@app.route('/affective')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app)
