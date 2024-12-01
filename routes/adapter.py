from flask import Blueprint, request, jsonify, Response
adapter = Blueprint('adapter', __name__)
import datetime
from functions.chacker import Checker
from functions.base_state import collection_alert

@adapter.route('/alerting/health', methods=['GET'])
def get_health():
    return jsonify({'status': 'Started'}), 200

#/alerting/api/v1/adapter?chat=TEST
@adapter.route('/alerting/api/v1', methods=['POST'])
def alert():
    print(request.get_json())
    ts = int(datetime.datetime.now().timestamp())
    if request.method == "POST":
        query = request.get_json()
        try:
            query['timestamp'] = ts
            collection_alert.insert_one(query)
        except:
            pass
        Checker.checker_webhook(request.get_json(), request.args['chat'])
        return jsonify({'data': 'transaction finish'}), 200
    else:
        pass

