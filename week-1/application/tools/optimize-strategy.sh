#!/usr/bin/env bash

source ./tools/strategy.env
usage="Usage: ${BASE} <strategy> <CalmarHyperOptLoss|MaxDrawDownHyperOptLoss|MaxDrawDownRelativeHyperOptLoss|OnlyProfitHyperOptLoss|ProfitDrawDownHyperOptLoss|SharpeHyperOptLoss|SharpeHyperOptLossDaily|ShortTradeDurHyperOptLoss|SortinoHyperOptLoss|SortinoHyperOptLossDaily>" 
mkdir -p user_data/hyperopt_configs/${MARKET}/


if [ $# -ge 1 ]
then
    STRATEGY=$1
    if [ $# -ge 2 ]; 
    then 
        LOSS_FUNCTION=$2 ; 
    else
        LOSS_FUNCTION="CalmarHyperOptLoss" ; 
        LOSS_FUNCTION="MaxDrawDownRelativeHyperOptLoss" ; 
        echo "INFO: Using default loss function: ${LOSS_FUNCTION}"
    fi

    docker run --rm -v $(pwd)/user_data/:/freqtrade/user_data/ freqtradeorg/freqtrade:develop hyperopt \
        -e ${TRAINING_EPOCHS} \
        --hyperopt-loss ${LOSS_FUNCTION} \
        --spaces roi stoploss buy sell \
        --dry-run-wallet ${TRAINING_WALLET_SIZE}  --fee ${TRAINING_FEES} --timerange=${TRAINING_TIMERANGE} \
        --config /freqtrade/user_data/configs/${EXCHANGE}/${STRATEGY}-pair.json \
        --config /freqtrade/user_data/configs/${STRATEGY}.json \
        --config /freqtrade/user_data/configs/${MARKET}-market.json \
        --strategy ${STRATEGY}

    if [ -f user_data/strategies/${STRATEGY}.json ]; then
        cp -f user_data/strategies/${STRATEGY}.json user_data/hyperopt_configs/${MARKET}/${STRATEGY}-${LOSS_FUNCTION}.json
    fi
else
    echo ${usage}
fi

