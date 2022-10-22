#!/usr/bin/env bash

source ./tools/strategy.env

# check for arguments
if [ $# -ge 1 ]
then
  STRATEGY=$1

  # ensure the required directory structure
  mkdir -p user_data/backtest_results/${MARKET}/{text,json}

  # find optimzation function
  if [ $# -ge 2 ]; then LOSS_FUNCTION=$2 ; fi

  # run backtest
  docker run --rm -v $(pwd)/user_data/:/freqtrade/user_data/ freqtradeorg/freqtrade:develop backtesting \
        --dry-run-wallet=${TRAINING_WALLET_SIZE} \
        --eps --timerange=${BACKTEST_TIMERANGE} \
        --enable-protections \
        --config /freqtrade/user_data/configs/${EXCHANGE}/${STRATEGY}-pair.json \
        --config /freqtrade/user_data/configs/${STRATEGY}.json \
        --config /freqtrade/user_data/configs/${MARKET}-market.json \
        --breakdown month --export trades \
        --export-filename user_data/backtest_results/${MARKET}/json/${STRATEGY}-${LOSS_FUNCTION}-${BACKTEST_TIMERANGE}.json \
        --strategy ${STRATEGY} | tee user_data/backtest_results/${MARKET}/text/${STRATEGY}-${LOSS_FUNCTION}-${BACKTEST_TIMERANGE}.txt
else
  echo "Usage: ${BASE} <strategy>"
fi




