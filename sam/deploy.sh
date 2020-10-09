#!/usr/bin/env bash
set -e
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

STAGE=$1
SERVICE="lift-log-api"
BUCKET="lift-log"
REGION="us-east-1"
USER=$LIFTLOG_DB_USER
PASSWORD=$LIFTLOG_DB_PW


echo
echo -e "${CYAN}CloudFormation Packaging...${NC}"
aws cloudformation package \
    --region ${REGION} \
    --template-file template.yaml \
    --output-template-file packaged-template.yml \
    --s3-bucket ${BUCKET} 


echo
echo -e "${CYAN}CloudFormation Deploying...${NC}"
aws cloudformation deploy  \
    --region ${REGION} \
    --template-file packaged-template.yml \
    --stack-name ${SERVICE} \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-override LiftLogDbPw=${PASSWORD} \
    LiftLogDbUser=${USER}
