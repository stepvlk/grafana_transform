import logging
import time
import datetime
import logging
from functions.base_state import Base
from functions.sender import Sender
import re

logger = logging.getLogger('werkzeug')
logging.basicConfig(level=logging.INFO)
handler = logging.FileHandler('logs/notifications.log')
logger.addHandler(handler)


def check_keys(query):
    
    if 'alertkey' in query['labels']:
        query['labels']['alertkey'] == query['labels']['alertkey']
        return {"state": "fm", "query": query}
    
    elif 'AlertKey' in query['labels']:
        query['labels'].update({"alertkey": query['labels']['AlertKey']})
        return {"state": "fm", "query": query}
    
    elif 'alertKey' in query['labels']:
        query['labels'].update({"alertkey": query['labels']['alertKey']})
        return {"state": "fm", "query": query}
    
    elif 'Alertkey' in query['labels']:
        query['labels'].update({"alertkey": query['labels']['Alertkey']})
        return {"state": "fm", "query": query}
    
    else:
        return {"state": "grf", "query": query}


class Checker():
    
    def checker_webhook(query, chat):
        start_time = time.time()
        ts = int(datetime.datetime.now().timestamp())
        dt = datetime.datetime.utcnow().strftime("%d %B %Y %I:%M%p")
        
        if query['state'] == "no_data":
            
            resp = Base.checker_webhook(query, query['state'])
            
            try:
                logger.info({"timestamp": ts, "rule": "NO_DATA","url":query['ruleUrl'], "state": query['state'], "sending": "skip", "date": dt, "duration": time.time() - start_time, "channel": chat})
                print({"timestamp": ts, "rule": "NO_DATA","url":query['ruleUrl'], "state": query['state'], "sending": "skip", "date": dt, "duration": time.time() - start_time, "channel": chat})
            
            except:
                logger.info({"bad_query": query, "channel": chat})
                print({"timestamp": ts, "bad_query": query, "channel": chat, "date": dt})
        
        elif query['state'] == "ok":
            
            resp = Base.checker_webhook(query, query['state'])
            
            if resp == "pass":
                logger.info({"timestamp": ts, "rule": "OK","url":query['ruleUrl'], "state": query['state'], "sending": "skip", "date": dt, "duration": time.time() - start_time, "channel": chat})
                print({"timestamp": ts, "rule": "OK","url":query['ruleUrl'], "state": query['state'], "sending": "skip", "date": dt, "duration": time.time() - start_time, "channel": chat})
            
            if resp == "send":
                logger.info({"timestamp": ts, "rule": "OK","url":query['ruleUrl'], "state": query['state'], "sending": "send", "date": dt, "duration": time.time() - start_time, "channel": chat})
                Sender.send_message_webhook(query, chat)
                print({"timestamp": ts, "rule": "OK","url":query['ruleUrl'], "state": query['state'], "sending": "send", "date": dt, "duration": time.time() - start_time, "channel": chat})
        
        elif query['state'] == "alerting":
            
            resp = Base.checker_webhook(query, query['state'])
            
            if resp == "pass":
                logger.info({"timestamp": ts, "rule": "ALERTING","url":query['ruleUrl'], "state": query['state'], "sending": "skip", "date": dt, "duration": time.time() - start_time, "channel": chat})
                print({"timestamp": ts,"rule": "ALERTING","url":query['ruleUrl'], "state": query['state'], "sending": "skip", "date": dt, "duration": time.time() - start_time, "channel": chat})
            
            if resp == "send":
                Sender.send_message_webhook(query, chat)
                logger.info({"timestamp": ts, "rule": "ALERTING","url":query['ruleUrl'], "state": query['state'], "sending": "send", "date": dt, "duration": time.time() - start_time, "channel": chat})
                print({"timestamp": ts,"rule": "ALERTING","url":query['ruleUrl'], "state": query['state'], "sending": "send", "date": dt, "duration": time.time() - start_time, "channel": chat}) 
        else:
            pass 

    
    def checker_mail(query, chat):
        start_time = time.time()
        ts = int(datetime.datetime.now().timestamp())
        dt = datetime.datetime.utcnow().strftime("%d %B %Y %I:%M%p")
        
        if query['state'] == "no_data":
            
            resp = Base.checker_mail(query, query['state'])
            
            try:
                logger.info({"timestamp": ts, "rule": "NO_DATA","url":query['ruleUrl'], "state": query['state'], "sending": "skip", "date": dt, "duration": time.time() - start_time, "channel": chat})
                print({"timestamp": ts, "rule": "NO_DATA","url":query['ruleUrl'], "state": query['state'], "sending": "skip", "date": dt, "duration": time.time() - start_time, "channel": chat})
            
            except:
                logger.info({"bad_query": query, "channel": chat})
                print({"timestamp": ts, "bad_query": query, "channel": chat, "date": dt})
        
        elif query['state'] == "ok":
            
            resp = Base.checker_mail(query, query['state'])
            
            if resp == "pass":
                logger.info({"timestamp": ts, "rule": "OK","url":query['ruleUrl'], "state": query['state'], "sending": "skip", "date": dt, "duration": time.time() - start_time, "channel": chat})
                print({"timestamp": ts, "rule": "OK","url":query['ruleUrl'], "state": query['state'], "sending": "skip", "date": dt, "duration": time.time() - start_time, "channel": chat})
            
            if resp == "send":
                logger.info({"timestamp": ts, "rule": "OK","url":query['ruleUrl'], "state": query['state'], "sending": "send", "date": dt, "duration": time.time() - start_time, "channel": chat})
                Sender.send_message_mail(query, chat)
                print({"timestamp": ts, "rule": "OK","url":query['ruleUrl'], "state": query['state'], "sending": "send", "date": dt, "duration": time.time() - start_time, "channel": chat})
        
        elif query['state'] == "alerting":
            
            resp = Base.checker_mail(query, query['state'])
            
            if resp == "pass":
                logger.info({"timestamp": ts, "rule": "ALERTING","url":query['ruleUrl'], "state": query['state'], "sending": "skip", "date": dt, "duration": time.time() - start_time, "channel": chat})
                print({"timestamp": ts,"rule": "ALERTING","url":query['ruleUrl'], "state": query['state'], "sending": "skip", "date": dt, "duration": time.time() - start_time, "channel": chat})
            
            if resp == "send":
                Sender.send_message_mail(query, chat)
                logger.info({"timestamp": ts, "rule": "ALERTING","url":query['ruleUrl'], "state": query['state'], "sending": "send", "date": dt, "duration": time.time() - start_time, "channel": chat})
                print({"timestamp": ts,"rule": "ALERTING","url":query['ruleUrl'], "state": query['state'], "sending": "send", "date": dt, "duration": time.time() - start_time, "channel": chat}) 
        else:
            pass
        
class Checker_New_Alerting():

    def transform(data, chat, thread):

        for res in data['alerts']:
            dashId = re.findall(r'(d)/(.*)\?', res['panelURL'])[0][1]
            orgId = re.search('orgId.*?(\d+)', res['panelURL']).group(1)
            panelId = re.search('viewPanel.*?(\d+)', res['panelURL']).group(1)
            results = []
            if res['status'] == "firing":
                metrics = []
                for k,v in res['values'].items():
                    metric = {k:v, "tag": {}}
                    metrics.append(metric)
                status = "alerting"
                check_FM = check_keys(res)
                if check_FM['state'] == "fm":
                    
                    result = {   "title": res['labels']['alertname'], 
                                    "state": status,
                                    "ruleId": res['labels']['grafana_folder'], 
                                    "ruleName": data['receiver'],
                                    "evalMatches": metrics,
                                    "orgId": int(orgId),
                                    "dashboardId": dashId,
                                    "panelId": int(panelId),
                                    "tags": {"alertkey": res['labels']['alertkey'], "severity": res['labels']['severity']},
                                    "ruleUrl": res['panelURL'],
                                    "message": res['annotations']['description']}
                    results.append(result)
                
                if check_FM['state'] == "grf":
                    if res['annotations'] == {}:
                        
                        result = {   "title": res['labels']['alertname'], 
                                        "state": status,
                                        "ruleId": res['labels']['grafana_folder'], 
                                        "ruleName": data['receiver'],
                                        "evalMatches": metrics,
                                        "orgId": int(orgId),
                                        "dashboardId": dashId,
                                        "panelId": int(panelId),
                                        "tags": res['labels'],
                                        "ruleUrl": res['panelURL'],
                                        "message": "The description field is empty" }
                        results.append(result)
                    if 'description' in res['annotations']:
                        result = {   "title": res['labels']['alertname'], 
                                        "state": status,
                                        "ruleId": res['labels']['grafana_folder'], 
                                        "ruleName": data['receiver'],
                                        "evalMatches": metrics,
                                        "orgId": int(orgId),
                                        "dashboardId": dashId,
                                        "panelId": int(panelId),
                                        "tags": res['labels'],
                                        "ruleUrl": res['panelURL'],
                                        "message": res['annotations']['description'] }
                        results.append(result)
                    else:
                        result = {   "title": res['labels']['alertname'], 
                                        "state": status,
                                        "ruleId": res['labels']['grafana_folder'], 
                                        "ruleName": data['receiver'],
                                        "evalMatches": metrics,
                                        "orgId": int(orgId),
                                        "dashboardId": dashId,
                                        "panelId": int(panelId),
                                        "tags": res['labels'],
                                        "ruleUrl": res['panelURL'],
                                        "message": "The description field is empty" } 
                        results.append(result)
            if res['status'] == "resolved":
                status = "ok"
                check_FM = check_keys(res)
                if check_FM['state'] == "fm":
                    result = {   "title": res['labels']['alertname'], 
                                    "state": status,
                                    "ruleId": res['labels']['grafana_folder'], 
                                    "ruleName": data['receiver'],
                                    "evalMatches": [],
                                    "orgId": int(orgId),
                                    "dashboardId": dashId,
                                    "panelId": int(panelId),
                                    "tags": {"alertkey": res['labels']['alertkey'], "severity": res['labels']['severity']},
                                    "ruleUrl": res['panelURL'],
                                    "message": res['annotations']['grafana_state_reason'] }
                    results.append(result)
                
                if check_FM['state'] == "grf":
                    if 'description' in res['annotations']:
                        result = {  "title": res['labels']['alertname'], 
                                    "state": status,
                                    "ruleId": res['labels']['grafana_folder'], 
                                    "ruleName": data['receiver'],
                                    "evalMatches": [],
                                    "orgId": int(orgId),
                                    "dashboardId": dashId,
                                    "panelId": int(panelId),
                                    "tags": res['labels'],
                                    "ruleUrl": res['panelURL'],
                                    "message": res['annotations']['description'] }
                        results.append(result)
                    else:
                        result = {  "title": res['labels']['alertname'], 
                                    "state": status,
                                    "ruleId": res['labels']['grafana_folder'], 
                                    "ruleName": data['receiver'],
                                    "evalMatches": [],
                                    "orgId": int(orgId),
                                    "dashboardId": dashId,
                                    "panelId": int(panelId),
                                    "tags": res['labels'],
                                    "ruleUrl": res['panelURL'],
                                    "message":  "The description field is empty"}
                        results.append(result)
            else:
                state = {"status": "skip"}
            state = Sender.send_new_format(results, chat, thread)
            return(state)

    