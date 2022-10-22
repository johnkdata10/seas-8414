#!/usr/bin/env bash

# select instance template
DEV_INSTANCE_TEMPLATE="dev-instance.yml"
INSTANCE_TEMPLATE=${DEV_INSTANCE_TEMPLATE}
INPUT=devconfig.csv


# variables
OUTPUT=docker-compose.yml
PORT_MAP="port_map.py"

INSTANCE_USER_CONFIG="../user_data/configs/instances"
LOG_DIR="../user_data/logs"
DB_DIR="../user_data/db"
mkdir -p ${INSTANCE_USER_CONFIG}
mkdir -p ${DB_DIR}
mkdir -p ${LOG_DIR}

# ensure all data is accessible by docker containers
unamestr=$(uname)
if [[ "$unamestr" == 'Linux' ]]; then
   chown -R admin:admin ../user_data/
fi

# check for input file
[ ! -f $INPUT ] && {
  echo "$INPUT file not found"
  exit 99
}

# create dependencies
cat "common/docker-compose-common.yml" >${OUTPUT}
echo "servers = { \"$(hostname)\" : {" >${PORT_MAP}

while IFS=, read STRATEGY_NAME FEE MARKET ACCOUNT CONFIG_FILE PAIR INSTANCE PORT HYPEROPT TELEGRAM_TOKEN; do
  if [ "x${STRATEGY_NAME}" == "xSTRATEGY_NAME" ]; then continue; fi
  if [ -z "$MARKET" ]; then continue; fi # empty lines
  
  sed "s#STRATEGY_NAME#${STRATEGY_NAME}#g;s#PORT#${PORT}#g;s#FEE#${FEE}#g;s#MARKET#${MARKET}#g;s#CONFIG_FILE#${CONFIG_FILE}#g;s#ACCOUNT#${ACCOUNT}#g;s#PAIR#${PAIR}#g;s#INSTANCE#${INSTANCE}#g" ${INSTANCE_TEMPLATE} >>${OUTPUT}
  if [ "x${TELEGRAM_TOKEN}" == "xX" ]; then
    TELEGRAM_ENABLED=false
  else
    TELEGRAM_ENABLED=true
  fi
  sed "s#TELEGRAM_TOKEN#${TELEGRAM_TOKEN}#g;s#TELEGRAM_ENABLED#${TELEGRAM_ENABLED}#g" telegram.json >${INSTANCE_USER_CONFIG}/${INSTANCE}-telegram.json

  echo "{ \"bot_name\": \"${INSTANCE}\" }" >${INSTANCE_USER_CONFIG}/${INSTANCE}.json
  echo "    \"${INSTANCE}\" : ${PORT}," >>${PORT_MAP}

done <$INPUT

echo "}}" >>${PORT_MAP}
