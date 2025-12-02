import os
import pandas as pd
import streamlit as st

PRED_DIR = "/Users/dnikita/Desktop/pred files"

def list_company_files(pred_dir: str):
    if not os.path.isdir(pred_dir):
        return {}
    files = [
        f for f in os.listdir(pred_dir)
        if os.path.isfile(os.path.join(pred_dir, f)) and f.lower().endswith(".csv")
    ]
    # Map display name -> full path
    return {os.path.splitext(f)[0]: os.path.join(pred_dir, f) for f in files}

@st.cache_data
def load_predictions(path: str):
    df = pd.read_csv(path)
    # Try to normalize date column name
    date_cols = [c for c in df.columns if c.lower() in ("date", "datetime", "timestamp")]
    if date_cols:
        date_col = date_cols[0]
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(by=date_col)
    else:
        date_col = None
    return df, date_col

def main():
    # Main heading with explicit color
    st.markdown(
        "<h1 style='color:#4FC3F7; margin-bottom: 0.5rem;'>Intraday Stock Prediction Dashboard</h1>",
        unsafe_allow_html=True,
    )

    company_files = list_company_files(PRED_DIR)
    if not company_files:
        st.error(f"No CSV prediction files found in '{PRED_DIR}'.")
        st.stop()

    st.sidebar.header("Filters")

    company = st.sidebar.selectbox(
        "Select company",
        options=sorted(company_files.keys()),
    )

    file_path = company_files[company]
    df, date_col = load_predictions(file_path)

    # Subheading for selected company
    st.markdown(
        f"<h2 style='color:#FFB74D; margin-top: 0.5rem;'>Predictions for {company}</h2>",
        unsafe_allow_html=True,
    )

    # Optional date filter
    if date_col is not None:
        min_date = df[date_col].min()
        max_date = df[date_col].max()
        start_date, end_date = st.sidebar.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
        if isinstance(start_date, tuple) or isinstance(start_date, list):
            # Streamlit sometimes returns tuple for single/dual dates, guard just in case
            start_date, end_date = start_date
        mask = (df[date_col].dt.date >= start_date) & (df[date_col].dt.date <= end_date)
        df = df[mask]

    # Columns for actual vs predicted sell prices and label
    lower_cols = {c.lower(): c for c in df.columns}

    actual_low_col = lower_cols.get("actual_low")
    predicted_low_col = lower_cols.get("predicted_low")
    label_col = lower_cols.get("buy_sell_label")

    if actual_low_col is None or predicted_low_col is None:
        st.error("Expected columns 'actual_low' and 'predicted_low' were not found in this file.")
        st.write("Columns found:", list(df.columns))
        st.stop()

    # Latest signal label
    if label_col is not None:
        latest_label = df[label_col].iloc[-1]
        st.markdown(f"### Latest Signal: **{latest_label}**")

    # Summary metrics for latest day: latest high, latest low, latest close
    actual_high_col = lower_cols.get("actual_high")
    predicted_high_col = lower_cols.get("predicted_high")
    predicted_low_col_for_fallback = lower_cols.get("predicted_low")

    # Choose columns for metrics with sensible fallbacks
    high_source_col = actual_high_col or predicted_high_col or predicted_low_col_for_fallback
    low_source_col = actual_low_col or predicted_low_col_for_fallback or predicted_high_col
    close_col = lower_cols.get("close") or predicted_high_col or predicted_low_col_for_fallback

    col1, col2, col3 = st.columns(3)

    if high_source_col is not None:
        col1.metric("Latest high", f"{df[high_source_col].iloc[-1]:.2f}")
    else:
        col1.metric("Latest high", "N/A")

    if low_source_col is not None:
        col2.metric("Latest low", f"{df[low_source_col].iloc[-1]:.2f}")
    else:
        col2.metric("Latest low", "N/A")

    if close_col is not None:
        col3.metric("Latest close", f"{df[close_col].iloc[-1]:.2f}")
    else:
        col3.metric("Latest close", "N/A")

    # Trend: toggle between low and high comparison
    compare_option = st.sidebar.radio(
        "Comparison metric",
        options=["Low", "High"],
        index=0,
    )

    if compare_option == "High":
        # Use actual_high/predicted_high if available, otherwise fall back to low columns
        comp_actual_col = actual_high_col or actual_low_col
        comp_pred_col = predicted_high_col or predicted_low_col
        chart_title = "Actual vs Predicted Sell Price (High)"
    else:
        comp_actual_col = actual_low_col
        comp_pred_col = predicted_low_col
        chart_title = "Actual vs Predicted Sell Price (Low)"

    if date_col is not None:
        trend_df = df[[date_col, comp_actual_col, comp_pred_col]].copy()
        trend_df = trend_df.set_index(date_col)
    else:
        trend_df = df[[comp_actual_col, comp_pred_col]].copy()
        trend_df.index.name = "index"

    st.markdown(
        f"<h2 style='color:#FFB74D; margin-top: 1.5rem;'>{chart_title}</h2>",
        unsafe_allow_html=True,
    )
    st.line_chart(trend_df, height=400)

    st.markdown(
        "<h2 style='color:#FFB74D; margin-top: 1.5rem;'>Raw data</h2>",
        unsafe_allow_html=True,
    )
    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()