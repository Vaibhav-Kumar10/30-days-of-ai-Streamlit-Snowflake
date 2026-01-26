# Day 24 – Working with Images (Multimodality)

This project is part of the **#30DaysOfAI** challenge by Streamlit.

## Goal

Build a complete **image analysis application** using Snowflake’s `AI_COMPLETE` function with **vision-capable LLMs**, enabling multimodal AI workflows.

## What this app does

- Allows users to upload images in a bordered container
- Uploads images securely to a Snowflake stage
- Uses **vision-capable models** to analyze images
- Supports multiple analysis types:
  - General description
  - OCR (text extraction)
  - Object identification
  - Chart/graph analysis
  - Custom prompts
- Displays AI-generated results in a separate bordered container
- Shows technical details like model, prompt, and stage used

## Tech Stack

- Python
- Streamlit
- Snowflake Snowpark
- Snowflake Cortex `AI_COMPLETE`
- Vision-capable LLMs (Claude, OpenAI, Pixtral)

## Key Concept: Multimodal AI with Images

This app demonstrates **multimodal AI**, where models process both:

- **Visual input** (images)
- **Text prompts**

Instead of just text-in/text-out, the AI can now:

- Read text from images (OCR)
- Understand visual content
- Analyze charts and diagrams
- Answer custom image-based questions

## How it Works

### 1. Secure Image Storage

- Images are uploaded to a Snowflake stage
- The stage is created with **server-side encryption (SNOWFLAKE_SSE)**, which is required for vision models
- Each image gets a unique timestamp-based filename

### 2. Vision Analysis with `AI_COMPLETE`

- The app calls `SNOWFLAKE.CORTEX.AI_COMPLETE()`
- Images are passed using the `TO_FILE()` syntax
- Users can select different vision-capable models from the sidebar

### 3. Clean UI with Bordered Containers

- One container for uploading and previewing images
- A separate container for displaying analysis results
- Session state ensures results persist across reruns

## Supported Models

- `claude-3-5-sonnet`
- `openai-gpt-4.1`
- `openai-o4-mini`
- `pixtral-large`

## Key Learning

Multimodal AI unlocks entirely new use cases.

With Snowflake Cortex and Streamlit:

- Images become first-class AI inputs
- Vision models can be used directly inside data apps
- Secure, production-ready image analysis is possible without external services

## Screenshot

![Day 24 Output](<../screenshots/day24_success.png>)
