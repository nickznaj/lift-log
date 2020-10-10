import json

from liftlog.sql_helpers import fetch_workout_for_date


def handler(event, context, config=None): 
    # add_workout(test)
    date = event['pathParameters']['date']

    workout = fetch_workout_for_date(date)

    return {
        "statusCode": 200,
        "body": json.dumps(workout)
    }
