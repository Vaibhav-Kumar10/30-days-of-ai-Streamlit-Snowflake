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
st.title(":material/post: LinkedIn Post Generator v2")
## Input Widgets
    # It creates a text field
content = st.text_area("CONTENT URL: ", "https://docs.snowflake.com/en/user-guide/views-semantic/overview")
    # It provides a dropdown menu 
tone = st.selectbox("TONE: ", ["Professional", "Natural", "Casual", "Funny", "Simple"])
    # It provides a slider
word_count = st.slider("Approximate WORD COUNT: ", 50, 300, 100)


### 3. Execution and Status Management
if st.button("Generate Post"):
    ## Initialize the status container
        # It creates a container to provide a visual feedback (like a spinner) to the user 
        # while the AI is processing. This prevenst the app from looking "frozen."
    with st.status("Starting the engine...", expanded=True) as status:
        
        # Step 3.1: Construct the Prompt
        st.write(":material/psychology: Thinking: Analyzing constraints and tone...")
        prompt = f"""
        You are an expert social media manager. Generate a LinkedIn post based on the following:

        Tone: {tone}
        Desired Length: Approximately {word_count} words
        Use content from this URL: {content}

        Generate only the LinkedIn post text. Use dash for bullet points.
        """
        
        # Step 3.2: Call API
        st.write(":material/flash_on: Generating: contacting Snowflake Cortex...")

        # This is the blocking call that takes time
        response = cached_cortex_response(prompt)

        # Step 3.3: Update Status to Complete
        st.write(":material/check_circle: Post generation completed!")
        status.update(label="Post Generated Successfully!", state="complete", expanded=False)

    # Display Result
    st.subheader("Generated Post:")
    st.markdown(response)


# Footer
st.divider()
st.caption("Day 6: LinkedIn Post Generator v2 | 30 Days of AI")
