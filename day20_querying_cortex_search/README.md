# Day 20 – Querying Cortex Search

This project is part of the **#30DaysOfAI** challenge by Streamlit.

## Goal

Query the **Cortex Search service** created in Day 19 to retrieve relevant customer reviews using **semantic search** and natural language queries.

## What this app does

- Connects to Snowflake across environments (SiS, local, Community Cloud)
- Detects available Cortex Search services
- Allows users to select or manually enter a search service
- Executes semantic search using the **Cortex Search Python SDK**
- Displays ranked results with metadata and relevance scores

## Tech Stack

- Python
- Streamlit
- Snowflake Snowpark
- Snowflake Cortex Search
- Snowflake Python SDK (`snowflake.core`)

## Key Concept: Querying Cortex Search

Cortex Search enables **meaning-based retrieval** rather than keyword matching.

Instead of matching exact words, it retrieves results based on semantic similarity.

Example:

- Query: *“durability issues”*
- Matches reviews like:
  - “broke after two weeks”
  - “lasted three seasons without problems”

## How it Works

### 1. Environment-Aware Snowflake Connection

The app automatically detects whether it is running:

- In Streamlit in Snowflake (SiS)
- Locally
- On Streamlit Community Cloud

and establishes the correct Snowflake session.

### 2. Search Service Discovery

The app runs:

```

SHOW CORTEX SEARCH SERVICES

```

This allows users to:

- Select an existing service from a dropdown
- Manually enter a service path if needed

The Day 19 service (`CUSTOMER_REVIEW_SEARCH`) is always prioritized.

### 3. Semantic Search Execution

The search is performed using the **Cortex Search Python SDK**:

- Natural language query input
- Configurable number of results
- Automatic relevance ranking

The SDK abstracts SQL and provides a clean, object-based API.

### 4. Result Display

Each result includes:

- Review text chunk
- File name
- Chunk type
- Chunk ID
- Optional relevance score

Results are displayed in a structured, readable layout with clear separation.

## Key Learning

Cortex Search makes it easy to build **production-grade semantic search** directly in Snowflake without managing embeddings, vector stores, or infrastructure.

By combining Day 19 and Day 20:

- Day 19 → Build the search index
- Day 20 → Query it using natural language

This completes the **search layer of a RAG pipeline**.

## Screenshot

![Day 20 Output](<../screenshots/day20_success (1).png>)
![Day 20 Output](<../screenshots/day20_success (2).png>)
