### 1. Import Libraries and connect to Snowflake
import streamlit as st
import time
import json
from snowflake.snowpark.functions import ai_complete

st.title(":material/cached: Caching your App")

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except Exception:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(
        st.secrets["connections"]["snowflake"]
    ).create()


### 2. Defining the Cortex LLM Call function
def call_vertex_llm(user_prompt_text):
    llm_model = "claude-3-5-sonnet"
    df = session.range(1).select(
    # Create a single-cell spreadsheet to run a function and capture its output
    # Then store the result in a Snowpark DataFrame - df
        ai_complete(model=llm_model, prompt=user_prompt_text).alias("response")
    )
    # .alias() rename the ouput column from ai_complete function to "Response"

    ## Get and display response
    raw_response = df.collect()[0][0]
    # .collect() command is used to execute the query in Snowflake 
    # and then it pulls the data from the DataFrame, df, back into the app
    json_response = json.loads(raw_response)
    return json_response

# It is used to cache the prompt sent to llm call. 
# If user submits the same prompt again, immediately then it returns the same saved answer
@st.cache_data
def cached_cortex_response(prompt_text):
    return call_vertex_llm(prompt_text)


### 3. Building the Web App Interface
user_prompt_text = st.text_area("Enter your prompt", "Why is the sky blue?")
if st.button("SUBMIT"):
    starting_time = time.time()
    # response = call_vertex_llm(user_prompt_text)
    response = cached_cortex_response(user_prompt_text)
    ending_time = time.time()

    st.success(f"*The call took {ending_time-starting_time:0.3f} seconds.")
    st.write(response)


# Footer
st.divider()
st.caption("Day 4: Caching your App | 30 Days of AI")
