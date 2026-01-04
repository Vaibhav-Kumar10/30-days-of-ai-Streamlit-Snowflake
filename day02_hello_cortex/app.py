### 1. Import Libraries and connect to Snowflake
import streamlit as st
# Imports the specific Cortex AI function ai_complete
from snowflake.snowpark.functions import ai_complete 
import json

st.title(":material/smart_toy: Hello, Cortex!")

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()


### 2. Set Up the AI Model and UI
ai_model = "claude-3-5-sonnet"
user_prompt = st.text_input("Enter your prompt: ")


### 3. Run LLM inference on Button Click
if st.button("Generate Response."):
    # Create a single-cell spreadsheet to run a function and capture its output
    # Then store the result in a Snowpark DataFrame - df
    df = session.range(1).select(
        ai_complete(model=ai_model, prompt=user_prompt).alias("Response")
    )
    # .alias() rename the ouput column from ai_complete function to "Response"

    ## Get and display response
    raw_response = df.collect()[0][0]
    # .collect() command is used to execute the query in Snowflake 
    # and then it pulls the data from the DataFrame, df, back into the app
    
    response = json.loads(raw_response)
    
    st.success("Successfully recieved response!!")

    st.write(response)
    

# Footer
st.divider()
st.caption("Day 2: Hello, Cortex!! | 30 Days of AI")