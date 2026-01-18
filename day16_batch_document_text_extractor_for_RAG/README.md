# 📄 Day 16 – Batch Document Text Extractor for RAG

This project is part of **Streamlit’s #30DaysOfAI challenge**.
On Day 16, the goal is to build the **document ingestion layer** of a Retrieval-Augmented Generation (RAG) pipeline.

The app allows users to upload documents in bulk, extract raw text, and store everything in **Snowflake**, ready for chunking and embeddings.

---

## 🚀 What This App Does

* Upload **multiple documents at once**
* Supports **TXT, Markdown (MD), and PDF**
* Extracts full raw text from each file
* Stores text + metadata in **Snowflake**
* Enables **Replace or Append** modes
* Provides a built-in UI to query and preview saved documents

---

## 🧠 Why This Matters for RAG

Before embeddings or vector search, RAG pipelines need:

1. Clean text
2. Consistent storage
3. Metadata for filtering and traceability

This app solves **Step 1** of the RAG workflow.

---

## 🧰 Tech Stack

* **Streamlit** – UI and interaction
* **Snowflake Snowpark** – Data storage and queries
* **PyPDF** – PDF text extraction
* **Python** – Core logic

---

## 📥 Sample Dataset

To get started quickly, you can use the provided dataset:

**100 customer review files (TXT format)**
Each file contains:

* Product name
* Review text
* Sentiment score
* Order ID

📦 Download:
[https://github.com/streamlit/30DaysOfAI/raw/refs/heads/main/assets/review.zip](https://github.com/streamlit/30DaysOfAI/raw/refs/heads/main/assets/review.zip)

---

## ▶️ How to Run

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd <repo-name>
```

### 2. Install dependencies

```bash
pip install streamlit snowflake-snowpark-python pypdf pandas
```

### 3. Configure Snowflake credentials

Add your Snowflake connection in:

```toml
.streamlit/secrets.toml
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## 🗄️ Snowflake Table Schema

```sql
CREATE TABLE EXTRACTED_DOCUMENTS (
    DOC_ID NUMBER AUTOINCREMENT,
    FILE_NAME VARCHAR,
    FILE_TYPE VARCHAR,
    FILE_SIZE NUMBER,
    EXTRACTED_TEXT VARCHAR,
    UPLOAD_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    WORD_COUNT NUMBER,
    CHAR_COUNT NUMBER
);
```

---

## 🔁 Replace vs Append Mode

* **Replace Mode**
  Clears existing data before saving new documents
* **Append Mode**
  Adds new documents to the existing table

This makes it easy to test batches or incrementally grow your dataset.

---

## 🔍 Features Included

* Progress bar for batch processing
* File preview before extraction
* Word and character counts
* Query interface to view stored documents
* Full document text viewer
* Session-state support for Day 17 integration

---

## 📌 Part of

**#30DaysOfAI by Streamlit**
Building practical, end-to-end AI applications step by step.

## Screenshot

![Day 16 Output](<../screenshots/day16_success (1).png>)
![Day 16 Output](<../screenshots/day16_success (2).png>)
