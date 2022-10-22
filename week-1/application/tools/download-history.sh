#!/usr/bin/env bash

source tools/strategy.env
PAIR_SYMBOL="BTC/USDT"

docker run --rm -v $(pwd)/user_data/:/freqtrade/user_data/ \
        freqtradeorg/freqtrade:develop download-data \
         --pairs ${PAIR_SYMBOL} --exchange ${EXCHANGE} \
         -t ${TIME_INTERVALS} --trading-mode ${MARKET} \
         --timerange ${DOWNLOAD_TIMERANGE}
