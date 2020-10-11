from liftlog.pymysql.err import IntegrityError
from liftlog.cors import access_control_headers
from functools import wraps
import traceback

errors = (
    IntegrityError, 
    KeyError
)

def error_wrapper(fn):
    @wraps(fn)
    def wrapped(event, context):
        try:
            return fn(event, context)
        except errors as e:
            print('ERROR: ', repr(e))
            traceback.print_exc(limit=5)
            return {
                "statusCode": 422,
                "body": repr(e)
            }
    return wrapped