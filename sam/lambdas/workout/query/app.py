import json

from liftlog.sql_helpers import fetch_workout_for_date, fetch_workouts_for_date_range
from liftlog.error_wrapper import error_wrapper


@error_wrapper
def handler(event, context, config=None): 
    query = event['body']

    if 'date' in query:
        date = query.get('date')
        result = fetch_workout_for_date(date)
    elif set(['start', 'end']).issubset(query.keys()):
        start = query.get('start')
        end = query.get('end')
        result = fetch_workouts_for_date_range(start, end)

        

# TODO: remove this by implementing custom error class
    if not result:
        return {
            "statusCode": 404,
            "body": "No workout(s) mathching query {}".format(event['body'])
        }

    return result
