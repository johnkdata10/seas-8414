from pandas import DataFrame
import talib.abstract as ta
import numpy as np
from freqtrade.strategy import (DecimalParameter, IStrategy, IntParameter)
from datetime import datetime, timedelta  # noqa
from typing import Optional, Union  # noqa

# super trend performance
# Training dataset: 2022 H1
# BACKTEST_TIMERANGE="20220101-"          # (P) 233% - (M) -58% down - (D) 0.7%
# BACKTEST_TIMERANGE="20200101-20210101"  # (P) 144% - (M) 304% up - (D) 32% - Not enough historical data
# BACKTEST_TIMERANGE="20210101-20220101"  # (P) 646% - (M) 61% mixed (D) 32%
# NOTE: Increasing leverage results in losses - do NOT use it.

class Strategy3(IStrategy):
    INTERFACE_VERSION: int = 3

    can_short = True
    # Buy hyperspace params:
    buy_params = {
        "buy_m1": 4,
        "buy_m2": 7,
        "buy_m3": 1,
        "buy_p1": 8,
        "buy_p2": 9,
        "buy_p3": 8,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_m1": 1,
        "sell_m2": 3,
        "sell_m3": 6,
        "sell_p1": 16,
        "sell_p2": 18,
        "sell_p3": 18,
    }

    # ROI table:
    minimal_roi = {"0": 0.1, "30": 0.75, "60": 0.05, "120": 0.025}

    # Stoploss:
    stoploss = -0.265

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.05
    trailing_stop_positive_offset = 0.1
    trailing_only_offset_is_reached = False

    timeframe = "1h"

    startup_candle_count = 18

    buy_m1 = IntParameter(1, 7, default=1)
    buy_m2 = IntParameter(1, 7, default=3)
    buy_m3 = IntParameter(1, 7, default=4)
    buy_p1 = IntParameter(7, 21, default=14)
    buy_p2 = IntParameter(7, 21, default=10)
    buy_p3 = IntParameter(7, 21, default=10)

    sell_m1 = IntParameter(1, 7, default=1)
    sell_m2 = IntParameter(1, 7, default=3)
    sell_m3 = IntParameter(1, 7, default=4)
    sell_p1 = IntParameter(7, 21, default=14)
    sell_p2 = IntParameter(7, 21, default=10)
    sell_p3 = IntParameter(7, 21, default=10)

    protect_optimize = True
    cooldown_lookback = IntParameter(1, 240, default=5, space="protection", optimize=protect_optimize)
    max_drawdown_lookback = IntParameter(1, 288, default=12, space="protection", optimize=protect_optimize)
    max_drawdown_trade_limit = IntParameter(1, 20, default=5, space="protection", optimize=protect_optimize)
    max_drawdown_stop_duration = IntParameter(1, 288, default=12, space="protection", optimize=protect_optimize)
    max_allowed_drawdown = DecimalParameter(0.10, 0.50, default=0.20, decimals=2, space="protection",
                                            optimize=protect_optimize)
    stoploss_guard_lookback = IntParameter(1, 288, default=12, space="protection", optimize=protect_optimize)
    stoploss_guard_trade_limit = IntParameter(1, 20, default=3, space="protection", optimize=protect_optimize)
    stoploss_guard_stop_duration = IntParameter(1, 288, default=12, space="protection", optimize=protect_optimize)

    leverage_optimize = True
    leverage_num = IntParameter(low=1, high=10, default=1, space='buy', optimize=leverage_optimize)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        for multiplier in self.buy_m1.range:
            for period in self.buy_p1.range:
                dataframe[f"supertrend_1_buy_{multiplier}_{period}"] = self.supertrend(
                    dataframe, multiplier, period
                )["STX"]

        for multiplier in self.buy_m2.range:
            for period in self.buy_p2.range:
                dataframe[f"supertrend_2_buy_{multiplier}_{period}"] = self.supertrend(
                    dataframe, multiplier, period
                )["STX"]

        for multiplier in self.buy_m3.range:
            for period in self.buy_p3.range:
                dataframe[f"supertrend_3_buy_{multiplier}_{period}"] = self.supertrend(
                    dataframe, multiplier, period
                )["STX"]

        for multiplier in self.sell_m1.range:
            for period in self.sell_p1.range:
                dataframe[f"supertrend_1_sell_{multiplier}_{period}"] = self.supertrend(
                    dataframe, multiplier, period
                )["STX"]

        for multiplier in self.sell_m2.range:
            for period in self.sell_p2.range:
                dataframe[f"supertrend_2_sell_{multiplier}_{period}"] = self.supertrend(
                    dataframe, multiplier, period
                )["STX"]

        for multiplier in self.sell_m3.range:
            for period in self.sell_p3.range:
                dataframe[f"supertrend_3_sell_{multiplier}_{period}"] = self.supertrend(
                    dataframe, multiplier, period
                )["STX"]

        dataframe["RSI"] = ta.RSI(dataframe)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                    dataframe[f"supertrend_1_buy_{self.buy_m1.value}_{self.buy_p1.value}"]
                    == "up"
            )
            & (
                    dataframe[f"supertrend_2_buy_{self.buy_m2.value}_{self.buy_p2.value}"]
                    == "up"
            )
            & (
                    dataframe[f"supertrend_3_buy_{self.buy_m3.value}_{self.buy_p3.value}"]
                    == "up"
            )
            & (  # The three indicators are 'up' for the current candle
                    dataframe["volume"] > 0
            ),
            "enter_long",
        ] = 0 ## RAVI: Make it a short only strategy

        dataframe.loc[
            (
                    dataframe[
                        f"supertrend_1_sell_{self.sell_m1.value}_{self.sell_p1.value}"
                    ]
                    == "down"
            )
            & (
                    dataframe[
                        f"supertrend_2_sell_{self.sell_m2.value}_{self.sell_p2.value}"
                    ]
                    == "down"
            )
            & (
                    dataframe[
                        f"supertrend_3_sell_{self.sell_m3.value}_{self.sell_p3.value}"
                    ]
                    == "down"
            )
            & (  # The three indicators are 'down' for the current candle
                    dataframe["volume"] > 0
            ),
            "enter_short",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    dataframe[
                        f"supertrend_2_sell_{self.sell_m2.value}_{self.sell_p2.value}"
                    ]
                    == "down"
            ),
            "exit_long",
        ] = 1

        dataframe.loc[
            (
                    dataframe[f"supertrend_2_buy_{self.buy_m2.value}_{self.buy_p2.value}"]
                    == "up"
            ),
            "exit_short",
        ] = 1

        return dataframe

    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: Optional[str],
                 side: str, **kwargs) -> float:
        """
        Customize leverage for each new trade. This method is only called in futures mode.

        :param pair: Pair that's currently analyzed
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
        :param proposed_leverage: A leverage proposed by the bot.
        :param max_leverage: Max leverage allowed on this pair
        :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
        :param side: 'long' or 'short' - indicating the direction of the proposed trade
        :return: A leverage amount, which is between 1.0 and max_leverage.
        """
        return self.leverage_num.value

    """
        Supertrend Indicator; adapted for freqtrade
        from: https://github.com/freqtrade/freqtrade-strategies/issues/30
    """

    def supertrend(self, dataframe: DataFrame, multiplier, period):
        df = dataframe.copy()

        df["TR"] = ta.TRANGE(df)
        df["ATR"] = ta.SMA(df["TR"], period)

        st = "ST_" + str(period) + "_" + str(multiplier)
        stx = "STX_" + str(period) + "_" + str(multiplier)

        # Compute basic upper and lower bands
        df["basic_ub"] = (df["high"] + df["low"]) / 2 + multiplier * df["ATR"]
        df["basic_lb"] = (df["high"] + df["low"]) / 2 - multiplier * df["ATR"]

        # Compute final upper and lower bands
        df["final_ub"] = 0.00
        df["final_lb"] = 0.00
        for i in range(period, len(df)):
            df["final_ub"].iat[i] = (
                df["basic_ub"].iat[i]
                if df["basic_ub"].iat[i] < df["final_ub"].iat[i - 1]
                   or df["close"].iat[i - 1] > df["final_ub"].iat[i - 1]
                else df["final_ub"].iat[i - 1]
            )
            df["final_lb"].iat[i] = (
                df["basic_lb"].iat[i]
                if df["basic_lb"].iat[i] > df["final_lb"].iat[i - 1]
                   or df["close"].iat[i - 1] < df["final_lb"].iat[i - 1]
                else df["final_lb"].iat[i - 1]
            )

        # Set the Supertrend value
        df[st] = 0.00
        for i in range(period, len(df)):
            df[st].iat[i] = (
                df["final_ub"].iat[i]
                if df[st].iat[i - 1] == df["final_ub"].iat[i - 1]
                   and df["close"].iat[i] <= df["final_ub"].iat[i]
                else df["final_lb"].iat[i]
                if df[st].iat[i - 1] == df["final_ub"].iat[i - 1]
                   and df["close"].iat[i] > df["final_ub"].iat[i]
                else df["final_lb"].iat[i]
                if df[st].iat[i - 1] == df["final_lb"].iat[i - 1]
                   and df["close"].iat[i] >= df["final_lb"].iat[i]
                else df["final_ub"].iat[i]
                if df[st].iat[i - 1] == df["final_lb"].iat[i - 1]
                   and df["close"].iat[i] < df["final_lb"].iat[i]
                else 0.00
            )
        # Mark the trend direction up/down
        df[stx] = np.where(
            (df[st] > 0.00), np.where((df["close"] < df[st]), "down", "up"), np.NaN
        )

        # Remove basic and final bands from the columns
        df.drop(["basic_ub", "basic_lb", "final_ub", "final_lb"], inplace=True, axis=1)

        df.fillna(0, inplace=True)

        return DataFrame(index=df.index, data={"ST": df[st], "STX": df[stx]})
