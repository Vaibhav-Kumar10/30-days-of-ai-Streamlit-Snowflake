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


def call_llm(user_prompt_text: str) -> str:
    """
    Call Snowflake Coretx LLM.
    """
    df = session.range(1).select(
        ai_complete(model="claude-3-5-sonnet", prompt=user_prompt_text).alias(
            "response"
        )
    )
    raw_response = df.collect()[0][0]
    json_response = json.loads(raw_response)

    # Extract text from response
    if isinstance(json_response, dict):
        return json_response.get("choices", [{}])[0].get("messages", "")
    return str(json_response)


st.title(":material/chat: My First CHATBOT!!")


### 1. Initialze the Message Storage using the messages list in session state
# It ensures that we initialize the list only once,
# only when the app first starts, not everytime
if "messages" not in st.session_state:
    st.session_state.messages = []
# For this we have created an empty list to store our conversations.
# In this list we will hold the dict with
# - "roles" - user / assistant, and
# - "content" - the message list
# [{"role":"user", "content":"the text question"}, {"role":"assistant","content":"the response"}]


### 2. Display the Chat History
# Loop through every message stored in the session state, and display them
for message in st.session_state.messages:
    # Create a chat bubble based on the stored role
    with st.chat_message(message["role"]):
        st.write(message["content"])


### 3. Handle New Messages
# Chat input
# Walrus operator handles input and checl if it's not empty, all in a single line
if user_prompt := st.chat_input("What would you like to know??"):
    # Add the user's message to the session state
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Display user message
    with st.chat_message("user"):
        st.write(user_prompt)

    ### 4. Generate and Store Response
    with st.chat_message("assitant"):
        response = call_llm(user_prompt)
        st.write(response)

    # Add assistant's response to session state
    st.session_state.messages.append({"role": "assitant", "content": response})


st.divider()
st.caption("Day 10: Your First Chatbot (with State) | 30 Days of AI")
