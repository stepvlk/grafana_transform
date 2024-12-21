

from flask_caching import Cache 
cache = Cache() 
#cache.init_app(app, config={'CACHE_TYPE': 'simple'}) 

def cacher(query, state):
    
    if state == "no_data":
        cache.set(str(query['ruleId']), query['state'], timeout=1200)
    
    if state == "ok":
        status = cache.get(str(query['ruleId']))
        if status is None:
            return "send"
        else:
            cache.delete(str(query['ruleId']))
            return "pass"
    
    if state == "alerting":
        status = cache.get(str(query['ruleId']))
        if status is None:
            return "send"
        else:
            cache.delete(str(query['ruleId']))
            return "pass" 
 


@app.route('/alerting/check_cache', methods=['GET'])
def cache_check():
    data = []
    for k in cache.cache._cache:
        data.append({k:cache.get(k)})
    return jsonify({"data": data, "z_count": len(data)}), 200


@app.route('/alerting/sync/<task>', methods=['GET'])
def cache_sync(task):
    if task == "delete":
        cache.delete(str(request.args['id']))
    if task == "create":
        cache.set(str(request.args['id']), request.args['state'], timeout=1200)
    return jsonify({"status": "cache_recreate"}), 200 