
# Day 15 – Model Comparison Arena

This project is part of the **#30DaysOfAI** challenge by Streamlit.

## Goal

Build a **side-by-side LLM comparison tool** to evaluate different models on the **same prompt**, helping make informed decisions about speed, output size, and overall suitability for real-world applications.

## Why This Matters

After building full-featured chatbots (Days 8–14), the next big question is:

> **Which model should I use?**

Different LLMs have different trade-offs:

- Speed vs quality
- Cost vs capability
- Smaller models vs larger reasoning models

This tool provides a practical way to compare models before moving into **RAG applications (Week 3)**.

## What this app does

- Lets users select **two LLMs** to compare
- Sends the **same prompt** to both models sequentially
- Displays responses **side-by-side**
- Measures and displays:
  - Total latency (seconds)
  - Estimated output token count
- Uses a clean, chat-style UI
- Persists the latest comparison using Streamlit session state

## Tech Stack

- Python
- Streamlit
- Snowflake Snowpark
- Snowflake Cortex (LLM Inference)
- Multiple LLMs (Llama, Mistral, Mixtral, Claude, OpenAI)

## Key Concepts: Model Evaluation & Trade-offs

### Metrics Collected

- **Latency:** Total time taken for model inference
- **Token Count (Estimated):** Approximate output size  
  (1 token ≈ 0.75 words)

These metrics help approximate:

- User experience (speed)
- Cost implications
- Verbosity of responses

---

## How it Works

### 1. Model Execution and Metrics Collection

Each model is executed using Snowflake Cortex’s `ai_complete()` function.

```python
def run_model(model: str, prompt: str) -> dict:
    start = time.time()
    df = session.range(1).select(
        ai_complete(model=model, prompt=prompt).alias("response")
    )
    rows = df.collect()
    response_raw = rows[0][0]
    response_json = json.loads(response_raw)

    text = response_json.get("choices", [{}])[0].get("messages", "")
    latency = time.time() - start
    tokens = int(len(text.split()) * 4/3)

    return {
        "latency": latency,
        "tokens": tokens,
        "response_text": text
    }
````

Each run returns:

- The model’s response text
- Total inference latency
- Estimated token count

---

### 2. Side-by-Side Model Selection UI

```python
col_a, col_b = st.columns(2)
model_a = col_a.selectbox("Model A", llm_models)
model_b = col_b.selectbox("Model B", llm_models, index=1)
```

- Two dropdowns allow selecting different models
- Defaults ensure models are not identical
- Clean, symmetrical layout improves readability

---

### 3. Side-by-Side Responses and Metrics

```python
container = st.container(height=400, border=True)
```

- Fixed-height containers keep layouts aligned
- Scrollable responses prevent UI overflow
- Metrics are displayed directly below each response

---

### 4. Sequential Execution with Status Feedback

```python
with st.status(f"Running {model_a}..."):
    result_a = run_model(model_a, prompt)

with st.status(f"Running {model_b}..."):
    result_b = run_model(model_b, prompt)
```

- Models run **sequentially** for simplicity and clarity
- Status indicators give users feedback during execution
- Results are stored in `st.session_state` and re-rendered cleanly

---

## Key Learning

Choosing the right LLM is a **product decision**, not just a technical one.

By comparing models side-by-side, you can:

- Identify the fastest model for real-time UX
- Spot overly verbose or underperforming models
- Make informed choices before scaling or adding RAG

This tool turns model selection into a **data-driven decision**.

## Screenshot

![Day 15 Output](<../screenshots/day15_success.png>)
