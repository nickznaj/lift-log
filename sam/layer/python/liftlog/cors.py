def access_control_headers():
    headers = {
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date"
        + ",Authorization,X-Api-Key,x-requested-with",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST,GET,PUT,OPTIONS",
    }
    return headers