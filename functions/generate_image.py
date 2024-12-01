import base64 

from jinja2 import Environment, PackageLoader, FileSystemLoader

from io import BytesIO
from PIL import Image
import requests

import datetime

from functions.get_account import get_account
from config.config import config

env = Environment(loader=FileSystemLoader('/data'))
template  = ('templates/alerts.html') 
def generates_templates(query, way, name):
    metrics = ""
    values = ""
    with open(way, "rb") as image:
        b64string = base64.b64encode(image.read()).decode("utf-8")

    for metric in query['evalMatches']:
        metrics += f"{metric['metric']}\n" 
        values  += f"{metric['value']}\n"
    if query['state'] == "ok":
        color = "#00ac46"
    if query['state'] == "alerting":
        color = "#8B0000"
    link = query['ruleUrl'].split('/d/')[0]
    if 'message' in query:
        message =  query['message']
    else:
        message = ""
    data = {"title": query['title'],
    "error": message, 
    "state":query['state'], 
    "values": values[:-1], 
    "metrics": metrics[:-1],
    "evali": query['evalMatches'],
    "color": color,
    "ruleUrl": query['ruleUrl'],
    "source": link,
    "link": "",
    "image": b64string,
    "embed": way,
    "image_name": name
    }
    rendered_template = template.render(data)
    return rendered_template


def generate_image(query):
        ts = int(datetime.datetime.now().timestamp())
        name = f"{query['ruleId']}_{ts}.png"
        file_way = f'/data/{name}'
        headers = get_account(query['ruleUrl'])
        url_render = f"{config['grafana']['url'].replace('http://', '').replace('https://', '')}/render/"
        find_url = f"{config['grafana']['url'].replace('http://', '').replace('https://', '')}"
        img_url = query['ruleUrl'].replace(find_url, url_render).replace("/d/", "d-solo/").replace("&viewPanel", "&panelId").replace("&orgId=1", "&height=800&width=1200")
        img = requests.get(img_url, headers=headers)
        img_code = img.content
        img_encode = Image.open(BytesIO(img_code))
        img_encode.save(file_way)
        return {"file":  file_way, "name": name}
    
def generate_image_raw(query):
    import re
    print(query)
    ts = int(datetime.datetime.now().timestamp())
    dash = re.findall(r'(d)/(.*)\?', query['ruleUrl'])[0][1]
    name = f"{dash}_{ts}.png"
    file_way = f'tmp/{name}'
    headers = get_account(query['ruleUrl'])
    find_url = f"{config['grafana']['url'].replace('http://', '').replace('https://', '')}"
    url_render = f"{config['grafana']['url'].replace('http://', '').replace('https://', '')}/render/"
    img_url = query['ruleUrl'].replace(find_url, url_render).replace("/d/", "d-solo/").replace("&viewPanel", "&panelId").replace("&orgId=1", "&height=800&width=1200")
    img = requests.get(img_url, headers=headers)
    print(img)
    img_code = img.content
    img_encode = Image.open(BytesIO(img_code))
    print(img_encode)
    img_encode.save(file_way)
    return {"file":  file_way, "name": name}