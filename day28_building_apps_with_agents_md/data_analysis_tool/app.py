import io
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Data Analysis Tool", page_icon=":material/table_chart:", layout="wide"
)

st.title(":material/table_chart: Data Analysis Tool — CSV Upload")
st.write("Upload a CSV, explore the data, and generate simple visualizations.")


@st.cache_data(show_spinner=False)
def load_csv(uploaded_file) -> pd.DataFrame:
    # Use a robust CSV load to handle different encodings/newlines
    uploaded_file.seek(0)
    return pd.read_csv(
        io.TextIOWrapper(uploaded_file, encoding="utf-8"), low_memory=False
    )


def numeric_cols(df: pd.DataFrame):
    return df.select_dtypes(include=[np.number]).columns.tolist()


def categorical_cols(df: pd.DataFrame):
    return df.select_dtypes(exclude=[np.number]).columns.tolist()


with st.sidebar:
    st.header("Upload / Settings")
    uploaded = st.file_uploader(
        "Upload CSV file", type=["csv"], accept_multiple_files=False
    )
    sample_rows = st.slider("Rows to preview", min_value=5, max_value=100, value=10)
    st.markdown("---")
    st.markdown(
        "Built with Streamlit — basic EDA: preview, describe, missing values, plots, download."
    )


if uploaded is not None:
    try:
        df = load_csv(uploaded)
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        st.stop()

    st.sidebar.success(
        f"Loaded: {uploaded.name} — {df.shape[0]} rows x {df.shape[1]} cols"
    )

    # Top summary
    st.subheader("Data Preview")
    st.dataframe(df.head(sample_rows))

    # Basic info
    st.subheader("Basic Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", df.shape[0])
    with col2:
        st.metric("Columns", df.shape[1])
    with col3:
        st.metric("Missing Cells", int(df.isna().sum().sum()))

    # Describe numeric
    if len(numeric_cols(df)):
        st.subheader("Numeric Summary")
        st.dataframe(df[numeric_cols(df)].describe().T)

    # Missing values
    st.subheader("Missing Values")
    miss = (df.isna().sum() / len(df) * 100).sort_values(ascending=False)
    st.dataframe(miss.to_frame("% missing"))

    # Column selection for plots
    st.subheader("Visualizations")
    plot_col1, plot_col2 = st.columns([2, 3])

    with plot_col1:
        x_axis = st.selectbox(
            "X axis (for histogram / box)", options=df.columns, index=0
        )
        numeric_candidates = numeric_cols(df)
        y_axis = st.selectbox(
            "Y axis (for scatter)",
            options=(numeric_candidates if numeric_candidates else [None]),
            index=0,
        )
        plot_type = st.radio("Plot type", ["Histogram", "Box", "Scatter"], index=0)

        # Filters
        st.markdown("---")
        st.write("Quick filters")
        filter_col = st.selectbox(
            "Filter column (optional)", options=[None] + df.columns.tolist(), index=0
        )
        filter_val = None
        if filter_col:
            unique_vals = df[filter_col].dropna().unique()[:50]
            filter_val = st.selectbox(
                "Filter value (optional)", options=[None] + list(unique_vals), index=0
            )

    with plot_col2:
        df_plot = df
        if filter_col and filter_val is not None:
            df_plot = df_plot[df_plot[filter_col] == filter_val]

        if plot_type == "Histogram":
            fig = px.histogram(
                df_plot, x=x_axis, nbins=50, title=f"Histogram — {x_axis}"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif plot_type == "Box":
            if x_axis in numeric_cols(df_plot):
                fig = px.box(df_plot, y=x_axis, title=f"Box plot — {x_axis}")
            else:
                fig = px.box(df_plot, x=x_axis, title=f"Box plot — {x_axis}")
            st.plotly_chart(fig, use_container_width=True)

        elif plot_type == "Scatter":
            if (y_axis is None) or (y_axis not in numeric_cols(df_plot)):
                st.info("Select a numeric Y axis for scatter plots")
            else:
                fig = px.scatter(
                    df_plot, x=x_axis, y=y_axis, title=f"Scatter — {x_axis} vs {y_axis}"
                )
                st.plotly_chart(fig, use_container_width=True)

    st.subheader("Correlation Matrix (numeric columns)")
    if len(numeric_cols(df)) >= 2:
        corr = df[numeric_cols(df)].corr()
        fig = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation matrix")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough numeric columns to show correlation matrix.")

    # Download cleaned/filtered CSV
    st.subheader("Download")

    def convert_df_to_csv(dataframe: pd.DataFrame) -> bytes:
        return dataframe.to_csv(index=False).encode("utf-8")

    cleaned = df_plot.copy()
    csv_bytes = convert_df_to_csv(cleaned)
    st.download_button(
        "Download current view as CSV",
        data=csv_bytes,
        file_name="data_view.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.caption(
        "Tip: Use the filter to focus on subsets before plotting or downloading."
    )

else:
    st.info(
        "Upload a CSV file from the sidebar to get started — sample datasets also work."
    )
