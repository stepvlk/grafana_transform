#imports
from config.config import config
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
#routes
from routes.webhook import webhook
from routes.mail import mail
from routes.system import system

#flask extentions
app = Flask(__name__, template_folder='templates')
app.register_blueprint(webhook)
app.register_blueprint(mail)
app.register_blueprint(system)

#metrics
metrics = PrometheusMetrics(app)

#initialization
if __name__ == "__main__":
    app.run(host=config['server']['adress'], port=config['server']['port'], debug=config['server']['debug'])