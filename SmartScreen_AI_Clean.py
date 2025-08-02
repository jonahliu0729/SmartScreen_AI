import streamlit as st
import pandas as pd
import numpy as np

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="SmartScreen AI",
    page_icon="💡",
    layout="wide"
)

# -------------------- GLOBAL STYLES --------------------
st.markdown("""
    <style>
        /* Main Title */
        .main-title {
            text-align: center;
            font-size: 3rem;
            font-weight: 700;
            color: #2E86C1;
            margin-bottom: 0.2rem;
        }

        /* Subtitle */
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #566573;
            margin-bottom: 2rem;
        }

        /* Buttons */
        .stButton>button {
            background-color: #2E86C1;
            color: white;
            font-size: 1rem;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #1F618D;
        }

        /* Footer */
        footer {visibility: hidden;}
        .footer-text {
            text-align: center;
            color: gray;
            font-size: 0.9rem;
            margin-top: 3rem;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("<p class='main-title'>SmartScreen AI</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Smarter Insights, Cleaner Visuals</p>", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
st.sidebar.title("⚙️ Controls")
page = st.sidebar.radio("Navigate", ["🏠 Home", "📊 Analytics", "⚙️ Settings"])

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh App"):
    st.rerun()

# -------------------- PAGE CONTENT --------------------
if page == "🏠 Home":
    st.subheader("Welcome to SmartScreen AI 👋")
    st.write("""
        This platform helps you visualize, analyze, and present your data in a smarter way.  
        Use the sidebar to navigate through **Analytics** or adjust **Settings**.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Active Sessions", value="245", delta="+12%")
    with col2:
        st.metric(label="Avg. Processing Time", value="1.8s", delta="-0.2s")
    with col3:
        st.metric(label="Data Processed Today", value="12.4 GB", delta="+5%")

    st.markdown("---")
    st.info("💡 Tip: Check the **Analytics** page for detailed data insights.")

elif page == "📊 Analytics":
    st.subheader("📊 Analytics Dashboard")

    # Example random data visualization
    st.write("Here’s a sample analytics preview using generated data:")
    data = pd.DataFrame({
        "Category": ["A", "B", "C", "D"],
        "Values": np.random.randint(10, 100, 4)
    })

    col1, col2 = st.columns([2, 3])
    with col1:
        st.dataframe(data, use_container_width=True)

    with col2:
        st.bar_chart(data.set_index("Category"))

    st.success("Analytics loaded successfully! Use this area to connect to real data sources.")

elif page == "⚙️ Settings":
    st.subheader("⚙️ Application Settings")
    theme = st.selectbox("Select Theme", ["Light", "Dark", "Auto"])
    notifications = st.checkbox("Enable Notifications", value=True)
    refresh_rate = st.slider("Data Refresh Rate (seconds)", 5, 60, 15)

    st.write(f"**Theme:** {theme}")
    st.write(f"**Notifications:** {'On' if notifications else 'Off'}")
    st.write(f"**Refresh every:** {refresh_rate} seconds")

    if st.button("Save Settings"):
        st.success("✅ Settings saved successfully!")

# -------------------- FOOTER --------------------
st.markdown("<p class='footer-text'>© 2025 SmartScreen AI. All rights reserved.</p>", unsafe_allow_html=True)
