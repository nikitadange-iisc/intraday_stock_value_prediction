# Intraday Stock Value Prediction

## Team Members
- Ananya Sarkar (ananya1@iisc.ac.in)
- Nikita Dange (nikita@iisc.ac.in)
- Vasanthkumar S (vasanthakum1@iisc.ac.in)
- Raj Shekhar (rajshekhar1@iisc.ac.in)

> **Note:** Replace the above with your actual team member names and roll numbers.

## Problem Statement

Build a system to predict intraday stock price ranges and trading signals (e.g., BUY/SELL) for selected equities using historical market data. The goal is to produce:

- Predicted intraday **high** and **low** prices.
- A trading recommendation label (e.g., BUY/SELL) per day.
- An interactive dashboard to explore model predictions across companies and dates.

## Dataset Description

All raw market data used in this project is stored under:

- `Code/Data/Data_25_companies/`

This folder contains **minute-level OHLCV data** for **25 NSE-listed equities**. Each stock has its own CSV file, for example:

- `HDFCAMC_minute.csv`
- `ICICIGI_minute.csv`
- `ICICIPRULI_minute.csv`
- `ADANIGREEN_minute.csv`, `ADANIPOWER_minute.csv`, ..., `SHREECEM_minute.csv`

Each CSV contains intraday records with the following columns:

- `date` – timestamp at 1-minute resolution (e.g., `2018-08-06 09:44:00`).
- `open` – open price for that minute.
- `high` – highest traded price during that minute.
- `low` – lowest traded price during that minute.
- `close` – closing price for that minute.
- `volume` – traded volume in that minute.

From this minute-level data, we derive daily features/targets used for modelling daily **high**/**low** ranges and trading signals. Aggregation and feature engineering steps (e.g., daily OHLC, rolling statistics, lag features) are implemented in the notebooks/scripts under `Code/EDA`, `Code/Modelling`, and `Code/Data_processed`.

You can document here any additional preprocessing choices, such as:

- Trading days/time windows retained (e.g., regular market hours only).
- Handling of missing/minimal-volume minutes.
- Train/validation/test split by time (e.g., first N years for training, last M months for validation/testing).

## Approach and Methods

Summarize, at a high level, the modeling and engineering pipeline. For example:

- **Exploratory Data Analysis (EDA):**
  - Distribution of price ranges and volumes.
  - Correlations between features and target variables.

- **Feature Engineering:**
  - Lag features (previous days' highs/lows/returns).
  - Rolling statistics (moving averages, volatility).
  - Technical indicators if used (RSI, MACD, etc.).

- **Modeling:**
  - Regression models for `predicted_high` and `predicted_low` (e.g., tree-based models, linear models, or deep learning).
  - Thresholding logic or auxiliary model to derive `buy_sell_label`.

- **Evaluation:**
  - Error metrics for price prediction (e.g., MAE, RMSE).
  - Confusion matrix / precision / recall for BUY/SELL labels.

- **Dashboard:**
  - Implemented with **Streamlit** (`Code/Dashboard/dashboard.py`).
  - Allows filtering by company and date range.
  - Shows trend charts comparing **actual vs predicted** highs/lows and summarizing latest-day metrics (latest high, low, and close-style values).

> Replace or expand this section with the exact methods you used (model types, hyperparameters, training strategy, etc.).

## Results Summary

Provide a concise summary of your key findings and performance. For example:

- **Price prediction performance:**
  - Validation MAE (high): XX.XX
  - Validation MAE (low): XX.XX
  - RMSE or other metrics.

- **Label performance (BUY/SELL):**
  - Accuracy: XX%
  - Precision/Recall/F1 for BUY class.

- **Qualitative insights:**
  - How well the model tracks market movements.
  - Cases where predictions are particularly strong or weak.

> Add tables, figures, or links to plots if you have them.

## Project Structure

A brief overview (update as needed):

- `Code/`
  - `Dashboard/`
    - `dashboard.py` – Streamlit app for visualizing predictions.
  - `EDA/` – notebooks or scripts for exploratory analysis.
  - `Modelling/` – model training and evaluation code.
  - `Data/` – raw data (if included or sample files).
  - `Data_processed/` – processed/feature-engineered data.
  - `pred files/` – prediction CSV files per company used by the dashboard.
- `requirements.txt` – Python dependencies.
- `LICENSE` – license for this repository.

## How to Run the Dashboard

1. Install dependencies (preferably in a virtual environment):

   ```bash
   pip install -r requirements.txt
   ```

2. From the repo root, run the Streamlit app:

   ```bash
   cd Code/Dashboard
   python3 -m streamlit run dashboard.py
   ```

3. Open the URL shown in the terminal (e.g., `http://localhost:8501`).

## How to Reproduce the Modelling

Briefly document how to:

- Prepare data (scripts/notebooks in `Code/Data` or `Code/Data_processed`).
- Train models (scripts in `Code/Modelling`).
- Generate prediction files into `Code/pred files/` that the dashboard reads.

## License

This project is licensed under the terms described in the `LICENSE` file in this repository.
