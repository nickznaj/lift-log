import json

from liftlog.sql_helpers import fetch_workout_for_date


def handler(event, context, config=None): 
    # add_workout(test)
    date = event['pathParameters']['date']

    workout = fetch_workout_for_date(date)

    if not workout:
        return {
            "statusCode": 404,
            "body": "Workouts for dates {} not found".format(date)
        }

    return {
        "statusCode": 200,
        "body": json.dumps(workout)
    }
