import pandas as pd

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # 移動平均（短期・長期）
    df["SMA25"] = df["Close"].rolling(25).mean()
    df["SMA75"] = df["Close"].rolling(75).mean()
    df["SMA200"] = df["Close"].rolling(200).mean()

    # RSI（14日）
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["Close"].ewm(span=12).mean()
    ema26 = df["Close"].ewm(span=26).mean()
    df["MACD"] = ema12 - ema26
    df["Signal"] = df["MACD"].ewm(span=9).mean()

    # ボリンジャーバンド
    ma20 = df["Close"].rolling(20).mean()
    std20 = df["Close"].rolling(20).std()
    df["BB_upper"] = ma20 + 2 * std20
    df["BB_lower"] = ma20 - 2 * std20
    return df

def signals(df: pd.DataFrame) -> dict:
    last = df.iloc[-1]
    out = {}
    out["RSI"] = (
        "売られすぎ（割安の可能性）" if last["RSI"] < 30
        else "買われすぎ（割高の可能性）" if last["RSI"] > 70
        else "中立"
    )
    out["短期トレンド"] = "上昇" if last["SMA25"] > last["SMA75"] else "下降"
    out["長期トレンド"] = "上昇" if last["Close"] > last["SMA200"] else "下降"
    out["MACD"] = "買い寄り" if last["MACD"] > last["Signal"] else "売り寄り"
    return out
