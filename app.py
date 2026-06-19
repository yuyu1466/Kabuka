import streamlit as st
import plotly.graph_objects as go
from data import get_price, get_info
from technical import add_indicators, signals
from fundamental import fundamentals, buy_zone

st.set_page_config(page_title="株価分析ツール", layout="wide")
st.title("株価分析ダッシュボード")

ticker = st.text_input("ティッカー（例: AAPL, 7203.T）", "AAPL")
period = st.selectbox("期間", ["6mo", "1y", "2y", "5y"], index=2)

if ticker:
    df = add_indicators(get_price(ticker, period))
    info = get_info(ticker)

    # チャート
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df["Open"], high=df["High"],
                                 low=df["Low"], close=df["Close"], name="価格"))
    for ma, color in [("SMA25", "blue"), ("SMA75", "orange"), ("SMA200", "red")]:
        fig.add_trace(go.Scatter(x=df.index, y=df[ma], name=ma, line=dict(color=color)))
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("テクニカル判断（短期向け）")
        for k, v in signals(df).items():
            st.write(f"**{k}**: {v}")
    with col2:
        st.subheader("ファンダ指標（長期向け）")
        for k, v in fundamentals(info).items():
            st.write(f"**{k}**: {v}")

    st.subheader("買い値の目安（参考）")
    st.json(buy_zone(df, info))

    st.caption("※ これは投資助言ではありません。判断材料の可視化を目的としています。")
