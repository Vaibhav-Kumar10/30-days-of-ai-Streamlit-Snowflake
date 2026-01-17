# Day 14 – Adding Avatars and Error Handling

This project is part of the **#30DaysOfAI** challenge by Streamlit.

## Goal

Enhance the chatbot built in previous days by adding **visual personalization with avatars** and **robust error handling**, making the app more **production-ready and user-friendly**.

## What this app does

- Displays chat messages with customizable user and assistant avatars
- Streams AI responses word-by-word for a natural chat experience
- Handles LLM/API failures gracefully without crashing
- Allows users to simulate API errors for testing
- Maintains full conversation history
- Supports system prompt customization
- Displays conversation statistics in the sidebar
- Allows clearing chat history

## Tech Stack

- Python
- Streamlit
- Snowflake Snowpark
- Snowflake Cortex (LLM Inference)
- Claude 3.5 Sonnet

## Key Concepts: Avatars & Error Handling

### Avatars

Avatars improve UX by visually distinguishing:

- User messages
- Assistant responses

Streamlit’s `st.chat_message()` supports emojis, images, or URLs as avatars, enabling easy personalization.

### Error Handling

LLM APIs can fail due to:

- Rate limits
- Network issues
- Model overload
- Temporary service outages

This app uses structured `try/except` blocks to:

- Prevent crashes
- Inform users when something goes wrong
- Provide helpful recovery suggestions

## How it Works

### 1. Avatar Configuration

Users select avatars for both roles from the sidebar.

```python
user_avatar = st.selectbox("Your Avatar:", ["👤", "🧑‍💻", "👨‍🎓", "👩‍🔬", "🦸", "🧙"])
assistant_avatar = st.selectbox("Assistant Avatar:", ["🤖", "🧠", "✨", "🎯", "💡", "🌟"])
````

Avatars are applied dynamically to each chat message based on the role.

---

### 2. Displaying Messages with Avatars

```python
for message in st.session_state.messages:
    avatar = user_avatar if message["role"] == "user" else assistant_avatar
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
```

Each message automatically renders with the correct avatar.

---

### 3. Debug Mode to Simulate Errors

```python
simulate_error = st.checkbox("Simulate API Error", value=False)
```

This toggle allows developers to test error handling behavior without waiting for real API failures.

---

### 4. Error Handling with Streaming Responses

```python
try:
    if simulate_error:
        raise Exception("Simulated API error (429)")

    with st.spinner("Processing..."):
        response = st.write_stream(stream_generator)

    st.session_state.messages.append({"role": "assistant", "content": response})

except Exception as e:
    st.error(f"I encountered an error: {str(e)}")
    st.info("Try again in a moment or rephrase your question.")
```

- Errors are caught safely
- The app continues running
- Failed responses are not added to chat history

---

## Key Learning

Polish and reliability matter just as much as model quality.

By adding:

- Avatars → Better user experience
- Error handling → Production stability
- Debug tools → Easier testing

This chatbot now behaves like a **real-world AI application**, not just a demo.

## Screenshot

![Day 14 Output](<../screenshots/day14_success (1).png>)
![Day 14 Output](<../screenshots/day14_success (2).png>)
