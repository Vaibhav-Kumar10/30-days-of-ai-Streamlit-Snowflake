# Day 25 – Voice Interface

This project is part of the **#30DaysOfAI** challenge by Streamlit.

## Goal

Build a **voice-enabled conversational AI assistant** that can listen, understand, and respond — all powered by Snowflake Cortex.

## What this app does

- Allows users to record voice messages using a microphone
- Uploads audio securely to a Snowflake stage
- Transcribes speech using **Snowflake Cortex AI_TRANSCRIBE**
- Generates context-aware responses using an LLM
- Maintains full conversation history for natural dialogue
- Displays a persistent chat interface with voice-first interaction

## Tech Stack

- Python
- Streamlit
- Snowflake Snowpark
- Snowflake Cortex `AI_TRANSCRIBE`
- Snowflake Cortex `AI_COMPLETE`
- Claude 3.5 Sonnet

## Key Concept: Voice-First Conversational AI

This app demonstrates how to build **speech-based AI assistants** by combining:

- Audio input
- Speech-to-text transcription
- LLM-based response generation
- Conversation memory

Instead of typing, users interact naturally using voice — while the assistant remembers context across turns.

## How it Works

### 1. Voice Recording

- Users record audio using Streamlit’s `st.audio_input`
- Audio is captured as WAV bytes and hashed to prevent duplicate processing

### 2. Secure Audio Storage

- Audio files are uploaded to a Snowflake stage
- The stage is created with **server-side encryption (SNOWFLAKE_SSE)**, which is required for `AI_TRANSCRIBE`
- Each recording is stored with a unique timestamp-based filename

### 3. Speech-to-Text with AI_TRANSCRIBE

- The app calls `SNOWFLAKE.CORTEX.AI_TRANSCRIBE()` using the `TO_FILE()` syntax
- The returned JSON response is parsed to extract transcribed text

### 4. Context-Aware Response Generation

- Full conversation history is assembled into a structured prompt
- The prompt is sent to a Snowflake Cortex LLM (`claude-3-5-sonnet`)
- The assistant responds conversationally, referencing prior messages

### 5. Persistent Chat Interface

- Chat history is stored in Streamlit session state
- Messages are rendered using `st.chat_message`
- Conversation remains visible while transcription and response generation happen

## Key Learning

Voice interfaces require more than transcription.

To feel natural, an AI assistant must:

- Preserve conversational context
- Avoid duplicate processing during UI reruns
- Handle audio securely and efficiently
- Respond quickly without disrupting the user experience

Snowflake Cortex makes it possible to build **end-to-end voice AI apps** entirely inside a data platform.

## Screenshot

![Day 25 Output](<../screenshots/day25_success.png>)
