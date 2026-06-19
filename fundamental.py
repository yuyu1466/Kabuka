def fundamentals(info: dict) -> dict:
    keys = {
        "trailingPE": "PER",
        "priceToBook": "PBR",
        "dividendYield": "配当利回り",
        "returnOnEquity": "ROE",
        "revenueGrowth": "売上成長率",
    }
    return {label: info.get(k) for k, label in keys.items()}

def buy_zone(df, info):
    """「いくらで買うか」の目安を複数出す（予測ではなく参考値）"""
    last_close = df["Close"].iloc[-1]
    sma75 = df["SMA75"].iloc[-1]
    bb_lower = df["BB_lower"].iloc[-1]
    return {
        "現在値": round(last_close, 2),
        "押し目目安(75日線)": round(sma75, 2),
        "割安ゾーン(BB下限)": round(bb_lower, 2),
    }
