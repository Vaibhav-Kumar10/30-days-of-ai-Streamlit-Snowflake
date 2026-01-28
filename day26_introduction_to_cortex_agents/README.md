# Day 26 – Introduction to Cortex Agents

This project is part of the **#30DaysOfAI** challenge by Streamlit.

## Goal

Build a **multi-tool Cortex Agent** that can autonomously answer questions by choosing between:

- Semantic search on sales conversations
- SQL-based analytics on sales metrics

## What this app does

- Sets up structured and unstructured sales data in Snowflake
- Creates a **Cortex Search service** for conversation transcripts
- Defines a **semantic model (YAML)** for analytics
- Builds a **Cortex Agent** that:
  - Uses Cortex Search for conversation-based questions
  - Uses Cortex Analyst for metrics and aggregations
- Provides a Streamlit UI to manage setup and agent creation

## Tech Stack

- Python
- Streamlit
- Snowflake Snowpark
- Snowflake Cortex Agents
- Cortex Search
- Cortex Analyst (Text-to-SQL)
- Claude Sonnet (Agent Orchestration)

## Key Concept: Cortex Agents

Cortex Agents are **autonomous AI assistants** that can:

- Analyze a user question
- Decide which tool to use
- Execute the tool
- Synthesize a final response

This removes the need for manually coding:

- Retrieval logic
- Tool selection
- Prompt routing
- SQL generation

## How it Works

### 1. Sales Conversations Data

A table of real-world sales call transcripts is created to simulate unstructured enterprise data.

This data is indexed using **Cortex Search**, enabling semantic retrieval based on meaning rather than keywords.

### 2. Sales Metrics Data

A structured sales metrics table is created containing:

- Deal values
- Win/loss status
- Sales reps
- Product lines

This table is queried by **Cortex Analyst** using natural language.

### 3. Semantic Model (YAML)

A semantic model defines:

- Dimensions
- Measures
- Synonyms
- Time fields

This allows Cortex Analyst to translate natural language questions into valid SQL.

### 4. Multi-Tool Cortex Agent

The agent is created with:

- Clear instructions and constraints
- Two tools:
  - Cortex Search → conversation questions
  - Cortex Analyst → metrics questions
- Orchestration logic that decides which tool to use automatically

### 5. Streamlit Interface

The app provides:

- Step-by-step data setup
- One-click agent creation
- Validation checks
- A clean foundation for adding a chat interface (Day 27)

## Key Learning

Cortex Agents represent a major shift from manual RAG pipelines to **autonomous, tool-driven AI systems**.

Instead of writing orchestration code, you define:

- Data
- Tools
- Rules

The agent handles the rest.

## Screenshot

![Day 26 Output](<../screenshots/day26_success (1).png>)
![Day 26 Output](<../screenshots/day26_success (2).png>)
![Day 26 Output](<../screenshots/day26_success (3).png>)
![Day 26 Output](<../screenshots/day26_success (4).png>)
![Day 26 Output](<../screenshots/day26_success (5).png>)
![Day 26 Output](<../screenshots/day26_success (6).png>)
![Day 26 Output](<../screenshots/day26_success (7).png>)
