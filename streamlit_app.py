# streamlit_app.py
import streamlit as st
import pandas as pd
import os

# --- FORCE DARK THEME ---
st.set_page_config(page_title="Specimen Rating Tracker", layout="wide")
st.markdown("""
    <style>
        .stApp { background-color: #0E1117; color: #FAFAFA; }
        .stDataFrame th { background-color: #1A1E24 !important; color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# --- DATA PERSISTENCE: LOAD FROM CSV ---
DATA_FILE = "specimen_data.csv"
COLUMNS = ["Nithin", "Mithra", "Pranava", "comments"]

if os.path.exists(DATA_FILE):
    df_saved = pd.read_csv(DATA_FILE)
else:
    df_saved = pd.DataFrame(columns=COLUMNS)

# Store in session_state for easy access
if 'df' not in st.session_state:
    st.session_state.df = df_saved.copy()

# --- ADD ENTRY FUNCTION ---
def add_entry(input_str):
    if not input_str.strip():
        return "Please enter values"
    
    parts = input_str.split()
    if len(parts) < 3:
        return "Enter: Nithin Mithra Pranava [comments]"
    
    try:
        nithin = float(parts[0])
        mithra = float(parts[1])
        pranava = float(parts[2])
        
        if not all(0 <= x <= 10 for x in [nithin, mithra, pranava]):
            return "Ratings must be between 0 and 10"
        
        comments = " ".join(parts[3:]) if len(parts) > 3 else ""
        
        # Add to DataFrame
        new_row = pd.DataFrame([{
            "Nithin": nithin,
            "Mithra": mithra,
            "Pranava": pranava,
            "comments": comments
        }])
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
        
        # SAVE TO CSV IMMEDIATELY
        st.session_state.df.to_csv(DATA_FILE, index=False)
        return "✅ Entry saved!"
    except ValueError:
        return "❌ Invalid numbers. Use decimals like 8.5"

# --- UI ---
st.title("🔬 Specimen Rating Tracker")

input_str = st.text_input(
    "Enter ratings (Nithin Mithra Pranava [comments]):",
    placeholder="e.g., 6 5 4.4 cute specimen"
)

if st.button("Add Entry"):
    msg = add_entry(input_str)
    if "✅" in msg:
        st.success(msg)
    else:
        st.error(msg)

# --- DISPLAY TABLE ---
if not st.session_state.df.empty:
    display_df = st.session_state.df.copy()
    display_df.insert(0, 'Specimen number', range(1, len(display_df) + 1))
    st.subheader("Current Entries")
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("No entries yet. Add your first specimen!")

# --- NAV TO STATS ---
st.markdown("---")
if st.button("📊 View Statistics"):
    st.switch_page("pages/stats.py")
