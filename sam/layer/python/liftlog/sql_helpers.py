import os
import re
import sys
import json
import logging
import datetime
from liftlog import pymysql
from liftlog.pymysql.constants import CLIENT
from liftlog.custom_encoder import CustomEncoder
from .templates import set_template, workout_template, set_insert_keys
from .sql_queries import *
logger = logging.getLogger()
logger.setLevel(logging.INFO)

conn = None
DB_HOST = "lift-log.crmfoj89n8bb.us-east-1.rds.amazonaws.com"
DB_USER = os.environ['LIFTLOG_DB_USER']
DB_PASSWORD = os.environ['LIFTLOG_DB_PW']
DB_NAME = "log_lift"

# connect to mysql DB
if not conn:
    try:
        conn = pymysql.connect(
            DB_HOST, 
            user=DB_USER,
            passwd=DB_PASSWORD, 
            db=DB_NAME, 
            connect_timeout=5, 
            cursorclass=pymysql.cursors.DictCursor,
            client_flag=CLIENT.MULTI_STATEMENTS
        )
        print('connected to RDS')
    except pymysql.MySQLError as e:
        print(
            "ERROR: Unexpected error: Could not connect to MySQL instance.")
        print(e)
        sys.exit()


def do_sql(query):
    result = []
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            logger.info(row)
            result.append(row)
    return sanitize_rows(result)


def write_sql(sql, body=None):
    print(sql)
    with conn.cursor() as cur:
        if body:
            print('writing with body')
            sql = sql.format(**body)
            cur.execute(sql)
        else:
            cur.execute(sql)
    res = conn.commit()
    return cur.lastrowid

# take something about to be written to the db and based on its template,
# replace all necessary values in the sql query with its corresponding value, 
# or NULL if missing an optional field
def replace_null_sql_values(sql, obj):
    required_keys = re.findall(r"(\"?\{([A-Za-z_]+)\}\"?)", sql)
    for match, set_key in required_keys:
        if not obj.get(set_key, False):
            sql = sql.replace(match, "NULL" )

    return sql

# convert datetimes and Decimals into serializable values
def sanitize_rows(rows):
    return json.loads(
        json.dumps(
            rows, cls=CustomEncoder
            )
        )


# remove None values from SQL rows
def remove_nones(row):
    return {
        k:v for (k,v) in row.items() if v
    }


# take in sql rows and compile into frontend friendly payload
def compile_workout(rows):
    result = {}
    for row in rows:
        row = remove_nones(row)
        curr_date = row['date']
        
        # initialize workout entry for date
        if not result.get(curr_date, False):
            workout = {'sets': []}
            for k in workout_template.keys():
                if row.get(k, False):
                    workout[k] = row[k]
            result[curr_date] = workout

        workout = result[curr_date] 
    
        # all remaining keys belong in the frontend set representation
        # get non-null values from row
        sset = {}
        for k in set_template.keys():
            if row.get(k, False):
                sset[k] = row[k]

        # if sset empty, then workout has no associated sets.
        if len(sset.keys()) > 0:
            workout['sets'].append(sset)
    
    return result
    

def fetch_workout_for_date(date):
    sql = FETCH_WORKOUT.replace("{WHERE}", 'where workout.date = "{}"').format(date)
    rows = do_sql(sql)

    return compile_workout(rows).get(date, None)
    

def fetch_workouts_for_date_range(start, end):
    sql = FETCH_WORKOUT.replace("{WHERE}", 
        'where workout.date >= "{}" and workout.date <= "{}"').format(
            start, end)
    
    query_result = do_sql(sql)
    
    print(
        json.dumps(compile_workout(query_result), indent=2)
    )
    # json.loads(CustomEncoder().encode(test))
    

def fetch_all_sets_for_exercise(exercise):
    sql = FETCH_SETS.replace("{NAME}", exercise)
    query_result = do_sql(sql)
    
    print(query_result)
    
    
def fetch_exercise(name="Barbell Squat"):
    sql = FETCH_EXERCISE.format(NAME = name)
    
    return do_sql(sql)[0]
    

# def add_set(workout_id, link_id):
def add_set(sset, adding_one=False, return_sql=False):
    sql = replace_null_sql_values(ADD_SET, sset)

    # if adding a single set
    if adding_one:
        if sset.get('link_id'):
            sql = "SET @link_id = {};\n".format(sset.get('link_id')) + sql
        else:
            sql= sql.replace('@link_id', "NULL")
        if sset.get('workout_id'):
            sql= sql.replace('@workout_id', "{workout_id}")
        
    if return_sql:
        return sql
    
    set_id = write_sql(sql, sset)
    return set_id


def update_set(sset):
    sql = UPDATE_SET.format(
        reps= sset.get("reps"),
	    weight= sset.get("weight"),
	    rpe= sset.get("rpe", None),
	    exercise_id= sset.get("exercise_id"),
	    link_id= sset.get("link_id", None),
	    workout_id= sset.get("workout_id"),
	    coach_notes = sset.get("set_coach_notes", None),
	    set_notes= sset.get("set_notes", None),
	    id= sset.get("id", None)
    )

    set_id = write_sql(sql)
    return set_id


def add_link(link_url, return_sql=False):
    if not link_url:
        return None

    link = {"link": link_url}
    sql = replace_null_sql_values(ADD_LINK, link)
    
    if return_sql:
        return sql
    
    link_id = write_sql(sql, link)
    
    return link_id
    

def add_exercise(exercise):
    sql = replace_null_sql_values(ADD_EXERCISE, exercise)

    exercise_id = write_sql(sql, exercise)
    
    return exercise_id
    

# TODO:


