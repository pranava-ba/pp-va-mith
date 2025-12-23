# pages/stats.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Rating Statistics")
st.markdown("""
    <style>.stApp { background-color: #0E1117; color: #FAFAFA; }</style>
""", unsafe_allow_html=True)

st.title("📊 Rating Statistics")

DATA_FILE = "../specimen_data.csv"  # Relative path to main dir

if not os.path.exists(DATA_FILE):
    st.warning("No data found. Add entries on the main page.")
    st.stop()

df = pd.read_csv(DATA_FILE)

if df.empty:
    st.warning("No data available.")
    st.stop()

# Add specimen numbers
df_display = df.copy()
df_display['Specimen number'] = range(1, len(df) + 1)
df_display['Avg Rating'] = df[['Nithin', 'Mithra', 'Pranava']].mean(axis=1)

# ... [rest of stats code remains same as before] ...
# (Use df instead of session_state.df)
# (All calculations now use the loaded CSV data)
