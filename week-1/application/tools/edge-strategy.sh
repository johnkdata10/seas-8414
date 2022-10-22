#!/usr/bin/env bash

source ./tools/strategy.env

# check for arguments
if [ $# -ge 1 ]
then
  STRATEGY=$1

  # run backtest
  docker run --rm -v $(pwd)/user_data/:/freqtrade/user_data/ freqtradeorg/freqtrade:latest edge \
        --fee ${FEES} --timerange=${BACKTEST_TIMERANGE} \
        --config /freqtrade/user_data/configs/${EXCHANGE}/${PAIR}-pair.json \
        --config /freqtrade/user_data/configs/${MARKET}1.json \
        --config /freqtrade/user_data/configs/${MARKET}-market.json \
        --strategy ${STRATEGY}
else
  echo "Usage: ${BASE} <strategy>"
fi




