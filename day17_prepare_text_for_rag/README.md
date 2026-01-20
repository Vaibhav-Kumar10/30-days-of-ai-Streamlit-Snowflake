# Day 17 – Preparing Text Data for RAG

This project is part of the **#30DaysOfAI** challenge by Streamlit.

## Goal

Prepare extracted document text for **Retrieval-Augmented Generation (RAG)** by loading it from Snowflake, applying chunking logic, and saving clean, structured chunks back to Snowflake.

This step bridges raw documents (Day 16) and embeddings + retrieval (Day 18).

## What this app does

- Loads extracted documents stored in Snowflake (from Day 16)
- Analyzes document length and metadata
- Applies configurable text chunking logic
- Stores text chunks in a new Snowflake table
- Makes the data ready for embedding generation and semantic search

## Tech Stack

- Python
- Streamlit
- Snowflake Snowpark
- Snowflake SQL
- Pandas

## Key Concept: Text Chunking for RAG

LLMs perform better when retrieving **small, meaningful chunks** of text instead of entire documents.

This app supports:

- **Full-document chunks** (for short texts like reviews)
- **Overlapping chunks** (for longer documents)

Chunking improves:

- Retrieval accuracy
- Context relevance
- Embedding quality

## How it Works

### 1. Load Documents from Snowflake

The app connects to Snowflake and loads documents created in Day 16 from the `EXTRACTED_DOCUMENTS` table.

Each row contains:

- File metadata
- Full extracted text
- Word and character counts

### 2. Chunking Strategy

Depending on document length:

- Short documents → Stored as a single chunk
- Long documents → Split into overlapping chunks using word-based windows

Each chunk is tagged with:

- Document ID
- File name
- Chunk size
- Chunk type (full or chunked)

### 3. Save Chunks to Snowflake

All chunks are written to a new table (e.g. `REVIEW_CHUNKS`) using Snowpark.

The table stores:

- Chunk text
- Metadata for traceability
- Timestamps for auditing

### 4. Preview and Validation

The app allows querying the chunk table and previewing chunk content to verify correctness before moving to embeddings.

## Key Learning

High-quality RAG systems depend more on **data preparation** than models.  
Proper chunking is essential for accurate retrieval, efficient embeddings, and reliable AI applications.

## Next Step

Day 18 will generate embeddings for these chunks and enable semantic search using Snowflake.

## Screenshot

![Day 17 Output](<../screenshots/day17_success (1).png>)
![Day 17 Output](<../screenshots/day17_success (2).png>)
![Day 17 Output](<../screenshots/day17_success (3).png>)
