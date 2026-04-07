import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

DB_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@db:3306/fraud_db")
engine = create_engine(DB_URL)

st.set_page_config(page_title="Fraud Monitor", layout="wide")
st.title("🛡️ Fraud Detection Real-Time Dashboard")

if st.sidebar.button('Refresh'):
    st.rerun()

try:
    df = pd.read_sql("SELECT * FROM transactions ORDER BY timestamp DESC", engine)
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total", len(df))
        c2.metric("Fraud", len(df[df['is_fraud'] == 1]))
        c3.metric("Avg Risk", f"{round(df['fraud_probability'].mean()*100, 2)}%")
        
        st.subheader("Live Transaction Feed")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Waiting for transactions...")
except Exception as e:
    st.error(f"Database connection error: {e}")