#!/usr/bin/env bash

USER=$LIFTLOG_DB_USER
PASSWORD=$LIFTLOG_DB_PW

echo ${USER}
echo ${USER}

sam build --parameter-overrides 'LiftLogDbUser=${USER},LiftLogDbPw=${PASSWORD}'

sam local start-api --port 3333

