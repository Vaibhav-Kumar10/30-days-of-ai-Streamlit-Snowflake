# Day 23 – LLM Evaluation & AI Observability

This project is part of the **#30DaysOfAI** challenge by Streamlit.

## Goal

Evaluate the quality of a **RAG application** using **TruLens** and **Snowflake AI Observability**, focusing on accuracy, grounding, and relevance.

## What this app does

- Evaluates a RAG application built in Days 21–22
- Uses **TruLens** to automatically score responses
- Computes the **RAG Triad metrics**:
  - Context Relevance
  - Groundedness
  - Answer Relevance
- Stores evaluation results in Snowflake
- Visualizes results directly in **Snowsight**
- Supports multiple runs, versions, and models

## Tech Stack

- Python
- Streamlit
- Snowflake Snowpark
- Snowflake Cortex (LLM Inference)
- Snowflake AI Observability
- TruLens
- Claude 3.5 Sonnet / Mixtral / LLaMA

## Key Concept: LLM Evaluation with the RAG Triad

This app evaluates RAG systems using three core metrics:

- **Context Relevance** → Did we retrieve the right documents?
- **Groundedness** → Is the answer strictly based on retrieved context?
- **Answer Relevance** → Does the answer actually address the question?

Together, these metrics provide a complete picture of RAG quality.

## How it Works

### 1. Instrumented RAG Pipeline

The RAG pipeline is wrapped with `@instrument()` decorators so TruLens can trace:

- Document retrieval
- Prompt construction
- LLM generation

### 2. Automated Batch Evaluation

- Test questions are stored in a Snowflake table
- TruLens runs the RAG app against all questions
- Each run is versioned for comparison

### 3. Metrics Computation

After execution, TruLens computes:

- Context Relevance
- Groundedness
- Answer Relevance

Results are automatically stored in Snowflake AI Observability.

### 4. Snowsight Visualization

All evaluation results can be explored in:
**Snowsight → AI & ML → Evaluations**

## Key Learning

Building LLM apps is not enough — **measuring quality is critical**.

With TruLens and Snowflake AI Observability:

- You detect hallucinations
- You validate retrieval quality
- You compare versions and models confidently

This is how RAG systems become production-ready.

## Screenshot

![Day 23 Output](<../screenshots/day23_success.png>)
