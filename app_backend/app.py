# https://medium.com/analytics-vidhya/setting-up-logging-in-python-and-flask-application-the-right-way-e4489c759e8d
from flask import Flask, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, pre_load
from os import environ
import sys
import logging
import requests
import opentracing
from jaeger_client import Config
from flask_opentracing import FlaskTracer

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(name)s %(threadName)s : %(message)s'
)

MYSQL_USER     = environ['MYSQL_USER']
MYSQL_PASSWORD = environ['MYSQL_PASSWORD']
MYSQL_HOST     = environ['MYSQL_HOST']
MYSQL_DATABASE = environ['MYSQL_DATABASE']

def initialize_tracer():
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'local_agent': {'reporting_host': 'jaeger'},
            'logging': True,
        },
        service_name='app-backend'
    )
    return config.initialize_tracer()

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{passwd}@{host}/{db}'.format(
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    db=MYSQL_DATABASE
)

flask_tracer = FlaskTracer(initialize_tracer, True, app)

db = SQLAlchemy(app)

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    category = db.Column(db.String(1000))

class InventorySchema(Schema):
    class Meta:
        fields = ('id', 'name', 'category')
        ordered = True

    id = fields.Int(dump_only=True)
    name = fields.Str()
    category = fields.Str()

@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())

@app.route('/api/v1/list')
def dbcall():
    parent_span = flask_tracer.get_span()
    with opentracing.tracer.start_span('query_database', child_of=parent_span) as span:
        span.set_tag('database.hostname', 'app-database')
        span.set_tag('appname', 'app-backend')
        inventory_schema = InventorySchema(many=True)
        all_inventory = Inventory.query.all()
        if all_inventory:
            db_query_status = 'ok'
        else:
            db_query_status = 'error'
        span.set_tag('db_query.status', db_query_status)

    with opentracing.tracer.start_span('serialize_db_result', child_of=parent_span) as span:
        result = inventory_schema.dump(all_inventory)
        span.set_tag('serialized_using_ma', True)

    return {"inventory": result}

if __name__ == '__main__':
    db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
