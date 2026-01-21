# Day 19 – Creating Cortex Search for Customer Reviews

This project is part of the **#30DaysOfAI** challenge by Streamlit.

## Goal

Create a **semantic search service** for customer reviews using **Snowflake Cortex Search**, enabling meaning-based retrieval instead of keyword matching.

## What this app does

* Uses customer review chunks created in Days 16–18
* Creates a **searchable view** over review text and metadata
* Builds a **Cortex Search service** on top of that view
* Verifies that the search service exists and is ready to use

## Tech Stack

* Python
* Streamlit
* Snowflake Snowpark
* Snowflake Cortex Search
* Snowflake SQL

## Key Concept: Semantic Search with Cortex Search

Cortex Search is Snowflake’s **fully managed semantic search service**.

Unlike keyword search:

* It understands **meaning**, not just exact words
* It automatically indexes data
* It stays in sync with underlying tables
* It inherits Snowflake security and governance

Example:

* Search: *“warm gloves”*
* Matches reviews mentioning *“toasty hands”* or *“kept my fingers warm”*

## How it Works

### 1. Database Configuration

The app allows users to configure:

* Database
* Schema

If embeddings from Day 18 exist in session state, those values are auto-detected.
Otherwise, it falls back to `RAG_DB.RAG_SCHEMA`.

This makes the app reusable across environments.

### 2. Create a Searchable View

A SQL view is created on top of the `REVIEW_CHUNKS` table.

The view:

* Selects review text (`CHUNK_TEXT`)
* Includes metadata (file name, chunk type, document ID)
* Filters out null text values

Why a view?
Cortex Search services operate on **queries**, not raw tables.
Using a view allows:

* Filtering
* Joins
* Schema flexibility

### 3. Create the Cortex Search Service

The app creates a Cortex Search service using:

* `ON CHUNK_TEXT` → searchable text column
* `ATTRIBUTES FILE_NAME, CHUNK_TYPE` → metadata returned with results
* `WAREHOUSE` → compute used for indexing
* `TARGET_LAG = '1 hour'` → refresh frequency

Snowflake automatically:

* Builds the semantic index
* Keeps it updated as data changes

### 4. Verify the Service

The app runs:

* `SHOW CORTEX SEARCH SERVICES`

This confirms:

* The service exists
* Its status (INDEXING or READY)

Once the service is **READY**, it can be queried in Day 20.

## Key Learning

Cortex Search removes the need to manually:

* Generate embeddings for search
* Build vector similarity queries
* Maintain indexes and sync logic

It provides **production-ready semantic search** directly inside Snowflake.

## Screenshot

![Day 19 Output](<../screenshots/day19_success (1).png>)
![Day 19 Output](<../screenshots/day19_success (2).png>)
