import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from oversold import compute_rsi

def test_rsi_uptrend():
    prices = pd.Series(range(1, 16), dtype=float)
    rsi = compute_rsi(prices, window=14)
    assert rsi.iloc[-1] == 100

def test_rsi_downtrend():
    prices = pd.Series(range(15, 0, -1), dtype=float)
    rsi = compute_rsi(prices, window=14)
    assert rsi.iloc[-1] == 0
