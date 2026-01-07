### 1. Setup and Snowflake Cortex AI Function
import streamlit as st
import json
from snowflake.snowpark.functions import ai_complete

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowpark.snowflake import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# Defining the Cortex LLM Call function
def call_vertex_llm(user_prompt_text):
    '''
    Make a call to Cortex AI with the given user prompt.
    '''
    llm_model = "claude-3-5-sonnet"
    df = session.range(1).select(
        ai_complete(
            model=llm_model,
            prompt=user_prompt_text,
        ).alias('response')
    )
    ## Get and display response
    raw_response = df.collect()[0][0]
    json_response = json.loads(raw_response)
    return json_response

# Cached LLM Function
@st.cache_data
def cached_cortex_response(prompt_text):
    return call_vertex_llm(prompt_text)


### 2. Building the Streamlit UI and User Input
st.title(":material/post: LinkedIn Post Generator")

# Input Widgets
# It creates a text field
content = st.text_area("CONTENT URL: ", "https://docs.snowflake.com/en/user-guide/views-semantic/overview")

# It provides a dropdown menu 
tone = st.selectbox("TONE: ", ["Professional", "Natural", "Casual", "Funny", "Simple"])

# It provides a slider
word_count = st.slider("Approximate WORD COUNT: ", 50, 300, 100)

# Generate button
if st.button("Generate Post"):

### 3. Prompt Construction and Output Display
    # Construct the prompt
    prompt = f"""
    You are an expert social media manager. Generate a LinkedIn post based on the following:

    Tone: {tone}
    Desired Length: Approximately {word_count} words
    Use content from this URL: {content}

    Generate only the LinkedIn post text. Use dash for bullet points.
    """
    response = cached_cortex_response(prompt)
    st.subheader("Generated Post:")
    st.markdown(response)


# Footer
st.divider()
st.caption("Day 5: LinkedIn Post Generator | 30 Days of AI")
