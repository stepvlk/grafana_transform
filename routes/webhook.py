from flask import Blueprint, request, jsonify, Response
webhook = Blueprint('webhook', __name__)
import datetime
from functions.chacker import Checker
from functions.chacker import Checker_New_Alerting
from functions.base_state import collection_alert

@webhook.route('/alerting/health', methods=['GET'])
def get_health():
    return jsonify({'status': 'Started'}), 200

#/alerting/api/v1/telegram?chat=-4530347279
@webhook.route('/alerting/api/v1/telegram', methods=['POST']) 
def alert():
    ts = int(datetime.datetime.now().timestamp())
    if request.method == "POST":
        query = request.get_json()
        if 'alerts' in query:
            pass
        else:
            try:
                query['timestamp'] = ts
                collection_alert.insert_one(query)
            except:
                pass
            Checker.checker_webhook(request.get_json(), request.args['chat'])
        return jsonify({'data': 'transaction finish'}), 200
    else:
        return jsonify({'status': 'only POST request'}), 405

#/alerting/api/v2/telegram?chat=-4530347279
@webhook.route('/alerting/api/v2/telegram', methods=['POST']) 
def alert_new():
    ts = int(datetime.datetime.now().timestamp())
    if request.method == "POST":
        query = request.get_json()
        try:
            query['timestamp'] = ts
            collection_alert.insert_one(query)
        except:
            pass
        Checker_New_Alerting.transform(request.get_json(), request.args['chat'], request.args['thread'] if 'thread' in request.args else None) 
        return jsonify({'data': 'transaction finish'}), 200
    else:
        return jsonify({'status': 'only POST request'}), 405