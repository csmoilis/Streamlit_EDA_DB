import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 0️⃣ Data Setup and Retrieval ---

st.set_page_config(layout="wide")

if 'DF' not in st.session_state or 'CATEGORICAL_COLS' not in st.session_state:
    st.warning("⚠️ Data not initialized. Please go back to the main page to load the data.")
    st.stop() 

DF = st.session_state['DF']
CATEGORICAL_COLS = st.session_state['CATEGORICAL_COLS']

st.title("🏷️ Categorical Variable Analysis")
st.info("This section is dedicated to exploring the distribution of discrete variables.")

# -------------------------
# 1️⃣ Sidebar: Select categorical column
# -------------------------
st.sidebar.title("Categorical Plot Options")

selected_cat_col = st.sidebar.selectbox(
    "Choose one categorical variable",
    options=CATEGORICAL_COLS
)

# -------------------------
# 2️⃣ Plot Value Counts (UPDATED)
# -------------------------
if selected_cat_col:
    st.subheader(f"Frequency Distribution: `{selected_cat_col}`")
    
    # Calculate value counts, limiting to the top 8 and including a count of missing (NaN) values
    # If a variable has fewer than 8 categories, it will show all of them.
    # We use dropna=False to explicitly count missing values.
    counts_full = DF[selected_cat_col].value_counts(dropna=False)
    
    # --- LIMIT TO TOP 8 CATEGORIES ---
    # Handle the case where NaN might be included in the top 8
    counts = counts_full.head(8)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Top 8 Categories (Including Missing)**")
        # Rename the index for NaN values to make the DataFrame clearer
        counts_display = counts.rename(lambda x: 'Missing (NaN)' if pd.isna(x) else x)
        st.dataframe(counts_display)
        
        # Display the number of unique values for context
        num_unique = DF[selected_cat_col].nunique(dropna=False)
        st.caption(f"Total unique categories (including missing): **{num_unique}**")
        st.caption(f"Displaying **{len(counts_display)}** of the top categories.")

    with col2:
        # Create a bar plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot using the top 8 data
        sns.barplot(x=counts_display.index, y=counts_display.values, ax=ax, palette="viridis")
        
        ax.set_title(f"Count Plot of {selected_cat_col} (Top 8)", fontsize=16)
        ax.set_xlabel(selected_cat_col)
        ax.set_ylabel("Count")
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        st.pyplot(fig)
        plt.close(fig)