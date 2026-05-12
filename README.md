# Product Line Profitability & Margin Performance Analysis for Nassau Candy Distribute Dashboard

## Overview

This project is an interactive **Streamlit dashboard** designed to analyze **product-level profitability, margin performance, and cost efficiency** using the Nassau Candy Distributor dataset.

The goal is to move beyond sales volume and uncover **true profit drivers**, **margin risks**, and **business inefficiencies**.

---

## Live Demo

Deployed on Streamlit Cloud:
(Add your link here after deployment)

---

## Business Objectives

* Identify high-profit and low-profit products
* Analyze margin performance across divisions
* Detect cost inefficiencies and pricing issues
* Evaluate profit concentration using Pareto (80/20) analysis
* Support data-driven business decisions

---

## Key Performance Indicators (KPIs)

* **Gross Margin (%)** → Profitability efficiency
* **Profit per Unit** → Product-level efficiency
* **Revenue Contribution (%)** → Sales share by product
* **Profit Contribution (%)** → Profit share by product
* **Margin Volatility** → Stability of margins over time

---

## Dashboard Features

### Product Analysis

* Product Margin Leaderboard
* Top Products by Profit
* High vs Low Margin Identification

### Division Analysis

* Revenue vs Profit comparison
* Margin distribution across divisions

### Cost Diagnostics

* Cost vs Sales scatter analysis
* Margin Risk Flags (low-margin products)

### Advanced Analytics

* Pareto 80/20 Analysis
* Dependency Indicators (over-reliance on top products)

---

## Key Insights

* A small number of products drive the majority of profit
* High-sales products are not always high-profit
* Certain divisions show structural margin weaknesses
* Some products require pricing or cost optimization

---

## Tech Stack

* Python
* Streamlit
* Pandas
* Matplotlib
* Seaborn
* Plotly

---

## Project Structure

```
project/
│── app.py
│── Nassau_Candy_Distributor.csv
│── requirements.txt
│── README.md
```

---

## How to Run Locally

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Run the app

```
streamlit run app.py
```

---

## Future Improvements

* Add predictive analytics (profit forecasting)
* Implement dynamic pricing recommendations
* Enhance UI with advanced filters and drill-downs
* Deploy with user authentication

---


