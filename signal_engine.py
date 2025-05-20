import yfinance as yf
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import numpy as np

def analyze_market(pair: str):
    try:
        df = yf.download(pair, period="3mo", interval="1h")
        if df.empty or len(df) < 50:
            return None, None
        df["EMA"] = df["Close"].ewm(span=21).mean()
        df["MACD"] = df["Close"].ewm(span=12).mean() - df["Close"].ewm(span=26).mean()
        df["Volume_Signal"] = df["Volume"] > df["Volume"].rolling(window=20).mean()
        df["ATR"] = df["High"] - df["Low"]
        df["ATR"] = df["ATR"].rolling(window=14).mean()

        latest = df.iloc[-1]
        if latest["Close"] > latest["EMA"] and latest["MACD"] > 0 and latest["Volume_Signal"]:
            sl = round(latest["Close"] - latest["ATR"], 2)
            tp = round(latest["Close"] + latest["ATR"] * 2, 2)
            signal = f"🚨 Buy Signal for {pair}\nPrice: {latest['Close']:.2f}\nSL: {sl} | TP: {tp}"
        else:
            return None, None

        fig, ax = plt.subplots()
        df["Close"].tail(50).plot(ax=ax, label="Close")
        df["EMA"].tail(50).plot(ax=ax, label="EMA 21")
        ax.set_title(f"{pair} - Last Signals")
        ax.legend()
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        return signal, buffer
    except Exception as e:
        print(f"Error analyzing {pair}: {e}")
        return None, None