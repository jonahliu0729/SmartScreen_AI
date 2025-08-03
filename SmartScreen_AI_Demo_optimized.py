import importlib
import subprocess
import sys

# Required external modules
required_modules = {
    "numpy": "numpy",
    "pandas": "pandas",
    "plotly": "plotly",
    "scikit-learn": "sklearn",  # key=package name, value=import name
    "streamlit": "streamlit"
}

# Check which packages are missing
missing = []
for package, import_name in required_modules.items():
    try:
        importlib.import_module(import_name)
    except ImportError:
        missing.append(package)

# Install missing packages only if needed
if missing:
    print(f"Installing missing packages: {', '.join(missing)}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
else:
    print("✅ All dependencies are already installed. Starting script...")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="SmartScreen AI", page_icon="📱", layout="wide")

# -----------------------------
# 1. Initialize session state
# -----------------------------
if "screen_time_data" not in st.session_state:
    days = pd.date_range(datetime.now() - timedelta(days=6), datetime.now())
    st.session_state.screen_time_data = pd.DataFrame({
        "Date": days,
        "Social Media (hrs)": np.random.uniform(0.5, 4, len(days)),
        "Entertainment (hrs)": np.random.uniform(0.5, 3, len(days)),
        "Work/Study (hrs)": np.random.uniform(0.5, 5, len(days)),
    })

st.title("📱 SmartScreen AI Dashboard")
st.markdown("Track usage, get AI nudges, and forecast your screen time – all **offline**!")

# Button to simulate a new day of screen time
if st.button("📊 Simulate Today's Usage"):
    today = datetime.now()
    new_day = pd.DataFrame({
        "Date": [today],
        "Social Media (hrs)": [round(random.uniform(0.5, 4), 2)],
        "Entertainment (hrs)": [round(random.uniform(0.5, 3), 2)],
        "Work/Study (hrs)": [round(random.uniform(0.5, 5), 2)],
    })
    st.session_state.screen_time_data = pd.concat(
        [st.session_state.screen_time_data, new_day]
    ).drop_duplicates(subset=["Date"]).sort_values("Date")

data = st.session_state.screen_time_data.copy()

# -----------------------------
# 2. Multi-Tab Layout
# -----------------------------
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🤖 AI Insights", "🔮 Forecast"])

# ===== TAB 1: DASHBOARD =====
with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Screen Time Over Time")
        fig_line = px.line(
            data,
            x="Date",
            y=["Social Media (hrs)", "Entertainment (hrs)", "Work/Study (hrs)"],
            markers=True,
            title="Daily Screen Time Usage",
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        st.subheader("Weekly Breakdown")
        weekly_avg = data[["Social Media (hrs)", "Entertainment (hrs)", "Work/Study (hrs)"]].mean()
        fig_pie = px.pie(
            values=weekly_avg.values,
            names=weekly_avg.index,
            title="Average Screen Time by Category",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Screen Time Log")
    st.dataframe(data.set_index("Date").style.format("{:.2f}"))

# ===== TAB 2: AI INSIGHTS =====
with tab2:
    st.subheader("Today's SmartScreen AI Nudges")
    latest = data.iloc[-1]
    nudges = []

    if latest["Social Media (hrs)"] > 2.5:
        nudges.append("⚠️ High social media usage today. Consider a break!")
    if latest["Work/Study (hrs)"] < 1:
        nudges.append("📚 Low productive time today. Try a 25-min focus session.")
    if latest["Entertainment (hrs)"] > 2:
        nudges.append("🍿 Lots of entertainment today. Balance with a walk!")

    if not nudges:
        st.success("✅ Great balance today! Keep it up!")
    else:
        for nudge in nudges:
            st.warning(nudge)

    # Daily trend analysis
    st.subheader("Weekly Trends")
    trend_text = []
    for category in ["Social Media (hrs)", "Entertainment (hrs)", "Work/Study (hrs)"]:
        if data[category].iloc[-1] > data[category].mean():
            trend_text.append(f"⬆ {category} is above your weekly average.")
        else:
            trend_text.append(f"⬇ {category} is below your weekly average.")
    for t in trend_text:
        st.info(t)

# ===== TAB 3: FORECAST =====
with tab3:
    st.subheader("Predicted Screen Time for Tomorrow")

    predictions = {}
    for category in ["Social Media (hrs)", "Entertainment (hrs)", "Work/Study (hrs)"]:
        X = np.arange(len(data)).reshape(-1, 1)
        y = data[category].values
        model = LinearRegression()
        model.fit(X, y)
        tomorrow_x = np.array([[len(data)]])
        predictions[category] = model.predict(tomorrow_x)[0]

    pred_df = pd.DataFrame([predictions], index=["Predicted Tomorrow"])
    st.dataframe(pred_df.style.format("{:.2f}"))

    fig_pred = px.bar(
        pred_df.T,
        title="Predicted Screen Time for Tomorrow",
        labels={"index": "Category", "value": "Hours"},
    )
    st.plotly_chart(fig_pred, use_container_width=True)

st.markdown("**Tip:** Use tabs to explore the dashboard, insights, and forecasts!")
