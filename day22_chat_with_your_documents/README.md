# Day 22 – Chat with Your Documents

This project is part of the **#30DaysOfAI** challenge by Streamlit.

## Goal

Build a **conversational RAG (Retrieval-Augmented Generation) chatbot** that allows users to chat with their own documents using **Cortex Search** and **Snowflake Cortex LLMs**.

Unlike single-turn Q&A, this app maintains **full conversation history**, enabling follow-up questions and contextual dialogue.

## What this app does

- Provides a chat-based interface using Streamlit
- Maintains multi-turn conversation history
- Performs semantic search on every user query using Cortex Search
- Grounds LLM responses strictly in retrieved document chunks
- Displays source attribution for transparency
- Allows users to clear chat history instantly

## Tech Stack

- Python
- Streamlit
- Snowflake Snowpark
- Snowflake Cortex Search
- Snowflake Cortex LLMs (Claude 3.5 Sonnet)

## Key Concept: Conversational RAG

Each user message triggers:

1. **Retrieve** – Relevant document chunks using Cortex Search  
2. **Augment** – Retrieved text injected into the prompt  
3. **Generate** – LLM produces a grounded answer  

Conversation history is preserved using `st.session_state`, allowing natural follow-up questions without losing context.

## How it Works

### 1. Persistent Conversation State

The entire chat (user + assistant messages) is stored in `st.session_state`, ensuring history persists across reruns.

### 2. Smart Cortex Search Service Selection

- Automatically detects available Cortex Search services
- Defaults to the Day 19 service
- Supports manual service path entry
- Provides visual confirmation when using the correct service

### 3. Secure Retrieval Function

A reusable search function:

- Validates service paths
- Retrieves chunk text and source metadata
- Returns structured results for clean rendering

### 4. Guardrails for Reliability

The system prompt strictly enforces:

- Answers only from retrieved documents
- No general knowledge, coding, or unrelated topics
- Clear fallback responses when context is insufficient

This prevents hallucinations and keeps the chatbot focused and trustworthy.

### 5. Source Attribution

Each response includes expandable sources showing:

- File name
- Relevant document excerpts
This improves transparency and debuggability.

## Key Learning

Conversational RAG combines **state management**, **retrieval accuracy**, and **strict grounding** to build reliable AI assistants that scale beyond simple Q&A.

This pattern is foundational for enterprise document chat, internal knowledge bases, and support copilots.

## Screenshot

![Day 22 Output](<../screenshots/day22_success (1).png>)
![Day 22 Output](<../screenshots/day22_success (2).png>)
![Day 22 Output](<../screenshots/day22_success (3).png>)
