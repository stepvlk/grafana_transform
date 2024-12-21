from flask import Blueprint, request, jsonify, make_response
system = Blueprint('system', __name__)
import datetime

from pymongo import MongoClient
import datetime
from config.config import config

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



@system.route('/alerting/deleter', methods=['GET'])
def deleter():
    ts = int(datetime.datetime.now().timestamp()) - 600
    try:
        collection_status.delete_one({"timestamp": {"$lt" : ts}})
        collection_status_mail.delete_one({"timestamp": {"$lt" : ts}})
    except:
        pass
    return jsonify({"status": "delete_old_alert_rules"}), 200

@system.route('/alerting/monitoring', methods=['GET'])
def monitoring():
    
    text = f"grafana_alerting_status,status_cache=test no_data_count={collection_status.count_documents({})},mongo_alerts_count={collection_alert.count_documents({})},mongo_mail_count={collection_alert_mail.count_documents({})}"
    response = make_response(text)
    response.mimetype = "text/plain"
    return response 

