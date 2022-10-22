#!/usr/bin/env python
from collections import OrderedDict
import pandas as pd
from freqtrade.misc import json_load
import sys
import glob
import quantstats as qs

# extend pandas functionality with metrics, etc.
qs.extend_pandas()

fields = ['model', 'strategy_name', 'total_trades', 'trade_count_long', 'trade_count_short', 'total_volume',
          'avg_stake_amount', 'profit_mean',
          'profit_median', 'profit_total', 'profit_total_long', 'profit_total_short', 'profit_total_abs',
          'profit_total_long_abs', 'profit_total_short_abs', 'cagr', 'profit_factor', 'backtest_start',
          'backtest_start_ts', 'backtest_end', 'backtest_end_ts', 'backtest_days', 'backtest_run_start_ts',
          'backtest_run_end_ts', 'trades_per_day', 'market_change', 'pairlist', 'stake_amount', 'stake_currency',
          'stake_currency_decimals', 'starting_balance', 'dry_run_wallet', 'final_balance', 'rejected_signals',
          'timedout_entry_orders', 'timedout_exit_orders', 'canceled_trade_entries', 'canceled_entry_orders',
          'replaced_entry_orders', 'max_open_trades', 'max_open_trades_setting', 'timeframe', 'timeframe_detail',
          'timerange', 'enable_protections', 'strategy_name', 'stoploss', 'trailing_stop', 'trailing_stop_positive',
          'trailing_stop_positive_offset', 'trailing_only_offset_is_reached', 'use_custom_stoploss', 'minimal_roi',
          'use_exit_signal', 'exit_profit_only', 'exit_profit_offset', 'ignore_roi_if_entry_signal',
          'backtest_best_day', 'backtest_worst_day', 'backtest_best_day_abs', 'backtest_worst_day_abs', 'winning_days',
          'draw_days', 'losing_days', 'wins', 'losses', 'draws', 'holding_avg', 'holding_avg_s', 'winner_holding_avg',
          'winner_holding_avg_s', 'loser_holding_avg', 'loser_holding_avg_s', 'max_drawdown', 'max_drawdown_account',
          'max_relative_drawdown', 'max_drawdown_abs', 'drawdown_start', 'drawdown_start_ts', 'drawdown_end',
          'drawdown_end_ts', 'max_drawdown_low', 'max_drawdown_high', 'csum_min', 'csum_max', 'sharpe_rf0',
          'sharpe_rf1', 'sharpe_rf2', 'sharpe_rf3', 'sharpe_rf4', 'sharpe_rf5', 'sharpe_rf10', 'smart_sharpe',
          'smart_sortino', 'autocorr_penalty', 'volatility', 'sortino', 'adjusted_sortino', 'calmar', 'recovery_factor',
          'risk_of_ruin', 'kelly_criterion', 'outlier_win_ratio', 'outlier_loss_ratio', 'risk_return_ratio',
          'gain_to_pain_ratio', 'avg_return', 'avg_win', 'avg_loss', 'exposure', 'consecutive_losses',
          'consecutive_wins']
fields = sorted(fields)
import os
simulations_dir = "user_data/backtest_results/*/"

for backtest_base in glob.glob(f"{simulations_dir}", recursive=False):
    backtest_dir = f"{backtest_base}/json/"
    # if not os.path.isdir(backtest_dir):
    #     backtest_dir = f"{backtest_base}/json/"

    result_file = f"{backtest_base}/backtest-summary.csv"

    simulation_files = f"{backtest_dir}/*[0-9].json"  # ignore meta files
    backtest_files = glob.glob(simulation_files)
    starting_balance = 10000


    def get_benchmark(filename=f"{backtest_dir}/Nibbles7-CalmarHyperOptLoss-*.json"):
        backtest_files = glob.glob(filename)
        print(backtest_files)
        for file in backtest_files:
            print("Filename : ", file)
            try:
                with open(file) as file_content:
                    stats = json_load(file_content)
                    strategy = list(stats["strategy"].keys())[0]
                    strategy_stats = stats['strategy'][strategy]

                    dates = []
                    profits = []
                    for date_profit in strategy_stats['daily_profit']:
                        dates.append(date_profit[0])
                        profits.append(date_profit[1])

                    equity = 0
                    equity_daily = []
                    for daily_profit in profits:
                        equity_daily.append(equity)
                        equity += float(daily_profit)

                    df = pd.DataFrame({'dates': dates, 'profits': profits})
                    df["dates"] = pd.to_datetime(df["dates"], infer_datetime_format=True)
                    df_returns = df.set_index('dates').squeeze()
            except:
                print("Skipping: ", file)
        return df_returns


    records = list()
    for file in backtest_files:
        print("Filename : ", file)

        ## TODO: Optimize this ugly code
        model = "-".join(file.split("/")[-1].split("-")[:4])
        timeline = "-".join(model.split("-")[2:])
        model = "-".join(model.split("-")[:2])
        print("Model : ", model)
        print("timeline : ", timeline)

        try:
            with open(file) as file_content:
                stats = json_load(file_content)
                strategy = list(stats["strategy"].keys())[0]
                strategy_stats = stats['strategy'][strategy]

                dates = []
                profits = []
                for date_profit in strategy_stats['daily_profit']:
                    dates.append(date_profit[0])
                    profits.append(date_profit[1])

                equity = 0
                equity_daily = []
                for daily_profit in profits:
                    equity_daily.append(equity)
                    equity += float(daily_profit)

                df = pd.DataFrame({'dates': dates, 'profits': profits})
                df["dates"] = pd.to_datetime(df["dates"], infer_datetime_format=True)
                df_returns = df.set_index('dates').squeeze()

                # # create a report
                # reports_dir = "/Users/rmallarapu/dev/mmn/models/simulations/reports/spot/tearsheets"
                # download_filename = f"{reports_dir}/{model}.html"
                # # benchmark = get_benchmark()
                # benchmark = None
                # # TODO: benchmark from None to benchamrk return df
                # try:
                #     qs.reports.html(df_returns, benchmark=None, rf=0.05, grayscale=False,
                #                     title=f"{model}", output=download_filename, compounded=True,
                #                     periods_per_year=365, download_filename=download_filename)
                # except:
                #     print("Failed to create tearsheet for : ", model)

                strategy_stats["sharpe_rf0"] = qs.stats.sharpe(df_returns, periods=365, rf=0)
                strategy_stats["sharpe_rf1"] = qs.stats.sharpe(df_returns, periods=365, rf=1)
                strategy_stats["sharpe_rf2"] = qs.stats.sharpe(df_returns, periods=365, rf=2)
                strategy_stats["sharpe_rf3"] = qs.stats.sharpe(df_returns, periods=365, rf=3)
                strategy_stats["sharpe_rf4"] = qs.stats.sharpe(df_returns, periods=365, rf=4)
                strategy_stats["sharpe_rf5"] = qs.stats.sharpe(df_returns, periods=365, rf=5)
                strategy_stats["sharpe_rf10"] = qs.stats.sharpe(df_returns, periods=365, rf=10)
                strategy_stats["smart_sharpe"] = qs.stats.smart_sharpe(df_returns, periods=365)
                strategy_stats["smart_sortino"] = qs.stats.smart_sortino(df_returns, periods=365)
                strategy_stats["autocorr_penalty"] = qs.stats.autocorr_penalty(df_returns)
                strategy_stats["volatility"] = qs.stats.volatility(df_returns, periods=365)
                strategy_stats["sortino"] = qs.stats.sortino(df_returns, periods=365)
                strategy_stats["adjusted_sortino"] = qs.stats.adjusted_sortino(df_returns, periods=365)
                strategy_stats["calmar"] = qs.stats.calmar(df_returns)
                # strategy_stats["kurtosis"] = qs.stats.kurtosis(df_returns)
                # strategy_stats["skew"] = qs.stats.skew(df_returns)
                # strategy_stats["ulcer_index"] = qs.stats.ulcer_index(df_returns)
                # strategy_stats["value_at_risk"] = qs.stats.value_at_risk(df_returns)
                strategy_stats["recovery_factor"] = qs.stats.recovery_factor(df_returns)
                strategy_stats["risk_of_ruin"] = qs.stats.ror(df_returns)
                strategy_stats["kelly_criterion"] = qs.stats.kelly_criterion(df_returns)

                strategy_stats["outlier_win_ratio"] = qs.stats.outlier_win_ratio(df_returns)
                strategy_stats["outlier_loss_ratio"] = qs.stats.outlier_loss_ratio(df_returns)
                strategy_stats["risk_return_ratio"] = qs.stats.risk_return_ratio(df_returns)
                strategy_stats["gain_to_pain_ratio"] = qs.stats.gain_to_pain_ratio(df_returns)
                # strategy_stats["omega"] = qs.stats.omega(df_returns)
                # strategy_stats["treynor_ratio"] = qs.stats.treynor_ratio(df_returns)
                strategy_stats["avg_return"] = qs.stats.avg_return(df_returns)
                strategy_stats["avg_win"] = qs.stats.avg_win(df_returns)
                strategy_stats["avg_loss"] = qs.stats.avg_loss(df_returns)
                strategy_stats["exposure"] = qs.stats.exposure(df_returns)
                strategy_stats["consecutive_losses"] = qs.stats.consecutive_losses(df_returns)
                strategy_stats["consecutive_wins"] = qs.stats.consecutive_wins(df_returns)

                # print("*" * 80)
                # print(strategy_stats.keys())

                strategy_stats["model"] = model
                strategy_stats["timeline"] = timeline
                # create an order dict
                new_dict = OrderedDict()
                for k in fields: new_dict[k] = strategy_stats[k]
                records.append(new_dict)
                # records.append(strategy_stats)
        except:
            print("Skipping file: ", file)

    df = pd.DataFrame(records)
    df.to_csv(result_file)
    # sys.exit(1)
