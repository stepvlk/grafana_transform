import os

config = {
        "server": {
        "adress": os.getenv('SERVER_HOST', "0.0.0.0"),
        "port": os.getenv('SERVER_PORT', 6845),
        "debug": os.getenv('SERVER_LOGLEVEL', True),
        },
        "db": {
            "url": os.getenv('DB_URL', "127.0.0.1:27017"),
            "user": os.getenv('DB_USER', "alerting"),
            "pass": os.getenv('DB_PASS', "alerting"),
        },
        "grafana": {
            "url": os.getenv('GRAFANA_URL', "http://127.0.0.1:3000"),
            "repeat": os.getenv('GRAFANA_REPEAT', 0),
        },
        "grafana_keys": {
            "orgid_1":  os.getenv('ORG1', "ORG1"), 
            "orgid_2": os.getenv('ORG2', "ORG2"),
            "orgid_3": os.getenv('ORG3', "ORG3"),
            "orgid_4": os.getenv('ORG4', "ORG5"),
        },
        "point": {
            "url": os.getenv('POINT_URL', "https://api.telegram.org/bot"),
        },
        "silent_ruleid": [],
        "mail": {
            "from_user": os.getenv('MAIL_FROM_USER', "grafana@domain.com"), 
            "host": os.getenv('MAIL_HOST', "<mail_host>"), 
            "port": os.getenv('MAIL_PORT', 25),
            "auth": os.getenv('MAIL_AUTH', 0),
            "user": os.getenv('MAIL_USER', "admin"),
            "password": os.getenv('MAIL_PASSWORD', "pass"),
        },
        "params": {
            "image_generate_backend": os.getenv('PARAMS_IMAGE', 1),
        },
        "notification": {
            "type": os.getenv('NOTIFICATION_TYPE', "Telegram"),
            "channel": os.getenv('NOTIFICATION_CHANNEL', "-4530347279"),
            "url": os.getenv('NOTIFICATION_URL', "https://api.telegram.org/bot"),
            "token": os.getenv('NOTIFICATION_TOKEN', "<>")
        }
}
