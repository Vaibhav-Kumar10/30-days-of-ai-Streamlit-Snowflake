import streamlit as st

st.title(":material/chat: Meet the Chat Elements")


### 1. Visualizing Static Messages
# It creates the message container, for role - USER.
with st.chat_message("USER"):
    st.write("Hello! Can you explain what Streamlit is?")

# It creates the message container, for role - ASSISTANT.
with st.chat_message("ASSITANT"):
    st.write("Streamlit is an open-source Python framework for building data apps.")
     
    # We can create chat bubbles which can contain rich media, like charts inside chat messages!
    st.bar_chart([10, 20, 30, 40]) 


### 2. The Chat Input Widget
# It creates a text entry box pinned to the bottom of the screen.
# It stores the string the user has typed, and None until the user hits "Enter."
user_prompt = st.chat_input("Type a message here...")


### 3. Reacting to Input (The "Glitchy" Loop)
# It ensures that this code runs only after the user submits text.
if user_prompt:
    # Display the user's new message
    with st.chat_message("USER"):
        st.write(user_prompt)
    
    # Display a mock assistant response
    with st.chat_message("assistant"):
        st.write(f"You just said:\n\n'{user_prompt}'\n\n(I don't have memory yet!)")


# Footer
st.divider()
st.caption("Day 8: Meet the Chat Elements | 30 Days of AI")