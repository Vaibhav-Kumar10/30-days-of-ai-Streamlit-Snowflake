# Day 21 – RAG with Cortex Search

This project is part of the **#30DaysOfAI** challenge by Streamlit.

## Goal

Build a complete **Retrieval-Augmented Generation (RAG)** pipeline using **Snowflake Cortex Search** and **Cortex LLMs** to generate grounded, document-based answers.

## What this app does

- Visualizes the 3-step RAG workflow (Retrieve → Augment → Generate)
- Retrieves relevant document chunks using Cortex Search
- Injects retrieved context into an LLM prompt
- Generates answers grounded strictly in retrieved documents
- Displays source context for transparency and debugging

## Tech Stack

- Python
- Streamlit
- Snowflake Snowpark
- Snowflake Cortex Search
- Snowflake Cortex LLMs
- Claude 3.5 Sonnet / Mistral Large / Llama 3.1

## Key Concept: Retrieval-Augmented Generation (RAG)

RAG combines **search** with **generation** to produce accurate, up-to-date, and context-aware answers.

Instead of relying only on an LLM’s training data:

- Relevant documents are retrieved at query time
- Those documents are injected as context
- The LLM is instructed to answer **only from that context**

This significantly reduces hallucinations and improves trust.

## How it Works

### 1. Visual RAG Overview

The app first explains RAG using a simple visual guide:

- **Retrieve**: Cortex Search finds relevant document chunks
- **Augment**: Retrieved chunks are added to the prompt
- **Generate**: The LLM produces a grounded answer

This helps users understand the pipeline before interacting with it.

### 2. Smart Search Service Selection

The sidebar automatically:

- Detects available Cortex Search services
- Prioritizes the Day 19 service (`CUSTOMER_REVIEW_SEARCH`)
- Allows manual entry if needed

This makes the app reusable across environments and schemas.

### 3. Retrieval with Cortex Search

When a user asks a question:

- The app queries Cortex Search using semantic similarity
- Retrieves the top-N most relevant chunks
- Collects both text and source metadata

These chunks become the grounding context.

### 4. Prompt Augmentation

The retrieved chunks are injected into a carefully structured prompt that:

- Restricts the LLM to use only the provided context
- Forces the model to say “I don’t know” if information is missing
- Clearly separates context from the user question

### 5. Grounded Answer Generation

The app uses:

```

SNOWFLAKE.CORTEX.COMPLETE()

```

to generate the final answer using the selected LLM.

This approach is well-suited for RAG workflows where prompts contain large, dynamic context blocks.

### 6. Transparent Results

The final output includes:

- A clear, readable answer
- Optional expandable context chunks
- Source attribution for each retrieved document

This makes the system explainable and trustworthy.

## Key Learning

By combining **Cortex Search** and **Cortex LLMs**, you can build a fully managed, production-ready RAG system directly inside Snowflake — without external vector databases or custom infrastructure.

Day 21 completes the full RAG pipeline:

- Day 19 → Build the search index
- Day 20 → Query it
- Day 21 → Generate grounded answers

## Screenshot

![Day 21 Output](<../screenshots/day21_success (1).png>)
![Day 21 Output](<../screenshots/day21_success (2).png>)
