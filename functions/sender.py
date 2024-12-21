from flask import Flask, jsonify, abort, request, make_response
import logging
import datetime
import time
import requests
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config.config import config
from functions.base_state import Base

from smtplib import SMTP

from functions.generate_image import generates_templates
from functions.generate_image import generate_image, generate_image_raw
logger = logging.getLogger('werkzeug')
logging.basicConfig(level=logging.INFO)
handler = logging.FileHandler('logs/notifications.log')
logger.addHandler(handler)

def get_grf_panel_info(query):
    print(query)
    return query

class Sender():
    def send_message_webhook(query, channel):
        try:
            query.pop('_id')
            start_time = time.time()
            ts = int(datetime.datetime.now().timestamp())
            dt = datetime.datetime.utcnow().strftime("%d %B %Y %I:%M%p")
            url = f"{config['point']['url']}/api/tamtam/grafana/webhook_bss?chat={channel}&double=15"
            resp = requests.post(url, data=json.dumps(query), verify=False).status_code
            if resp != 200:
                Base.repeat_webhook_save(query)
            logger.info({"timestamp": ts, "rule": "SENDING", "url":query['ruleUrl'], "state": query['state'], "sending": "send", "ElenaTree_satus": resp, "date": dt, "duration": time.time() - start_time, "channel": channel})
            print({"timestamp": ts, "rule": "SENDING", "url":query['ruleUrl'], "state": query['state'], "sending": "send", "ElenaTree_satus": resp, "date": dt, "duration": time.time() - start_time, "channel": channel})
            return jsonify({"status": "rule_finish"}), 200
        except:
            return jsonify({"status": "rule error"}), 429
    
    def send_new_format(query, channel, thread):
        # coding: utf-8
        start_time = time.time()
        ts = int(datetime.datetime.now().timestamp())
        import pytz
        dt = datetime.datetime.now(pytz.utc)
        dt = dt.astimezone(pytz.timezone('Europe/Moscow'))
        dt = str(dt).split('.')[0]
        if thread is None:
            if int(config['params']['image_generate_backend']) != 0:
                for res in query:
                    image = generate_image_raw(res)
                    files = {'photo': open(image['file'], 'rb')}
                    if res['state'] == "ok":
                        text = f"Description: {res['message']}\nRuleUrl: <a href='{res['ruleUrl']}'>go panel url</a>\n\nAlertTime: {dt}"
                        code = "<b>\U00002705 \nAlertname: " + res['title'] + "\n\n" + text  + "</b>"  
                    if res['state'] == "alerting":
                        string = ""
                        for dd in res['evalMatches']:
                            dd.pop("tag")
                            for k,v in dd.items():
                                string += f"mertic: {k} value: {v}\n"
                        text = f"Description: {res['message']}\nRuleUrl: <a href='{res['ruleUrl']}'>go panel url</a>\nMetrics:\n{string[:-1]}\n\nAlertTime: {dt}"
                        
                        code = "<b>\U00002757 \nAlertname: " + res['title'] + "\n\n" + text +"</b>"
                        print(code)    
                    result = requests.post(url='https://api.telegram.org/bot{0}/{1}'.format(str(config['notification']['token']), 'sendPhoto'), data={'chat_id': str(config['notification']['channel']), 'caption': code, "parse_mode": 'HTML'}, files=files).json #"parse_mode": 'Markdown'
                    print(result)       
                    return {"massage_send_status": result}    
        else:
            pass
        return {"massage_send_status": result}
        
    def send_message_mail(query, channel):
        msg = MIMEMultipart()
        image = generate_image(query)
        text = generates_templates(query, image['file'], image['name'])
        chann = channel.split(',')
        try:
            query.pop('_id')
            start_time = time.time()
            ts = int(datetime.datetime.now().timestamp())
            dt = datetime.datetime.utcnow().strftime("%d %B %Y %I:%M%p")
            task = {'from_user': config['mail']['from_user'],
                    'to_user':  ', '.join(chann),
                    'massage':  text,
                    'subject':  query['ruleName'],
                    'type':  "html"}
            msg.attach(MIMEText( text, 'html'))   
            msg['To'] = ', '.join(chann)
            msg['From'] = config['mail']['from_user']
            msg["Subject"] =  query['title']
            to_user =  ', '.join(chann)
            part = MIMEBase('application', "octet-stream")
            files = image['file']
            with open(files, 'rb') as file:
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % image['name'])
                msg.attach(part)
            server = SMTP(config['mail']['host'], int(config['mail']['port']))
            if int(config['mail']['auth']) != 0:
                server.login(config['mail']['user'], config['mail']['password'])
            server.set_debuglevel(1)
            server.sendmail(task['from_user'], to_user, msg.as_string())
            server.quit()
            logger.info({"timestamp": ts, "rule": "SENDING", "url":query['ruleUrl'], "state": query['state'], "sending": "send", "mail_satus": "send", "date": dt, "duration": time.time() - start_time, "channel": channel})
            print({"timestamp": ts, "rule": "SENDING", "url":query['ruleUrl'], "state": query['state'], "sending": "send", "mail_satus": "send", "date": dt, "duration": time.time() - start_time, "channel": channel})
            return jsonify({"status": "rule_finish"}), 200
        
        except:
            return jsonify({"status": "rule error"}), 429
        
    def send_new_format_prod(query, channel, thread):
        # coding: utf-8
        start_time = time.time()
        ts = int(datetime.datetime.now().timestamp())
        import pytz
        dt = datetime.datetime.now(pytz.utc)
        dt = dt.astimezone(pytz.timezone('Europe/Moscow'))
        dt = str(dt).split('.')[0]
        if thread is None:
            if int(config['params']['image_generate_backend']) != 0:
                for res in query:
                    image = generate_image_raw(res)
                    if config['notification']['type'] == "Telegram":
                        files = {'photo': open(image['file'], 'rb')}
                        if res['state'] == "ok":
                            text = f"Description: {res['message']}\nRuleUrl: <a href='{res['ruleUrl']}'>go panel url</a>\n\nAlertTime: {dt}"
                            code = "<b>\U00002705 Alertname: " + res['title'] + "\n\n" + text  + "</b>"  
                        if res['state'] == "alerting":
                            string = ""
                            for dd in res['evalMatches']:
                                try:
                                    dd.pop("tag")
                                except:
                                    dd = dd
                                for k,v in dd.items():
                                    string += f"mertic: {k} value: {v}\n"
                            text = f"Description: {res['message']}\nRuleUrl: <a href='{res['ruleUrl']}'>go panel url</a>\nMetrics:\n{string[:-1]}\n\nAlertTime: {dt}"
                            
                        code = "<b>\U00002757 Alertname: " + res['title'] + "\n\n" + text +"</b>"
                        result = requests.post(url='https://api.telegram.org/bot{0}/{1}'.format(str(config['notification']['token']), 'sendPhoto'), data={'chat_id': str(config['notification']['channel']), 'caption': code, "parse_mode": 'HTML'}, files=files).json #"parse_mode": 'Markdown'
                    
                    if config['notification']['type'] == "Elena":
                        files = {'photo': open(image['file'], 'rb')}
                        if res['state'] == "ok":
                            text = f"Description: {res['message']}\nRuleUrl: {res['ruleUrl']}\n\nAlertTime: {dt}"
                            code = "\U00002705 Alertname: " + res['title'] + "\n\n" + text 
                        if res['state'] == "alerting":
                            # string = ""
                            # for dd in res['evalMatches']:
                                # try:
                                    # dd.pop("tag")
                                # except:
                                    # dd = dd
                                # for k,v in dd.items():
                                    # string += f"{k} : {v}\n"
                            #ss = f"<details><summary>Metrics</summary>{string[:-1]}</details>"
                            #doc = f"*html*<pre>{text}</pre>"
                            text = f"Description: {res['message']}\nRuleUrl: {res['ruleUrl']}\n\nAlertTime: {dt}" #Metrics:\n{string[:-1]}
                            
                        #texts = f"Description: {res['message']}\nRuleUrl: {res['ruleUrl']}\nMetrics:\n{ss}\n\nAlertTime: {dt}"
                            code = "\U00002757 Alertname: " + res['title'] + "\n\n" + text 
                        #text = f"*html*<pre>{code}</pre>"
                        data = {"text": code, "chat": channel, "double": "1", "user": "1", "channel": "ElenaTree"}
                        result=requests.post(config['point']['url'],files=files,data=data, verify=False).status_code
                return {"massage_send_status": "send"}
   
        else:
            pass
        return {"massage_send_status": result} 