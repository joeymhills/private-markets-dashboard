import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from scipy.optimize import newton


st.set_page_config(page_title="Fund Performance Tracker", layout="centered")

# ---------- Functions ----------
@st.cache_data
def load_cash_flows(filepath):
    df = pd.read_csv(filepath, parse_dates=["Date"])
    df.sort_values("Date", inplace=True)
    return df

def calculate_moic(df):
# Only use the last NAV row for MOIC
    latest_nav = df[df["Type"] == "NAV"]["Amount"].iloc[-1] if not df[df["Type"] == "NAV"].empty else 0
    total_calls = df[df["Type"] == "Capital Call"]["Amount"].sum()
    total_distributions = df[df["Type"] == "Distribution"]["Amount"].sum()

    moic = (total_distributions + latest_nav) / total_calls if total_calls > 0 else None

    return round(moic, 2) if moic else None

def calculate_irr(df):
    # Build dated cash flows
    cash_flows = []
    for _, row in df.iterrows():
        amount = -row["Amount"] if row["Type"] == "Capital Call" else row["Amount"]
        cash_flows.append((row["Date"], amount))

    # Add NAV as final distribution if it exists
    nav_row = df[df["Type"] == "NAV"]
    if not nav_row.empty:
        nav = nav_row["Amount"].iloc[-1]
        date = nav_row["Date"].iloc[-1]
        cash_flows.append((date, nav))

    if len(cash_flows) < 2:
        return None

    # XIRR calculation
    dates = [cf[0] for cf in cash_flows]
    amounts = [cf[1] for cf in cash_flows]

    def xnpv(rate):
        return sum(
            amt / (1 + rate) ** ((date - dates[0]).days / 365.0)
            for amt, date in zip(amounts, dates)
        )

    try:
        irr = newton(func=xnpv, x0=0.1)
        return round(irr * 100, 2)
    except (RuntimeError, OverflowError):
        return None
# ---------- Streamlit App ----------
st.title("📈 Private Markets Performance Analyzer")

uploaded_file = st.file_uploader("Upload a cash flow CSV file", type="csv")

if uploaded_file:
    df = load_cash_flows(uploaded_file)

    st.subheader("📊 Cash Flows")
    st.dataframe(df)

    moic = calculate_moic(df)
    irr = calculate_irr(df)

    st.subheader("📌 Performance Summary")
    col1, col2 = st.columns(2)
    col1.metric("MOIC", f"{moic:.2f}" if moic else "N/A")
    col2.metric("IRR", f"{irr:.2f}%" if irr else "N/A")

    st.subheader("🧾 Cash Flow Over Time")
    chart_df = df.copy()
    chart_df["Signed Amount"] = chart_df.apply(
        lambda row: -row["Amount"] if row["Type"] == "Capital Call" else row["Amount"], axis=1
    )
    st.bar_chart(chart_df.set_index("Date")["Signed Amount"])

else:
    st.info("Please upload a CSV file with Date, Type, Amount columns.")

