import pandas as pd

# NOTE: The @st.cache_data, urllib, and os imports are REMOVED here.

def load_and_clean_data(df_raw):
    """Cleans and categorizes a raw DataFrame input."""
    
    df = df_raw.copy()
        
    # 1. Drop columns with all missing values
    df = df.dropna(axis='columns', how='all')
    
    # 2. Select numerical columns and filter out 'id' columns
    numerical_cols = df.select_dtypes(include=['number']).columns
    numerical_cols_filtered = [
        col for col in numerical_cols 
        if "id" not in col.lower()
    ]
    
    # 3. Select categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    return df, numerical_cols_filtered, categorical_cols

# NOTE: No function call or variable assignments at the top level.