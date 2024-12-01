from config.config import config
import re

def get_account(url):
    print(url)
    org = re.search('orgId.*?(\d+)', url).group(1)
    print(org)
    
    headerses = {"1" : {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Cache-Control": "no-cache, no-store, must-revalidate",
                        "Authorization": config['grafana_keys']['orgid_1']
                       },
                "2" : {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Cache-Control": "no-cache, no-store, must-revalidate",
                        "Authorization": config['grafana_keys']['orgid_2']
                       },
                "3" : {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Cache-Control": "no-cache, no-store, must-revalidate",
                        "Authorization": config['grafana_keys']['orgid_3']
                       },
                "4" : {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Cache-Control": "no-cache, no-store, must-revalidate",
                        "Authorization": config['grafana_keys']['orgid_4']
                       }}
    
    for k,v in headerses.items():
        if str(k) == str(org):
            print(v)
            return v
