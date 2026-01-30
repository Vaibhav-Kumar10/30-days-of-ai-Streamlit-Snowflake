# Data Analysis Tool (CSV Upload)

This small Streamlit app lets you upload a CSV file, perform quick exploratory data analysis (EDA), visualize columns, and download the current view as CSV.

## Features

- Upload CSV files
- Preview rows and summary statistics
- View missing-value percent per column
- Create histogram, box, and scatter plots
- Correlation matrix for numeric columns
- Download filtered/cleaned view as CSV

## Run locally

```bash
cd day28_building_apps_with_agents_md/data_analysis_tool
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- Works locally and in Streamlit Community Cloud
- For large CSVs, increase memory or sample before uploading
