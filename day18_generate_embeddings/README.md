# Day 18 – Generating Embeddings for Customer Reviews

This project is part of the **#30DaysOfAI** challenge by Streamlit.

## Goal

Generate **vector embeddings** for customer review chunks created in Day 17 using **Snowflake Cortex**, and store them in Snowflake’s **VECTOR** data type to enable semantic search.

## What this app does

* Loads review chunks from Snowflake (Day 17 output)
* Generates **768-dimensional embeddings** using Snowflake Cortex
* Stores embeddings in a Snowflake table with the VECTOR data type
* Verifies embeddings to ensure correctness before semantic search

## Tech Stack

* Python
* Streamlit
* Snowflake Snowpark
* Snowflake Cortex (Embeddings)
* Snowflake VECTOR data type

## Key Concept: Embeddings for Semantic Search

Embeddings convert text into numerical vectors that capture meaning.

* Similar text → Similar vectors
* Different text → Distant vectors
* Enables **semantic search**, not keyword matching

Each review chunk is converted into a **768-dimensional vector** using the model:

`snowflake-arctic-embed-m`

## How it Works

### 1. Load Review Chunks

The app connects to Snowflake and loads review chunks created in Day 17 from the `REVIEW_CHUNKS` table.

Each chunk includes:

* Chunk ID
* Review text
* Metadata (file name, size, chunk type)

### 2. Generate Embeddings (Correct Cortex Pattern)

Embeddings are generated **inside Snowflake** using SQL:

* Uses `SNOWFLAKE.CORTEX.EMBED_TEXT_768`
* Processes all chunks in a single query
* Avoids Python-side embedding calls
* Fully production-ready and scalable

This approach is faster, cheaper, and follows Snowflake’s official Cortex usage pattern.

### 3. Save Embeddings to Snowflake

Embeddings are stored in a table with schema:

* `CHUNK_ID`
* `EMBEDDING VECTOR(FLOAT, 768)`
* Creation timestamp

The app supports:

* **Replace mode** (overwrite existing embeddings)
* **Append mode** (add new embeddings)

### 4. Validate Stored Embeddings

The app validates embeddings by:

* Querying the embedding table
* Computing self-distance (should be `0`)
* Inspecting individual embedding vectors

## Key Learning

High-quality RAG and semantic search systems depend on **efficient, database-native embedding generation**.

Generating embeddings directly inside Snowflake:

* Improves performance
* Reduces orchestration complexity
* Aligns with production AI architecture

## Screenshot

![Day 18 Output](<../screenshots/day18_success (1).png>)
![Day 18 Output](<../screenshots/day18_success (2).png>)
![Day 18 Output](<../screenshots/day18_success (3).png>)
![Day 18 Output](<../screenshots/day18_success (4).png>)
