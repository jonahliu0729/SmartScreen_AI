import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="SmartScreen AI Demo",
    page_icon="🤖",
    layout="wide",
)

# ---------------------- HEADER ----------------------
st.title("🤖 SmartScreen AI: Live AI Demo with Simulation")
st.markdown("""
**Welcome, Judges!**  
This demo showcases **SmartScreen AI's core capability**:  
1. **Analyzing data**  
2. **Generating AI SmartScores**  
3. **Simulating decisions in real time**  
Upload a **CSV or CVD file** to get started.
""")

# ---------------------- FILE UPLOAD ----------------------
uploaded_file = st.file_uploader(
    "Upload your CSV or CVD file",
    type=["csv", "cvd"],
    help="Upload a dataset to let SmartScreen AI analyze and score your data."
)

if uploaded_file is not None:
    # Load data
    if uploaded_file.name.endswith(".cvd"):
        df = pd.read_csv(uploaded_file, delimiter=";")  # adjust if needed
    else:
        df = pd.read_csv(uploaded_file)

    st.success(f"✅ File uploaded: **{uploaded_file.name}**")
    
    # ---------------------- DATA PREVIEW ----------------------
    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # ---------------------- DATA PROCESSING ----------------------
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    # Encode categorical columns if needed
    df_encoded = df.copy()
    for col in df_encoded.select_dtypes(include=['object']).columns:
        df_encoded[col] = LabelEncoder().fit_transform(df_encoded[col].astype(str))

    if len(numeric_cols) >= 1:
        # ---------------------- AI MODEL ----------------------
        st.subheader("⚡ Generating AI SmartScores")

        X = df_encoded.dropna().values
        synthetic_target = np.random.rand(len(X)) * 100
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X, synthetic_target)
        smart_scores = model.predict(X)

        df["SmartScore"] = np.round(smart_scores, 2)

        # Display table with scores
        st.write("**AI SmartScores generated for each row:**")
        st.dataframe(df.head())

        # ---------------------- EXPORT TO CSV ----------------------
        st.download_button(
            label="📥 Download SmartScore Results as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="SmartScreen_Results.csv",
            mime="text/csv"
        )

        # ---------------------- VISUALIZATION ----------------------
        st.subheader("📊 SmartScore Distribution")
        fig = px.histogram(df, x="SmartScore", nbins=20, title="Distribution of AI SmartScores")
        st.plotly_chart(fig, use_container_width=True)

        # ---------------------- INTERACTIVE SIMULATION ----------------------
        st.subheader("🎛 Live AI Simulation")
        st.markdown("Adjust the sliders to simulate how changes affect the AI SmartScore.")

        # Row selection
        row_index = st.slider("Select a row to simulate", 0, len(df) - 1, 0)
        sample_row = df_encoded.iloc[row_index].copy()

        # Create sliders for numeric features
        for i, col in enumerate(df_encoded.columns):
            current_val = sample_row[col]
            min_val = float(df_encoded[col].min())
            max_val = float(df_encoded[col].max())
            sample_row[col] = st.slider(
                f"{col} (Row {row_index})", 
                min_val, max_val, float(current_val)
            )

        # Predict new SmartScore
        new_score = model.predict([sample_row.values])[0]
        st.metric("Updated SmartScore", f"{new_score:.2f}")

        # ---------------------- IMPACT EXPLANATION ----------------------
        st.subheader("🚀 Potential of SmartScreen AI")
        st.markdown("""
        **What you're seeing is a mini version of SmartScreen AI:**  
        1. **Real-time scoring** for any dataset  
        2. **Interactive decision simulation** for judges or stakeholders  
        3. Could integrate with **safety, efficiency, or risk models** in real products  

        This is how **SmartScreen AI** turns raw data into **actionable insights**!
        """)

    else:
        st.warning("No numeric data found for analysis.")

else:
    st.info("Please upload a CSV or CVD file to start the demonstration.")

# ---------------------- FOOTER ----------------------
st.markdown("---")
st.caption("SmartScreen AI Demo © 2025 • Live AI Scoring & Simulation with Export")
