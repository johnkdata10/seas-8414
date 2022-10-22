#!/usr/bin/env bash

if [ $# -eq 1 ]
then
  docker run --rm -v $(pwd)/user_data/:/freqtrade/user_data/ freqtradeorg/freqtrade:latest new-strategy --template advanced --strategy ${1}
else
  echo "Usage: $0 <strategy>"
fi


cp $(pwd)/user_data/data/prod/configs/binance/btcusdt-pair.json $(pwd)/user_data/configs/binance/${1}-pair.json
cp $(pwd)/user_data/configs/default.json $(pwd)/user_data/configs/${1}.json
