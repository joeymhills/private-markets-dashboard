# Private Markets Performance Analyzer

This is a lightweight Streamlit app that calculates and visualizes performance metrics (MOIC, IRR) for alternative investments like private equity and hedge funds based on user-uploaded cash flow data.

## Features

- Upload a CSV of capital calls, distributions, and NAVs
- Calculates:
  - IRR (Internal Rate of Return)
  - MOIC (Multiple on Invested Capital)
- Visualizes signed cash flows over time

## Sample Input Format (CSV)

Your CSV should have the following structure:

```csv
Date,Type,Amount
2020-01-15,Capital Call,250000
2020-12-31,Distribution,25000
2022-12-31,NAV,325000
```
