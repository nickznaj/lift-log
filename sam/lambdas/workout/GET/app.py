import json

from liftlog import sql_helpers


def handler(event, context, config=None): 
    # add_workout(test)
    date = event['pathParameters']['date']

    workout = fetch_workout_for_date(date)

    

    return {
        "statusCode": 200,
        "body": json.dumps(workout)
    }
