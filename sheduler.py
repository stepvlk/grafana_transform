from flask import Flask
from config.config import config
from flask_apscheduler import APScheduler

from prometheus_flask_exporter import PrometheusMetrics

from routes.system import system
from pymongo import MongoClient

import datetime
import logging

app = Flask(__name__, static_folder='', template_folder='')
app.register_blueprint(system, prefix='api/v2/')
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
metrics = PrometheusMetrics(app)
metrics.info('sheduler', 'production_version', version='1.0.0')


base = f"mongodb://{config['db']['user']}:{config['db']['pass']}@{config['db']['url']}"

client_alert = MongoClient(base)
db_alert = client_alert['alerting']
collection_alert = db_alert.grafana_alerting

client_status = MongoClient(base)
db_status = client_status['alerting']
collection_status = db_status.grafana_statuses

client_adapter = MongoClient(base)
db_adapter = client_adapter['alerting']
collection_adapter = db_adapter.grafana_adapter

client_alert_mail = MongoClient(base)
db_alert_mail = client_alert_mail['alerting']
collection_alert_mail = db_alert_mail.grafana_alerting_mail

client_status_mail = MongoClient(base)
db_status_mail = client_status_mail['alerting']
collection_status_mail = db_status_mail.grafana_statuses_mail

client_status_adapter = MongoClient(base)
db_status_adapter = client_status_adapter['alerting']
collection_status_adapter = db_status_adapter.grafana_statuses_adapter

client_repeat = MongoClient(base)
db_repeat = client_repeat['alerting']
collection_repeat = db_alert.grafana_repeat

client_repeat_mail = MongoClient(base)
db_repeat_mail = client_repeat_mail['alerting']
collection_repeat_mail = db_repeat_mail.grafana_repeat_mail

client_repeat_adapter = MongoClient(base)
db_repeat_adapter = client_repeat_adapter['alerting']
collection_repeat_adapter = db_repeat_adapter.grafana_repeat_adapter

def update_statuses():
    try:
        dt = datetime.datetime.utcnow().strftime("%d %B %Y %I:%M%p")
        ts = int(datetime.datetime.now().timestamp()) - 600
        state = collection_status.delete_one({"timestamp": {"$lt" : ts}})
        state_mail = collection_status_mail.delete_one({"timestamp": {"$lt" : ts}})
        logger.info({"jobname": "netserver", "result": state, "result_mail": state_mail, "runtime": dt})
        return {"jobname": "netserver", "result": state, "result_mail": state_mail, "runtime": dt}
    except:
        return {"jobname": "netserver", "status": "fail","runtime": dt}


if __name__ == "__main__":
    
    scheduler = APScheduler()
    scheduler.add_job(func=update_statuses, trigger='interval', id='updater', minutes=1, timezone='Europe/Moscow')

    scheduler.start()
    app.run(host=config['server']['adress'], port=int(config['server']['port']), debug=False)