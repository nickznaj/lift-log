import json
from liftlog import pymysql
from liftlog.sql_helpers import update_set, fetch_exercise
from liftlog.error_wrapper import error_wrapper
    
# modifies an existing set that belongs to a workout
@error_wrapper
def handler(event, context, config=None): 
    sset = event['body']
    workout_id = event['pathParameters']['workout_id']
    set_id = event['pathParameters']['set_id']
    exercise_id = fetch_exercise(sset['exercise'])['id']

    sset['id'] = set_id
    sset['workout_id'] = workout_id
    sset['exercise_id'] = exercise_id

    sql = update_set(sset, return_sql=False)

    return sql