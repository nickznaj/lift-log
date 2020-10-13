import json
from liftlog.sql_queries import UPDATE_WORKOUT
from liftlog.error_wrapper import error_wrapper
from liftlog.sql_helpers import write_sql, replace_null_sql_values

# updates the values for a single row in the workout table
@error_wrapper
def handler(event, context, config=None):
    workout = event["body"]
    workout_id = event["pathParameters"]["workout_id"]
    workout["id"] = workout_id

    sql = replace_null_sql_values(UPDATE_WORKOUT, workout)

    workout_id = write_sql(sql, workout)
    return workout_id