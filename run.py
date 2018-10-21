import signal
import sys
import traceback
import logging

from flask import Flask, jsonify
from lib.errors import RestException

app = Flask(__name__)

# Set logger:
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s][%(process)d][%(levelname)s]: %(message)s',
                              datefmt='%d-%m-%Y %H:%M:%S %z')
handler.setFormatter(formatter)
default_handlers = app.logger.handlers[:]
for default_handler in default_handlers:
    app.logger.removeHandler(default_handler)  # <-- removing default handlers

app.logger.addHandler(handler)
app.logger.setLevel('DEBUG')

# Register blueprints:
from test_app.views import address_api
app.register_blueprint(address_api)


# Add handlers:
def signal_handler(_signal, _frame):
    app.logger.warning('Application shutting down...')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


@app.errorhandler(RestException)
def handle_rest_exception(err):
    app.logger.error(err.log_message) if err.log_message else None
    response = jsonify(err.to_dict())
    response.status_code = err.status_code
    return response


@app.errorhandler(StandardError)
def handle_standard_error(err):
    app.logger.error('%s occurred!\n%s' % (type(err).__name__, traceback.format_exc()))

    response = jsonify({'success': False, 'errorMessage': 'system_error', 'code': 500})
    response.status_code = 500
    return response
