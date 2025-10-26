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

# Create the subset DataFrame
df_numerical = DF[NUMERICAL_COLS]

st.title("📈 Numerical Variable Analysis")

# -------------------------
# 1️⃣ Sidebar: Select numerical columns
# -------------------------

st.sidebar.title("Numerical Plot Options")

default_cols = NUMERICAL_COLS[:5] if len(NUMERICAL_COLS) >= 5 else NUMERICAL_COLS

selected_cols = st.sidebar.multiselect(
    "1. Choose numerical variables to plot",
    options=NUMERICAL_COLS,
    default=default_cols
)

# ----------------------------------------------------
# 2️⃣ Numerical Summary Statistics
# ----------------------------------------------------
st.header("Summary Statistics of Numerical Variables")
st.markdown("This table provides descriptive statistics (mean, standard deviation, min/max, quartiles) for all numerical features.")
# Use .T to transpose the DataFrame for a better vertical view in Streamlit
st.dataframe(df_numerical.describe().T, use_container_width=True)


# ----------------------------------------------------
# 3️⃣ Plot Boxplots Separately with INDIVIDUAL X-Axis Filters
# ----------------------------------------------------

st.header("Individual Boxplots of Selected Numerical Variables")

if not selected_cols:
    st.warning("Please select at least one numerical variable to display the plot.")
else:
    if len(selected_cols) > 15:
        st.info("Displaying the first 15 selected variables.")
        selected_cols = selected_cols[:15]
        
    cols = st.columns(2)
    col_index = 0
    
    for variable in selected_cols:
        with cols[col_index % 2]:
            st.subheader(f"Distribution: **{variable}**")
            
            # --- INDIVIDUAL X-AXIS FILTER SETUP ---
            # Calculate the true min/max for the current variable
            data_series = df_numerical[variable].dropna()
            
            # Use max/min for the current variable
            min_var_val = data_series.min()
            max_var_val = data_series.max()

            # Cap the max value for better slider usability, ensuring it's never less than the min
            max_val_safe = max(max_var_val, min_var_val + 1) if not pd.isna(max_var_val) else 10000
            if max_val_safe > 10000:
                 max_val_safe = 10000 
            
            # Ensure proper float types for the slider inputs
            min_f = float(min_var_val) if not pd.isna(min_var_val) else 0.0
            max_f = float(max_val_safe)

            # Create the unique slider for this variable
            current_value_range = st.slider(
                f'Select X-Axis Range for **{variable}**',
                min_f,
                max_f,
                (min_f, max_f),
                # Set a reasonable step, ensuring it's not zero if min_f == max_f
                step=max(1.0, (max_f - min_f) / 100) if max_f > min_f else 1.0,
                key=f'slider_{variable}' # Crucial for Streamlit to recognize unique widgets
            )
            
            # --- PLOTTING LOGIC ---
            
            # Apply the filter based on the variable's unique slider values
            data_filtered = data_series[
                (data_series >= current_value_range[0]) & 
                (data_series <= current_value_range[1])
            ]
            
            if data_filtered.empty:
                 st.info("No data points fall within the selected X-axis range for this variable.")
                 col_index += 1
                 continue
            
            # Create a Matplotlib figure
            fig, ax = plt.subplots(figsize=(10, 4))
            
            # Create the boxplot using the filtered data
            sns.boxplot(x=data_filtered, ax=ax)
            
            ax.set_title(f"Boxplot of {variable}", fontsize=14)
            ax.set_xlabel(variable)
            ax.set_yticks([]) 
            
            # Explicitly set the x-axis limits to match the variable's slider for consistent viewing
            ax.set_xlim(current_value_range) 
            
            st.pyplot(fig)
            plt.close(fig)
            
        col_index += 1
