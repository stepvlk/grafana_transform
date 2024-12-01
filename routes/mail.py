from flask import Blueprint, request, jsonify, Response
mail = Blueprint('mail', __name__)
import datetime
import time
from functions.chaker import Checker
from functions.base_state import collection_alert_mail


@mail.route('/mail', methods=['POST'])
def alert():
    start_time = time.time()
    ts = int(datetime.datetime.now().timestamp())
    dt = datetime.datetime.utcnow().strftime("%d %B %Y %I:%M%p")
    if request.method == "POST":
        query = request.get_json()
        try:
            query['timestamp'] = ts
            collection_alert_mail.insert_one(query)
        except:
            pass
        result = Checker.checker_mail(request.get_json(), request.args['chat'])
        return jsonify({'data': 'ok'}), 200
    else:
        pass