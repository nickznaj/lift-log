import json
from liftlog import pymysql
from liftlog import sql_helpers
from liftlog import sql_queries
    

def handler(event, context, config=None): 
    # add_workout(test)
    sset = event['body']
    workout_id = event['pathParameters']['workout_id']
    set_id = event['pathParameters']['set_id']

    sset['set_id'] = set_id
    sset['workout_id'] = workout_id

    update_set(sset)

    return {
        "statusCode": 200
    }