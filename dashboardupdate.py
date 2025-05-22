import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Set Streamlit page config
st.set_page_config(page_title="Opto", layout="wide")

# Header
st.markdown("""
    <style>
    .header-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #f9f9f9;
        padding: 10px 20px;
        border-radius: 8px;
        border: 1px solid #ddd;
    }}
    .header-left {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .green-dot {{
        height: 12px;
        width: 12px;
        background-color: #28a745;
        border-radius: 50%;
        display: inline-block;
    }}
    .logo-eye {{
        width: 28px;
        height: 28px;
    }}
    .title {{
        font-size: 24px;
        font-weight: bold;
    }}
    .timestamp {{
        font-size: 14px;
        color: #666;
    }}
    </style>
    <div class="header-container">
        <div class="header-left">
            <span class="green-dot"></span>
            <img src="https://upload.wikimedia.org/wikipedia/commons/2/24/Red_eye_icon.svg" class="logo-eye" />
            <span class="title">Opto</span>
        </div>
        <div class="timestamp">Last updated: {}</div>
    </div>
""".format(datetime.now().strftime("%d-%b-%Y - %H:%M")), unsafe_allow_html=True)

# Sidebar controls
st.sidebar.header("Settings")
selected_symbol = st.sidebar.selectbox("Select Symbol", ["SPY", "QQQ", "AAPL", "TSLA"], index=0)
interval = st.sidebar.radio("Select Interval", ["1min", "5min", "15min", "30min"], index=1)
filter_option = st.sidebar.radio("Filter Flow Type", ["Net Flow", "Bullish Only", "Bearish Only"], index=0)
manual_refresh = st.sidebar.button("Refresh Data")

# Generate synthetic data
np.random.seed(42)
n = 100
timestamps = [datetime.now() - timedelta(minutes=99 - i) for i in range(n)]
calls = np.cumsum(np.random.randint(-1000000, 1500000, size=n))
puts = np.cumsum(np.random.randint(-1500000, 1000000, size=n))
spy_price = 420 + np.cumsum(np.random.randn(n) * 0.5)

df = pd.DataFrame({
    'timestamp': timestamps,
    'calls': calls,
    'puts': puts,
    'spy': spy_price
})

# Filter based on selection
if filter_option == "Bullish Only":
    df['puts'] = 0
elif filter_option == "Bearish Only":
    df['calls'] = 0

# Matplotlib chart
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(df['timestamp'], df['calls'], color='green', label='All Calls', linewidth=2)
ax1.plot(df['timestamp'], df['puts'], color='crimson', label='All Puts', linewidth=2)
ax1.set_ylabel('Cumulative Net Premiums', fontsize=12)
ax1.tick_params(axis='y')
ax1.legend(loc='upper left')

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45)
ax1.set_xlabel("Time")

ax2 = ax1.twinx()
ax2.plot(df['timestamp'], df['spy'], color='gray', linestyle='--', alpha=0.5, label='{} Price'.format(selected_symbol))
ax2.set_ylabel('{} Stock Price'.format(selected_symbol), fontsize=12)
ax2.tick_params(axis='y', labelcolor='gray')

fig.suptitle("Opto", fontsize=16)
ax1.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()

# Show chart in Streamlit
st.pyplot(fig)
