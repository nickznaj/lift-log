FETCH_WORKOUT = """
            SELECT 
                workout.id,
                workout.workout_notes,
                workout.workout_coach_notes,
                workout.date,
                `set`.id as set_id,
                `set`.reps,
                `set`.weight,
                `set`.rpe,
                exercise.name as exercise,
                link.link
            FROM workout
                left join `set` on `workout`.`id` = `set`.`fk_set_workout`
                left join exercise on `set`.fk_set_exercise  = exercise.id
                left join link on `set`.fk_set_link = link.id
            {WHERE}
        """
        

FETCH_SETS = """
    SELECT 
        workout.date, 
        exercise.name, 
        `set`.reps, 
        `set`.weight,
        `set`.rpe
    FROM workout
        inner join `set` on workout.id = `set`.fk_set_workout
        inner join exercise on `set`.fk_set_exercise = exercise.id
    WHERE 
        exercise.name = "{name}"
"""


FETCH_EXERCISE = """
    SELECT *
    FROM `log_lift`.`exercise`
    WHERE exercise.name = "{name}";
"""


ADD_WORKOUT = """
    INSERT INTO `log_lift`.`workout`
    SET
        `date` = {date},
        `workout_notes` = {workout_notes}
    
    SELECT LAST_INSERT_ID() INTO @workout_id;
"""


ADD_EXERCISE = """
    INSERT INTO `log_lift`.`exercise`
    SET
        `name` = {name}
        `body_part` = {body_part}
    
    SELECT LAST_INSERT_ID() INTO @exercise_id;
"""


ADD_SET = """
    INSERT INTO `log_lift`.`set`
    SET
        `reps` = {reps},
        `weight` = {weight},
        `rpe` = {rpe},
        `fk_set_exercise` = {exercise_id},
        `fk_set_link` = @link_id,
        `fk_set_workout` = @workout_id,
        `set_coach_notes` = "{set_coach_notes}",
        `set_notes` = "{set_notes}";
"""


UPDATE_SET = """
    UPDATE `log_lift`.`set`
    SET
        `reps` = {reps},
        `weight` = {weight},
        `rpe` = {rpe},
        `fk_set_exercise` = {exercise_id},
        `fk_set_link` = {link_id},
        `fk_set_workout` = {workout_id},
        `set_coach_notes` = "{set_coach_notes}",
        `set_notes` = "{set_notes}" 
    WHERE `id` = {id};
"""


ADD_LINK = """
	INSERT INTO `log_lift`.`link`
    SET
	    `link` = "{link}"
	;
    SELECT LAST_INSERT_ID() INTO @link_id;
"""

