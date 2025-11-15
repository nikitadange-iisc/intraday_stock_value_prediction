import pandas as pd
import streamlit as st

PRED_PATH = "Data_processed/daily_predictions_all_companies.csv"
METRICS_PATH = "Data_processed/daily_model_metrics_all_companies.csv"

@st.cache_data
def load_data():
    preds = pd.read_csv(PRED_PATH, parse_dates=["date"])
    metrics = pd.read_csv(METRICS_PATH)
    return preds, metrics

preds_df, metrics_df = load_data()

if preds_df.empty:
    st.error("Predictions file is empty or not found.")
    st.stop()

if metrics_df.empty:
    st.error("Metrics file is empty or not found.")
    st.stop()

st.sidebar.title("Filters")

companies = sorted(preds_df["company_name"].unique())
targets = sorted(preds_df["target"].unique())

selected_company = st.sidebar.selectbox("Company", companies)
selected_target = st.sidebar.selectbox("Target (OHLC)", targets)

model_options = ["RandomForest_v1"]
selected_model = st.sidebar.selectbox("Model", model_options)
st.sidebar.markdown(f"**Selected model:** {selected_model}")

mask = (
    (preds_df["company_name"] == selected_company) &
    (preds_df["target"] == selected_target)
)
company_preds = preds_df[mask].sort_values("date")

if company_preds.empty:
    st.warning("No prediction data for this combination.")
    st.stop()

st.title("Stock Price Prediction Dashboard")
st.subheader(f"{selected_company} – {selected_target.upper()}")

st.write(
    "Trend of actual vs predicted values on the test set "
    "(from daily_predictions_all_companies.csv)."
)

plot_df = company_preds[["date", "y_true", "y_pred"]].set_index("date")
st.line_chart(plot_df.rename(columns={
    "y_true": "Actual",
    "y_pred": "Predicted",
}))

st.markdown("### Model Metrics")

row = metrics_df[metrics_df["company_name"] == selected_company]
if row.empty:
    st.warning("No metrics found for this company in metrics file.")
else:
    row = row.iloc[0]
    prefix = selected_target  # "open", "high", "low", "close"
    metric_names = ["RMSE", "MAE", "MAPE", "R2"]

    metrics_data = {}
    for m in metric_names:
        col = f"{prefix}_{m}"
        metrics_data[m] = row[col] if col in row.index else None

    cols = st.columns(len(metric_names))
    for i, m in enumerate(metric_names):
        with cols[i]:
            val = metrics_data[m]
            if val is None:
                st.metric(m, "N/A")
            else:
                if m == "MAPE":
                    st.metric(m, f"{val:.2f} %")
                else:
                    st.metric(m, f"{val:.4f}")

with st.expander("Show raw prediction data"):
    st.dataframe(company_preds.sort_values("date").reset_index(drop=True))

with st.expander("Show metrics row for this company"):
    if not metrics_df[metrics_df["company_name"] == selected_company].empty:
        st.dataframe(metrics_df[metrics_df["company_name"] == selected_company])