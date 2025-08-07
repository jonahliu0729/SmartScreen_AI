import importlib
import subprocess
import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# ==========================
# Dependency Management
# ==========================
required_modules = {
    "numpy": "numpy",
    "pandas": "pandas",
    "plotly": "plotly",
    "scikit-learn": "sklearn",
    "streamlit": "streamlit"
}

missing = []
for package, import_name in required_modules.items():
    try:
        importlib.import_module(import_name)
    except ImportError:
        missing.append(package)

if missing:
    print(f"Installing missing packages: {', '.join(missing)}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
else:
    print("✅ All dependencies installed.")

st.set_page_config(page_title="SmartScreen AI", page_icon="📱", layout="wide")

# ==========================
# 1. Initialize session state
# ==========================
if "screen_time_data" not in st.session_state:
    days = pd.date_range(datetime.now() - timedelta(days=6), datetime.now())
    st.session_state.screen_time_data = pd.DataFrame({
        "Date": days,
        "Social Media (hrs)": np.random.uniform(0.5, 4, len(days)),
        "Entertainment (hrs)": np.random.uniform(0.5, 3, len(days)),
        "Work/Study (hrs)": np.random.uniform(0.5, 5, len(days)),
    })

if "commit_mode" not in st.session_state:
    st.session_state.commit_mode = False
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "last_reflection_time" not in st.session_state:
    st.session_state.last_reflection_time = None
if "override_log" not in st.session_state:
    st.session_state.override_log = []

# ==========================
# Sidebar Controls
# ==========================
st.sidebar.title("⚙️ Controls")
if st.sidebar.button("Activate Commit Mode" if not st.session_state.commit_mode else "Commit Mode Active ✅"):
    st.session_state.commit_mode = not st.session_state.commit_mode
    st.sidebar.success(f"Commit Mode {'Activated' if st.session_state.commit_mode else 'Deactivated'}")

parent_notify = st.sidebar.checkbox("Send Positive Reports to Parent (Simulated)", value=False)

# ==========================
# Main Title
# ==========================
st.title("📱 SmartScreen AI Dashboard")
st.markdown("Track usage, get AI nudges, and forecast your screen time – now with **Commit Mode & Streaks**!")

# ==========================
# Simulate a new day
# ==========================
# Button to simulate a new day of screen time
if st.button("📊 Simulate Today's Usage"):
    today = datetime.now().date()  # Use date only (no time)
    
    # Normalize all existing dates to just date (no timestamp)
    existing_data = st.session_state.screen_time_data.copy()
    existing_data["Date"] = pd.to_datetime(existing_data["Date"]).dt.date
    
    # Remove existing entry for today
    existing_data = existing_data[existing_data["Date"] != today]
    
    # Generate new data for today
    new_day = pd.DataFrame({
        "Date": [today],
        "Social Media (hrs)": [round(random.uniform(0.5, 4), 2)],
        "Entertainment (hrs)": [round(random.uniform(0.5, 3), 2)],
        "Work/Study (hrs)": [round(random.uniform(0.5, 5), 2)],
    })

    # Combine and store
    st.session_state.screen_time_data = pd.concat([existing_data, new_day]).sort_values("Date")

# ==========================
# Tabs
# ==========================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🤖 AI Insights", "🔮 Forecast", "🧠 Reflection & Streaks"])

# ===== TAB 1: DASHBOARD =====
with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Screen Time Over Time")
        fig_line = px.line(
            st.session_state.screen_time_data,
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
            if st.session_state.commit_mode:
                if st.button(f"Override: {nudge}"):
                    reason = st.text_input("Why are you overriding?", key=nudge)
                    st.session_state.override_log.append((datetime.now(), nudge, reason))
                    st.warning("Override logged. Reflection required in Tab 4.")
            else:
                st.warning(nudge)

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

# ===== TAB 4: REFLECTION & STREAKS =====
with tab4:
    st.subheader("🧠 Reflection & Streak Tracking")
    
    # Calculate streak
    avg_social = data["Social Media (hrs)"].iloc[-1] <= 2.5
    avg_entertainment = data["Entertainment (hrs)"].iloc[-1] <= 2
    avg_work = data["Work/Study (hrs)"].iloc[-1] >= 1
    
    if avg_social and avg_entertainment and avg_work:
        st.session_state.streak += 1
        st.success(f"🔥 Current Streak: {st.session_state.streak} days!")
        if parent_notify:
            st.info("📧 Positive report sent to parent! (Simulated)")
    else:
        st.warning("Streak broken today. Reflect and try again tomorrow.")
        st.session_state.streak = 0

    st.subheader("Override & Reflection Log")
    if len(st.session_state.override_log) == 0:
        st.write("No overrides yet. Great job staying disciplined!")
    else:
        st.dataframe(pd.DataFrame(st.session_state.override_log, columns=["Time", "Nudge", "Reason"]))

    reflection = st.text_area("Reflect on today's screen-time habits:")
    if st.button("Save Reflection"):
        st.session_state.last_reflection_time = datetime.now()
        st.success("Reflection saved. Keep going strong!")
