import os
import sys
import json
import logging
import datetime
from liftlog import pymysql
from liftlog.pymysql.constants import CLIENT
from liftlog.custom_encoder import CustomEncoder
from .templates import set_template, workout_template
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


def write_sql(sql):
    print(sql)
    with conn.cursor() as cur:
        cur.execute(sql)
    res = conn.commit()
    return cur.lastrowid


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
def add_set(sset, return_sql=False):
    sql = ADD_SET.format(
        reps= sset.get("reps"),
	    weight= sset.get("weight"),
	    rpe= sset.get("rpe", None),
	    exercise_id= sset.get("exercise_id"),
	   # link_id= sset.get("link_id", None),
	   # workout_id= sset.get("workout_id"),
	    coach_notes = sset.get("set_coach_notes", None),
	    set_notes= sset.get("set_notes", None)
    )

    # if adding a single set
    if sset.get('link_id'):
        sql = "SET @link_id = {};\n".format(sset.get('link_id'))
    if sset.get('workout_id'):
        sql = "SET @workout_id = {};\n".format(sset.get('workout_id'))
    
    
    if return_sql:
        return sql
    
    set_id = write_sql(sql)
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

# put together a sql transaction to write the whole workout to DB.
# start with the workout entry, then any dependent child rows.
def add_workout(workout):
    sql = ADD_WORKOUT.format(
        date = workout['date'], 
        workout_notes = workout.get('workout_notes', None)
    )
    
    sql = "START TRANSACTION;\n" + sql
    
    # workout_id = write_sql(sql)
    
    # add each set to the db with needed foreign keys
    for idx, sset in enumerate(workout['sets']):
        exercise_id = fetch_exercise(sset['exercise'])['id']
        sset['exercise_id'] = exercise_id
        
        link_id = None
        if sset.get('link'):
            link_id = "@link_id" + str(idx)
            link_sql = add_link(sset.get('link', None), return_sql = True)
            link_sql = link_sql.replace('@link_id', link_id)
            sql += link_sql + "\n"
        
        set_sql = add_set(sset, return_sql=True)
        set_sql = set_sql.replace('@link_id', link_id)
        sql += set_sql + "\n" 
    
    sql += "\nCOMMIT;"
    write_sql(sql)


def add_link(link_url, return_sql=False):
    if not link_url:
        return None
    
    sql = ADD_LINK.format(
        link = link_url    
    )
    
    if return_sql:
        return sql
    
    link_id = write_sql(sql)
    
    print(link_id)
    return link_id
    

def add_exercise(exercise):
    sql = ADD_EXERCISE.format(
        name = exercise.get('name'),
        body_part = exercise.get('body_part')
    )
    
    exercise_id = write_sql(sql)
    return exercise_id
    

# TODO:
# add an add exercise function
# somehow create an update function

