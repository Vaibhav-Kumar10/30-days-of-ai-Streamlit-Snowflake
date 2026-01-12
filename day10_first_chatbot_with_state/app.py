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
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

def call_llm(prompt_text: str) -> str:
    """Call Snowflake Cortex LLM."""
    df = session.range(1).select(
        ai_complete(model="claude-3-5-sonnet", prompt=prompt_text).alias("response")
    )
    response_raw = df.collect()[0][0]
    response_json = json.loads(response_raw)
    # Extract text from response
    if isinstance(response_json, dict):
        return response_json.get("choices", [{}])[0].get("messages", "")
    return str(response_json)

st.title(":material/chat: My First Chatbot")

### 1. Initialize Message Storage using the messages list in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

### 2. Display Chat History
# Display all messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

### 3. Handle New Messages
# Chat input
# := Walrus Operator 
# This assigns the input value to prompt and checks if it's not empty in one line.
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    ### 4. Generate and Store Response
    # Generate and display assistant response
    with st.chat_message("assistant"):
        response = call_llm(prompt)
        st.write(response)
    
    # Add assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.caption("Day 10: Your First Chatbot (with State) | 30 Days of AI")