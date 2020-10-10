import json

from liftlog.sql_helpers import fetch_workout_for_date


def handler(event, context, config=None): 
    # add_workout(test)
    query = json.loads(event['body'])
    print(query)

    if query.get('date', False):
        date = query.get('date')
        result = fetch_workout_for_date(date)

    if not result:
        return {
            "statusCode": 404,
            "body": "No workout(s) mathching query {}".format(event['body'])
        }

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }
