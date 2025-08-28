from oversold import find_oversold

if __name__ == "__main__":
    symbols = ["AAPL", "MSFT", "TSLA"]
    oversold = find_oversold(symbols, "2023-01-01", "2023-12-31")
    for sym, rsi in oversold.items():
        print(f"{sym} is oversold (RSI={rsi:.2f})")
