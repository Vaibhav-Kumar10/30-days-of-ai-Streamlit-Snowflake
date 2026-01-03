### 1. Import Libraries
import streamlit as st

### 2. Connect to Snowflake
# Auto-detect environment and connect
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

st.title("Day 1: Connect to Snowflake")

### 3. Query Snowflake Version
snowflake_version = session.sql("SELECT CURRENT_VERSION()").collect()[0][0]

### 4. Display Results
st.success(f"Successfully connected!! Snowflake Version: {snowflake_version}")
