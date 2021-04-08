import requests
import logging
import sys
import opentracing
from flask import Flask, jsonify, request
from jaeger_client import Config
from flask_opentracing import FlaskTracer

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(name)s %(threadName)s : %(message)s'
)

def initialize_tracer():
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'local_agent': {'reporting_host': 'jaeger'},
            'logging': True,
        },
        service_name='app-frontend'
    )
    return config.initialize_tracer()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

flask_tracer = FlaskTracer(initialize_tracer, True, app)

@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())


@app.route('/')
def call_backend():
    parent_span = flask_tracer.get_span()
    with opentracing.tracer.start_span('call_backend', child_of=parent_span) as span:
        span.set_tag('http.url', 'http://app-backend:5000/api/v1/list')
        span.set_tag('appname', 'app-frontend')
        span.log_kv({'event': 'test message', 'method': 'GET'})
        inventory = requests.get('http://app-backend:5000/api/v1/list')
        span.set_tag('http.status_code', inventory.status_code)

    with opentracing.tracer.start_span('parse_json', child_of=parent_span) as span:
        json = inventory.json()
        span.set_tag('get_inventory_from_api', len(json))
        span.log_kv({'event': 'got inventory count', 'value': len(json)})

    return jsonify(json)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
