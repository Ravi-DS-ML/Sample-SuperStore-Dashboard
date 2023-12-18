# Sample SuperStore EDA Dashboard

## Overview

This Streamlit-based dashboard provides an exploratory data analysis (EDA) of the Sample SuperStore dataset. The dashboard allows users to upload a file, filter data based on date ranges and geographical attributes, and explore various visualizations and summaries related to sales data.

## Features

- **File Upload:** Users can upload CSV or Excel files containing SuperStore data.
- **Date Filtering:** Filter data based on a selected date range.
- **Geographical Filtering:** Filter data by Region, State, and City.
- **Visualizations:**
  - Category-wise Sales Bar Chart
  - Region-wise Sales Pie Chart
  - Monthly Sales Line Chart
  - Hierarchical TreeMap
  - Segment-wise and Category-wise Pie Charts
- **Data Exploration:**
  - View and download Category-wise and Region-wise sales data.
  - View and download Monthly sales data.
- **Summary Tables:**
  - Display a summary table of Category-wise and Region-wise sales.
  - Display a summary table of Month-wise Sub-Category Sales.
- **Scatter Plot:** Explore the relationship between Sales, Profit, and Quantity.
- **Download Original Data:** Download the original SuperStore dataset.

## How to Run

1. Install the required dependencies:

   ```bash
   pip install streamlit pandas plotly openpyxl

2. Or use

   ```bash
   pip install -r requirements.txt
  
## Open the provided URL in your web browser.

## Project Structure
  dashboard.py: Main application file containing the Streamlit app code.
  Sample - Superstore.xls: Default dataset file (Excel format).
  README.md: Project documentation.
## Dependencies
  streamlit: Web app framework for creating data applications.
  pandas: Data manipulation library.
  plotly: Interactive plotting library.
  openpyxl: Excel file reading and writing library.

## Author
  Ravi

