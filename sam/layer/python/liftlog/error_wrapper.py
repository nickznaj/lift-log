from liftlog.pymysql.err import IntegrityError, ProgrammingError
from liftlog.cors import access_control_headers
from functools import wraps
import traceback
import json

errors = (IntegrityError, KeyError, ProgrammingError)

# turns any body from a string to a dict
# runs the lambda, returning a 200 response with headers on success
# catches errors and returns an appropriate response
def error_wrapper(fn):
    @wraps(fn)
    def wrapped(event, context):
        body = event.get("body", None)
        try:
            if isinstance(body, str):
                event["body"] = json.loads(body)
            response = fn(event, context)
            return {
                "statusCode": 200,
                "body": json.dumps(response),
                "headers": access_control_headers(),
            }
        except errors as e:
            print("ERROR: ", repr(e))
            traceback.print_exc(limit=5)
            return {
                "statusCode": 422,
                "body": repr(e),
                "headers": access_control_headers(),
            }

    return wrapped