# Day 01 – Connect Streamlit to Snowflake

This project is part of the **#30DaysOfAI** challenge by Streamlit.

## Goal

Establish a successful connection between a Streamlit app and a Snowflake database and verify it by querying the Snowflake version.

## What the app does

- Connects to Snowflake using Snowpark
- Runs a simple SQL query: `SELECT CURRENT_VERSION()`
- Displays the result in a Streamlit UI

## Tech Stack

- Python
- Streamlit
- Snowflake Snowpark

## How it works

When run inside **Streamlit in Snowflake**, the app automatically uses the active Snowflake session.  
No credentials or secrets are stored in the code or repository.

## Output

A success message confirming the Snowflake connection along with the current Snowflake version.

## Screenshot

![Day 1 Output](../screenshots/day01_success.png)
