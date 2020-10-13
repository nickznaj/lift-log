import json

from liftlog.sql_queries import FETCH_WORKOUT
from liftlog.error_wrapper import error_wrapper
from liftlog.sql_helpers import (
    do_sql,
    compile_workout,
)
from liftlog.query_converter import construct_where


@error_wrapper
def handler(event, context, config=None):
    query = event["body"]

    where = construct_where(query)
    sql = FETCH_WORKOUT.format(WHERE=where)

    rows = do_sql(sql)
    result = compile_workout(rows)

    return result
