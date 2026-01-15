import streamlit as st
import json
from snowflake.snowpark.functions import ai_complete
import time

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


st.title(":material/chat: CUSTOMIZABLE Chatbot")


### 1. Initialize System Prompt and Messages Early
# Set up both before we create the sidebar widget
# 1.1 Initialize system prompt if not exists
if "system_prompt" not in st.session_state.messages:
    st.session_state.system_prompt = "You are a helpful pirate assistant named Captain Starlight. You speak with pirate slang, use nautical metaphors, and end sentences with 'Arrr!' when appropriate. Be helpful but stay in character."

# 1.2 Initialize messages with a personality-appropriate greeting
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ahoy! Captain Starlight here, ready to help ye navigate the high seas of knowledge! Arrr!",
        }
    ]


### 2. Preset Personality Buttons (at the top)
# Preset buttons are placed at the top for better UX - users see presets before the text area.

# Sidebar configuration
with st.sidebar:
    st.header(":material/theater_comedy: Bot Personality")
    # Preset personalities
    st.subheader("Quick Presets")
    column1, column2 = st.columns(2)
    with column1:
        if st.button(":material/sailing: Pirate"):
            st.session_state.system_prompt = "You are a helpful pirate assistant named Captain Starlight. You speak with pirate slang, use nautical metaphors, and end sentences with 'Arrr!' when appropriate."
            st.rerun()
    with column2:
        if st.button(":material/smart_toy: Robot"):
            st.session_state.system_prompt = "You are UNIT-7, a helpful robot assistant. You speak in a precise, logical manner. You occasionally reference your circuits and processing units."
            st.rerun()

    column3, column4 = st.columns(2)
    with column3:
        if st.button(":material/mood: Comedian"):
            st.session_state.system_prompt = "You are Chuckles McGee, a witty comedian assistant. You love puns, jokes, and humor, but you're still genuinely helpful. You lighten the mood while providing useful information."
            st.rerun()
    with column4:
        if st.button(":material/school: Teacher"):
            st.session_state.system_prompt = "You are Professor Ada, a patient and encouraging teacher. You explain concepts clearly, use examples, and always check for understanding."
            st.rerun()

    ### 3. The System Prompt Text Area (below presets)
    st.divider()
    st.text_area("System Prompt:", height=250, key="system_prompt")
    st.divider()

    # Conversation stats
    st.header("Conversation Stats")
    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    assistant_msgs = len(
        [m for m in st.session_state.messages if m["role"] == "assistant"]
    )
    st.metric("Your Messages", user_msgs)
    st.metric("AI Responses", assistant_msgs)

    # Clear History Button
    if st.button("Clear History"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Ahoy! Captain Starlight here, ready to help ye navigate the high seas of knowledge! Arrr!",
            }
        ]
        st.rerun()


# Display all messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
if user_prompt := st.chat_input("Type your message..."):
    # Add and display the user's message to the session state
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    # Generate and display assistant response with streaming
    with st.chat_message("assistant"):
        ### 4. Injecting the System Prompt with Streaming
        # Custom generator for reliable streaming
        def stream_generator():
            # Build the full conversation history for context
            conversation_history = "\n\n".join(
                [
                    f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                    for msg in st.session_state.messages
                ]
            )
            # Create prompt with system instruction
            full_user_prompt = f"""
                {st.session_state.system_prompt}
Here is the conversation so far:
{conversation_history}

Respond to the user's latest message while staying in character.
            """
            response_text = call_llm(full_user_prompt)
            for word in response_text.split(" "):
                yield word + " "
                time.sleep(0.02)

        with st.spinner("Processing..."):
            response = st.write_stream(stream_generator)

    # Add assistant's response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()  # Force rerun to update sidebar stats


st.divider()
st.caption("Day 13: Adding a System Prompt | 30 Days of AI")
