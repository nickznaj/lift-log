import json
from liftlog import pymysql
from liftlog.sql_helpers import add_link, add_set, fetch_exercise
from liftlog.error_wrapper import error_wrapper

# adds a new set to an existing workout
@error_wrapper
def handler(event, context, config=None):
    sset = event["body"]
    workout_id = event["pathParameters"]["workout_id"]
    exercise_id = fetch_exercise(sset["exercise"])["id"]

    sset["exercise_id"] = exercise_id
    sset["workout_id"] = workout_id

    if sset.get("link", False):
        link_id = add_link(sset["link"])
        sset["link_id"] = link_id

    result = add_set(sset, adding_one=True, return_sql=False)
    return result