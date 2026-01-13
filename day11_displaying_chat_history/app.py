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


st.title(":material/chat: Chatbot with HISTORY!!")


### 1. Initialze the Message Storage, with a Welcome Message, using the messages list in session state
# It ensures that we initialize the list only once,
# only when the app first starts, not everytime
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm your AI assistant. How can I help you today?",
        }
    ]

### 2. Sidebar Statistics and Controls
with st.sidebar:
    st.header("Conversation Stats")
    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    assistant_msgs = len(
        [m for m in st.session_state.messages if m["role"] == "assistant"]
    )
    st.metric("Your Messages", user_msgs)
    st.metric("AI Responses", assistant_msgs)

    ### 3. Clear History Button
    if st.button("Clear History"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I'm your AI assistant. How can I help you today?",
            }
        ]
        # It forces the app to rerun immediately.
        # Thus refreshing the display to show the cleared state.
        st.rerun()


### 4. Enhanced Message Display
# Loop through every message stored in the session state, and display them
for message in st.session_state.messages:
    # Create a chat bubble based on the stored role
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
# Walrus operator handles input and checl if it's not empty, all in a single line
if user_prompt := st.chat_input("Type your message..."):
    # Add and Display the user's message to the session state
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):

        ### 5. Adding a Loading Indicator with st.spinner
        with st.spinner("Thinking..."):

            ### 6. Passing Conversation History to the LLM
            # Build the full conversation history for context
            conversation_history = "\n\n".join(
                [
                    f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                    for msg in st.session_state.messages
                ]
            )
            full_user_prompt = f"{conversation_history}\n\nAssistant:"
            response = call_llm(full_user_prompt)

        st.markdown(response)

    # Add assistant's response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})

    ### 7. Updating Sidebar Stats with st.rerun()
    st.rerun()


st.divider()
st.caption("Day 11: Displaying Chat History | 30 Days of AI")
