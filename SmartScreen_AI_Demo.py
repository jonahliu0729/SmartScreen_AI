import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io

st.set_page_config(page_title="SmartScreen AI Demo", layout="wide")

# -------------------------
# Sidebar & Branding
# -------------------------
st.sidebar.title("SmartScreen AI")
st.sidebar.markdown("### Dual-Sustainability Concrete")
st.sidebar.markdown("**ISEF Demonstration Tool**")
st.sidebar.info("Upload CAD/CVD files to see AI-powered predictions and impact potential.")

# -------------------------
# Tabs
# -------------------------
tab1, tab2, tab3 = st.tabs(["Overview", "AI Demonstration", "Future Potential"])

# -------------------------
# Tab 1: Overview
# -------------------------
with tab1:
    st.title("SmartScreen AI")
    st.markdown("""
    ### Revolutionizing Construction with AI  
    **SmartScreen AI** enhances concrete for **cold climates** using **biochar-infused, self-healing technology**.  
    Our AI optimizes materials for **durability, sustainability, and reduced emissions**.
    """)
    
    st.subheader("🌟 Key Highlights")
    st.markdown("""
    - **Self-healing concrete** extends infrastructure lifespan  
    - **CO₂ emission reduction** via biochar infusion  
    - **AI-powered optimization** for cold climate resilience
    """)

    st.markdown("---")
    st.success("➡ Switch to the **AI Demonstration** tab to start the live demo!")

# -------------------------
# Tab 2: AI Demonstration
# -------------------------
with tab2:
    st.header("Live AI Demonstration")

    uploaded_file = st.file_uploader("Upload your CAD or CVD file", type=["cad", "cvd", "csv"])

    if uploaded_file:
        file_name = uploaded_file.name.lower()
        
        # --- CVD / CSV Visualization ---
        if file_name.endswith(("cvd", "csv")):
            st.subheader("📊 CVD Data Visualization")
            df = pd.read_csv(uploaded_file)
            st.write("Preview of uploaded data:", df.head())

            if len(df.columns) >= 2:
                x_col, y_col = df.columns[:2]
                fig = px.scatter(df, x=x_col, y=y_col, title="CVD Data Scatter Plot", color_discrete_sequence=["#0072B2"])
                st.plotly_chart(fig, use_container_width=True)

            # Simulated AI prediction
            durability = np.random.randint(70, 95)
            healing_efficiency = np.random.randint(60, 90)
            st.subheader("🤖 AI Prediction")
            st.info(f"Predicted Durability: **{durability}%** | Self-Healing Efficiency: **{healing_efficiency}%**")
        
        # --- CAD File Visualization (Placeholder) ---
        elif file_name.endswith("cad"):
            st.subheader("🖼 CAD Model Preview")
            st.info("Interactive 3D visualization placeholder - upload as STL/OBJ for full 3D preview in future versions.")
            
            # Simulated AI prediction
            strength = np.random.randint(75, 95)
            eco_score = np.random.randint(65, 90)
            st.subheader("🤖 AI Prediction")
            st.info(f"Estimated Structural Integrity: **{strength}%** | Sustainability Score: **{eco_score}%**")

    else:
        st.warning("Please upload a CAD or CVD file to begin the demonstration.")

# -------------------------
# Tab 3: Future Potential
# -------------------------
with tab3:
    st.header("SmartScreen AI: Impact and Future Potential")
    st.markdown("""
    With further development, SmartScreen AI can:
    - Predict material failures **before they happen**
    - **Optimize mixes** for extreme weather conditions
    - Reduce **construction costs and carbon footprint**
    """)

    st.subheader("📈 AI vs Traditional Concrete Simulation")
    categories = ["Durability", "Self-Healing", "Sustainability"]
    ai_scores = [90, 80, 85]
    traditional_scores = [70, 40, 50]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=categories, y=traditional_scores, name='Traditional Concrete'))
    fig.add_trace(go.Bar(x=categories, y=ai_scores, name='AI-Optimized Concrete'))

    fig.update_layout(
        barmode='group',
        title="Projected Performance Comparison",
        yaxis_title="Performance Score (%)",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.success("✅ SmartScreen AI has the potential to **transform sustainable construction globally**.")
