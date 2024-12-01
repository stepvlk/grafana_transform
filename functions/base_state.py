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

client_alert_mail = MongoClient(base)
db_alert_mail = client_alert_mail['alerting']
collection_alert_mail = db_alert_mail.grafana_alerting_mail


client_status_mail = MongoClient(base)
db_status_mail = client_status_mail['alerting']
collection_status_mail = db_status_mail.grafana_statuses_mail

client_repeat = MongoClient(base)
db_repeat = client_repeat['alerting']
collection_repeat = db_alert.grafana_repeat

client_repeat_mail = MongoClient(base)
db_repeat_mail = client_repeat_mail['alerting']
collection_repeat_mail = db_repeat_mail.grafana_repeat_mail

class Base():

    def skip_rule(rule_id):
        if rule_id in config['silent_ruleid']:
            return {"state": "skip"}
        else:
            return {"state": "send"}


    def checker_webhook(query, state):
        state = Base.skip_rule(str(query['ruleId']))
        if state['state'] != "skip":
            ts = int(datetime.datetime.now().timestamp())        
            if state == "no_data":
                collection_status.insert_one({"ruleId": str(query['ruleId']), "state": query['state'], "timestamp": ts})       
            if state == "ok":
                status = collection_status.find_one({"ruleId" : str(query['ruleId'])})
                if status is None:
                    return "send"
                else:
                    collection_status.delete_one({"ruleId": str(query['ruleId'])})
                    return "pass"    
            if state == "alerting":
                status = collection_status.find_one({"ruleId" : str(query['ruleId'])})
                if status is None:
                    return "send"
                else:
                    collection_status.delete_one({"ruleId": str(query['ruleId'])})
                    return "pass"
            
    def checker_mail(query, state):
        state = Base.skip_rule(str(query['ruleId']))
        if state['state'] != "skip":
            ts = int(datetime.datetime.now().timestamp())
            
            if state == "no_data":
                collection_status_mail.insert_one({"ruleId": str(query['ruleId']), "state": query['state'], "timestamp": ts})
            
            if state == "ok":
                status = collection_status_mail.find_one({"ruleId" : str(query['ruleId'])})
                if status is None:
                    return "send"
                else:
                    collection_status_mail.delete_one({"ruleId": str(query['ruleId'])})
                    return "pass"
            
            if state == "alerting":
                status = collection_status_mail.find_one({"ruleId" : str(query['ruleId'])})
                if status is None:
                    return "send"
                else:
                    collection_status_mail.delete_one({"ruleId": str(query['ruleId'])})
                    return "pass"
    
    def repeat_webhook_save(query):
        collection_repeat.insert_one(query)

    def repeat_mail_save(query):
        collection_repeat_mail.insert_one(query)