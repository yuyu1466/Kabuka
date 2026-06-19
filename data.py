import yfinance as yf
import pandas as pd

def get_price(ticker: str, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    df = yf.Ticker(ticker).history(period=period, interval=interval)
    return df

def get_info(ticker: str) -> dict:
    return yf.Ticker(ticker).info
