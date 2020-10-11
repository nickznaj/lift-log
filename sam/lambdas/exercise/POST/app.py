import json
import sys
from liftlog.sql_helpers import add_exercise
from liftlog.error_wrapper import error_wrapper

@error_wrapper
def handler(event, context, config=None): 
    exercise = event['body']
    exercise_id = add_exercise(exercise)

    return exercise_id