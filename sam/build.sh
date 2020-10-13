#!/usr/bin/env bash

USER=$LIFTLOG_DB_USER
PASSWORD=$LIFTLOG_DB_PW

echo ${USER}
echo ${USER}

ttab -s nickznaj "sam local start-api --port 3333"

ttab -s nickznaj "nodemon --exec sam build --parameter-overrides 'LiftLogDbUser=${USER},LiftLogDbPw=${PASSWORD}'"


