import streamlit as st
import pandas as pd
import urllib.request
import os # Needed for file cleanup
# Assuming data_setup.py is available with the load_and_clean_data function
from data_setup import load_and_clean_data 

st.set_page_config(
    page_title="Data Analysis App", 
    layout="wide"
)

st.title("🏡 Copenhagen Airbnb Data Exploration")
st.markdown("### 🇩🇰 Automatically Loading the Latest Listings Data (June 2025)")

# --------------------------------
# --- Data Source Configuration ---
# --------------------------------
DATA_URL = "https://data.insideairbnb.com/denmark/hovedstaden/copenhagen/2025-06-27/data/listings.csv.gz"
DATA_FILENAME = "listings.csv.gz"


# --------------------------------
# 1️⃣ Data Loading and Preprocessing
# --------------------------------

# Check if data is already loaded into session state to prevent re-download on every interaction
if 'DF' not in st.session_state:
    st.info(f"Downloading and processing the Copenhagen Airbnb dataset from {DATA_URL}...")
    
    # Use a placeholder container to display the initial loading message cleanly
    placeholder = st.empty()
    
    with placeholder.container():
        with st.spinner(f"Downloading {DATA_FILENAME}..."):
            try:
                # 1. Download the file
                urllib.request.urlretrieve(DATA_URL, DATA_FILENAME)

                # 2. Load raw data from the downloaded file
                df_raw = pd.read_csv(DATA_FILENAME, compression='infer', low_memory=False)

                # 3. Clean and structure data
                with st.spinner("Cleaning and structuring data..."):
                    # This function is imported from data_setup and handles transformation
                    df, numerical_cols, categorical_cols = load_and_clean_data(df_raw)
                
                # 4. Store Data in Session State
                st.session_state['DF'] = df
                st.session_state['NUMERICAL_COLS'] = numerical_cols
                st.session_state['CATEGORICAL_COLS'] = categorical_cols

                st.success("Dataset loaded and processed successfully! Use the sidebar navigation to explore.")

            except Exception as e:
                placeholder.empty() # Clear success/loading message
                st.error(f"Error processing data from URL. Please check connection and URL: {e}")
                st.stop()
            finally:
                # Clean up the downloaded file after loading it into the DataFrame
                if os.path.exists(DATA_FILENAME):
                    os.remove(DATA_FILENAME)
                    
    placeholder.empty() # Clear the initial message/spinner area completely

# --------------------------------
# 2️⃣ Analysis and Display (Only run if data is available)
# --------------------------------

if 'DF' in st.session_state:
    # Access the variables from session state
    DF = st.session_state['DF']
    NUMERICAL_COLS = st.session_state['NUMERICAL_COLS']
    CATEGORICAL_COLS = st.session_state['CATEGORICAL_COLS']
    
    st.markdown("---")
    
    # --------------------------------
    # 2️⃣ Missing Values Per Column
    # --------------------------------
    st.subheader("Missing Value Summary")
    # Missing values check on the *cleaned* dataframe (DF)
    missing_data = DF.isnull().sum()
    missing_data = missing_data[missing_data > 0].sort_values(ascending=False)

    if not missing_data.empty:
        st.warning(f"Found **{len(missing_data)}** columns with partial missing data in the processed dataset:")
        missing_percentage = (missing_data / len(DF)) * 100
        missing_df = pd.DataFrame({
            'Missing Count': missing_data,
            'Missing Percentage (%)': missing_percentage.round(2)
        })
        # Display the missing values summary using an interactive table
        st.dataframe(missing_df, use_container_width=True)
    else:
        st.success("No partial missing values found in the remaining columns! 🎉")

    # --------------------------------
    # 3️⃣ Data Summary and Preview
    # --------------------------------
    st.subheader("Processed Data Preview")
    st.dataframe(DF.head(), use_container_width=True)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Rows", f"{len(DF):,}")
    col2.metric("Total Features", len(DF.columns))
    st.info(
        f"Numerical Variables: **{len(NUMERICAL_COLS)}** | "
        f"Categorical Variables: **{len(CATEGORICAL_COLS)}**"
    )

else:
    # Fallback if initial load failed (e.g., due to network error)
    st.error("The required dataset could not be loaded from the external URL.")
    # Ensure session state is clean if a failure occurred
    if 'DF' in st.session_state: del st.session_state['DF']
