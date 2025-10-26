import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- 0️⃣ Data Setup and Retrieval ---

st.set_page_config(layout="wide")

# Retrieve variables from Session State
if 'DF' not in st.session_state or 'NUMERICAL_COLS' not in st.session_state:
    st.warning("⚠️ Data not initialized. Please go back to the main page to load the data.")
    st.stop() 

# Assign variables from session state
DF = st.session_state['DF']
NUMERICAL_COLS = st.session_state['NUMERICAL_COLS']

st.title("📊 Correlation Matrix Analysis")
st.markdown("### Visualize the linear relationships between numerical variables.")

# -------------------------
# 1️⃣ Sidebar: Select numerical features
# -------------------------
st.sidebar.title("Correlation Options")

# Set a reasonable default (e.g., the first 8 numerical columns)
default_corr_cols = NUMERICAL_COLS[:8] if len(NUMERICAL_COLS) >= 8 else NUMERICAL_COLS

selected_features = st.sidebar.multiselect(
    "Choose numerical features for the Matrix",
    options=NUMERICAL_COLS,
    default=default_corr_cols
)

# -------------------------
# 2️⃣ Generate and Plot Correlation Matrix
# -------------------------

if not selected_features:
    st.warning("👈 Please select at least two numerical features to generate the correlation matrix.")
elif len(selected_features) < 2:
    st.warning("Please select at least two features to calculate correlation.")
else:
    st.subheader(f"Correlation Matrix for {len(selected_features)} Selected Features")

    corr_matrix = DF[selected_features].corr()

    size = max(8, len(selected_features) * 0.8)
    
    fig, ax = plt.subplots(figsize=(size, size))
    
    sns.heatmap(
        corr_matrix, 
        annot=True,              
        cmap='coolwarm',         
        fmt='.2f',               
        linewidths=.5,           
        cbar_kws={'label': 'Correlation Coefficient'}, 
        ax=ax
    )
    
    ax.set_title('Correlation Matrix of Selected Numerical Features', fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    st.pyplot(fig)
    plt.close(fig)
    
    st.caption("Correlation values range from -1 (perfect negative correlation) to +1 (perfect positive correlation).")
