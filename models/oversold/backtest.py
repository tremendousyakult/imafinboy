from oversold import backtest_strategy

if __name__ == "__main__":
    # Example backtest
    trades = backtest_strategy("AAPL", "2023-01-01", "2023-12-31")
    for trade in trades:
        print(trade)
