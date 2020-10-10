import json
import sys
from liftlog import pymysql
from liftlog import sql_helpers
from liftlog import sql_queries

sys.path.append('/opt')

def handler(event, context, config=None): 
    # add_workout(test)
    workout = event['body']

    sql = ADD_WORKOUT.format(
        date = workout['date'], 
        workout_notes = workout.get('workout_notes', None)
    )
    
    sql = "START TRANSACTION;\n" + sql
    
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
    
    # sql = "COMMIT;"
    
    write_sql(sql)


    return {
        "statusCode": 200
    }