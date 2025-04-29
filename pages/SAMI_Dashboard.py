import streamlit as st
import pandas as pd
from utils.web_scraper import hybrid_scrape

st.title("Enterprise Reputation Analyzer")

company = st.text_input("Enter company name", "Secureonix")
max_results = st.slider("Number of posts/reviews", 5, 50, 10)

if st.button("Run Analysis") and company:
    with st.spinner("Scraping data, please wait..."):
        result_df = hybrid_scrape(company, max_results_per_source=max_results//4)
        if not result_df.empty:
            st.success(f"Found {len(result_df)} results for {company}! 🚀")
            st.dataframe(result_df)
        else:
            st.error("No data found. Try a different company or check naming.")
