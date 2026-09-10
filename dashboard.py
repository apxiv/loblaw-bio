import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DB_FILE = "cell_count.db"
PLOT_FILE = "response_boxplots.png"

st.set_page_config(page_title="Loblaw Bio", layout="wide")
st.title("Loblaw Bio trial dashboard")

if not Path(DB_FILE).exists():
    st.error("Database not found. Run `make pipeline` first.")
    st.stop()

conn = sqlite3.connect(DB_FILE)

part2, part3, part4 = st.tabs(
    [
        "Part 2: Cell frequencies",
        "Part 3: Responders vs non-responders",
        "Part 4: Baseline subset",
    ]
)

with part2:
    st.subheader("Relative frequency of each cell type in each sample")
    sample_id = st.text_input("Filter by sample id")
    query = "SELECT sample, total_count, population, count, percentage FROM population_frequencies"
    if sample_id:
        frequencies = pd.read_sql_query(query + " WHERE sample = ?", conn, params=(sample_id,))
    else:
        frequencies = pd.read_sql_query(query, conn)
    st.dataframe(frequencies, width="stretch")

with part3:
    st.subheader("Melanoma patients on miraclib (PBMC only)")
    if Path(PLOT_FILE).exists():
        st.image(PLOT_FILE)
    comparison = pd.read_sql_query("SELECT * FROM response_comparison", conn)
    st.dataframe(comparison, width="stretch")
    st.caption("Mann-Whitney U p-values. Below 0.05 is usually called significant.")

with part4:
    st.subheader("Melanoma PBMC samples at day 0 on miraclib")
    counts = pd.read_sql_query("SELECT * FROM subset_counts", conn)
    samples = pd.read_sql_query("SELECT * FROM subset_samples", conn)
    st.dataframe(counts, width="stretch")
    st.dataframe(samples, width="stretch")

conn.close()
