# 💳 DefaulterInsight – Credit Card Defaulters Prediction

A scalable machine learning solution to predict whether a customer will default on their credit card payment next month. This system uses clustering and model tuning techniques to provide accurate predictions for batch-uploaded CSV files.

🔗 **Live App**: [DefaulterInsight on Render](https://machine-learning-b4qq.onrender.com)

---

## 🧠 Problem Statement

Financial institutions face massive losses due to unpaid credit card bills. This system uses predictive modeling to determine whether a customer is likely to **default next month**, helping institutions mitigate risk.

---

## 📂 Dataset Description

The dataset contains **32,561 records** with features that include demographics, payment history, bill amounts, and repayment amounts.

### 🎯 Features

| Feature            | Description                            |
|--------------------|----------------------------------------|
| `LIMIT_BAL`        | Credit limit of the customer           |
| `SEX`              | 1 = Male, 2 = Female                   |
| `EDUCATION`        | 1 = Grad, 2 = Univ, 3 = High School     |
| `MARRIAGE`         | 1 = Married, 2 = Single, 3 = Others     |
| `AGE`              | Age of the customer                    |
| `PAY_0` to `PAY_6` | Past monthly repayment status           |
| `BILL_AMT1-6`      | Amount of bill statements              |
| `PAY_AMT1-6`       | Amount of previous repayments          |

### 🏷️ Target

`default payment next month`  
- `1` – Yes (Will default)  
- `0` – No (Will not default)

---

## ⚙️ End-to-End Architecture

### ✅ 1. Data Validation

- Filename check (date + timestamp)
- Schema matching (column names, count)
- Null value check
- Files split into:
  - `Good_Raw/`
  - `Bad_Raw/`

### 🛢️ 2. Data Ingestion

- Validated files inserted into **SQLite3 DB**
- Table name: `Good_Data`

### 🔄 3. Data Preprocessing

- Missing value imputation
- Standardization
- Correlation filtering

### 📊 4. Clustering

- KMeans applied
- Optimal `K` auto-selected using **KneeLocator**
- Each cluster treated as a separate dataset

### 🤖 5. Model Training

- Trained both **XGBoost** and **Naive Bayes** per cluster
- Selected the best based on **AUC score**
- Saved trained models per cluster

### 🔮 6. Prediction Flow

- Accepts **custom CSV path** or uses **default folder**
- Applies preprocessing and clustering
- Loads appropriate model based on cluster
- Outputs:
  - `Prediction_Output_File/Predictions.csv`
  - Preview returned on the web interface

---

## 🌐 Web UI Preview

![Web UI Preview](https://i.imgur.com/zA0Epv1.png) *(Replace with actual UI image if needed)*

- 📁 Upload CSV (custom or default)
- 📊 View prediction results
- 🗃️ Download final output file

---


---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **ML Models**: XGBoost, Naive Bayes
- **Clustering**: KMeans
- **DB**: SQLite3
- **Deployment**: Render.com
- **UI**: HTML, CSS, Bootstrap, jQuery

---

## 📌 Notes

- Ensure uploaded CSV files follow the required **schema format**.
- Invalid files are logged and archived automatically.
- Full prediction logs are stored in `Prediction_Logs/`.

---

