import json
from liftlog.sql_queries import ADD_WORKOUT
from liftlog.error_wrapper import error_wrapper
from liftlog.sql_helpers import fetch_exercise, add_link, add_set, write_sql

# creates one large SQL transaction for adding a workout, its sets, and the sets'
# links
@error_wrapper
def handler(event, context, config=None): 
    workout = json.loads(event['body'])

    sql = ADD_WORKOUT.format(
        date = workout['date'], 
        workout_notes = workout.get('workout_notes', None)
    )
    
    # start a transaction to ensure something gets written only if
    # each step succeeds
    sql = "START TRANSACTION;\n" + sql
    
    # form each set with the needed foreign keys
    for idx, sset in enumerate(workout['sets']):
        exercise_id = fetch_exercise(sset['exercise'])['id']
        sset['exercise_id'] = exercise_id
        
        link_id = "NULL"
        if sset.get('link', False):
            link_id = "@link_id" + str(idx)
            link_sql = add_link(sset.get('link', None), return_sql = True)
            link_sql = link_sql.replace('@link_id', link_id)
            sql += link_sql + "\n"
        
        
        set_sql = add_set(sset, return_sql=True)
        set_sql = set_sql.replace('@link_id', link_id)
        sql += set_sql + "\n" 
    
    sql += "\nCOMMIT;"
        
    write_sql(sql)



    return {
        "statusCode": 200
    }