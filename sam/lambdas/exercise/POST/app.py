import json
import sys
from liftlog.pymysql.err import IntegrityError
from liftlog.sql_helpers import add_exercise

def handler(event, context, config=None): 
    exercise = json.loads(event['body'])

    try:
        add_exercise(exercise)
    except IntegrityError as e:
        print(e.args)
        return {
            "statusCode": 422,
            "body": json.dumps(e.args[1])
        }

    return {
        "statusCode": 200
    }