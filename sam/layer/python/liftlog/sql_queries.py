FETCH_WORKOUT = """
            select 
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
            from workout
                left join `set` on `workout`.`id` = `set`.`fk_set_workout`
                left join exercise on `set`.fk_set_exercise  = exercise.id
                left join link on `set`.fk_set_link = link.id
            {WHERE}
        """
        
FETCH_SETS = """
    select 
        workout.date, 
        exercise.name, 
        `set`.reps, 
        `set`.weight,
        `set`.rpe
    from workout
        inner join `set` on workout.id = `set`.fk_set_workout
        inner join exercise on `set`.fk_set_exercise = exercise.id
    where 
        exercise.name = "{NAME}"
"""

FETCH_EXERCISE = """
    SELECT *
    FROM `log_lift`.`exercise`
    WHERE exercise.name = "{NAME}";
"""

ADD_WORKOUT = """
    INSERT INTO `log_lift`.`workout`
        (`date`, `workout_notes`)
        VALUES ("{date}", "{workout_notes}");
    
    SELECT LAST_INSERT_ID() INTO @workout_id;
"""


ADD_EXERCISE = """
    INSERT INTO `log_lift`.`exercise`
        (`name`, `body_part`)
        VALUES ("{name}", "{body_part}");
    
    SELECT LAST_INSERT_ID() INTO @workout_id;
"""
    

ADD_SET = """
	INSERT INTO `log_lift`.`set`
	    (`reps`,
	    `weight`,
	    `rpe`,
	    `fk_set_exercise`,
	    `fk_set_link`,
	    `fk_set_workout`,
	    `set_coach_notes`,
	    `set_notes`)
	VALUES(
	    {reps},
	    {weight},
	    {rpe},
	    {exercise_id},
	    @link_id,
	    @workout_id,
	    "{coach_notes}",
	    "{set_notes}");
"""

UPDATE_SET = """
    UPDATE `log_lift`.`set`
    SET
    `reps` = {reps} 
    `weight` = {weight} 
    `rpe` = {rpe} 
    `fk_set_exercise` = {exercise_id} 
    `fk_set_link` = {link_id} 
    `fk_set_workout` = {workout_id} 
    `set_coach_notes` = {coach_notes} 
    `set_notes` = {set_notes} 
    WHERE `id` = {id};
"""


ADD_LINK = """
	INSERT INTO `log_lift`.`link`
	(`link`)
	VALUES
	("{link}");
	
    SELECT LAST_INSERT_ID() INTO @link_id;
"""




# INSERT INTO `log_lift`.`workout`
# (`date`, `workout_notes`)
# VALUES ('2019-10-01', 'super duper');

# -- store workout id

# -- for set in sets: 
#     -- look up exercise id based on name
# 	INSERT INTO `log_lift`.`link`
# 	(`link`)
# 	VALUES
# 	("supa dupah link");
#     -- store link id

# 	INSERT INTO `log_lift`.`set`
# 	(`reps`,`weight`,`rpe`,`fk_set_exercise`,`fk_set_link`,`fk_set_workout`)
# 	VALUES
# 	(5,315,6,exercise_id,link_id,workout_id);

