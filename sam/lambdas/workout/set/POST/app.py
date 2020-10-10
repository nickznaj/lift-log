import json
from liftlog import pymysql
from liftlog import sql_helpers
from liftlog import sql_queries
    
# adds a new set to an existing workout
def handler(event, context, config=None): 
    # add_workout(test)
    sset = event['body']
    workout_id = event['pathParameters']['workout_id']
    exercise_id = fetch_exercise(sset['exercise'])['id']

    sset['exercise_id'] = exercise_id
    sset['workout_id'] = workout_id

    if sset['link']:
        link_id = add_link(sset['link'])
        sset['link_id'] = link_id

    add_set(sset)

    return {
        "statusCode": 200
    }