import pandas as pd
import numpy as np

try:
    import yfinance as yf
except Exception:  # pragma: no cover - environment may block access
    yf = None


def fetch_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    """Fetch historical price data for a symbol using yfinance."""
    if yf is None:
        raise ImportError("yfinance is required to fetch data")
    return yf.download(symbol, start=start, end=end, progress=False)


def compute_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    """Compute the Relative Strength Index (RSI) for a price series."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    rsi = np.where(avg_loss == 0, 100, rsi)
    rsi = np.where(avg_gain == 0, 0, rsi)
    return pd.Series(rsi, index=series.index)


def find_oversold(symbols, start, end, threshold=30, window=14):
    """Return a dict of symbols with their latest RSI if oversold."""
    oversold = {}
    for symbol in symbols:
        data = fetch_data(symbol, start, end)
        if data.empty:
            continue
        rsi = compute_rsi(data['Close'], window)
        latest_rsi = rsi.iloc[-1]
        if latest_rsi < threshold:
            oversold[symbol] = latest_rsi
    return oversold


def backtest_strategy(symbol, start, end, threshold=30, hold_days=5, window=14):
    """Simple backtest: buy when RSI < threshold and hold for a number of days."""
    data = fetch_data(symbol, start, end)
    data = data[['Open', 'Close']].copy()
    data['RSI'] = compute_rsi(data['Close'], window)
    data['Signal'] = (data['RSI'] < threshold).shift(1)
    trades = []
    for i, row in data.iterrows():
        if not row['Signal']:
            continue
        buy_price = row['Open']
        sell_index = data.index.get_loc(i) + hold_days
        if sell_index >= len(data):
            break
        sell_date = data.index[sell_index]
        sell_price = data.loc[sell_date, 'Open']
        return_pct = (sell_price - buy_price) / buy_price
        trades.append({
            'buy_date': i,
            'sell_date': sell_date,
            'buy_price': buy_price,
            'sell_price': sell_price,
            'return_pct': return_pct,
        })
    return trades


if __name__ == "__main__":
    # Example usage: find oversold stocks
    symbols = ["AAPL", "MSFT", "TSLA"]
    try:
        oversold = find_oversold(symbols, "2023-01-01", "2023-12-31")
        for sym, rsi in oversold.items():
            print(f"{sym} is oversold (RSI={rsi:.2f})")
    except ImportError as e:
        print(e)
