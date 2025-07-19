# Credit Card Defaulters Prediction - DefaulterInsight 💳📉

A machine learning solution to classify whether a person will default on their credit card payment for the next month. The system accepts batch input files, performs data validation, preprocessing, clustering, and model prediction to provide insights on customer credit risk.

### 🔗 Deployed App:
**Web App** 👉 [https://machine-learning-b4qq.onrender.com](https://machine-learning-b4qq.onrender.com)

---

## 🧠 Problem Statement

Build a classification model that predicts whether a person will default on credit card payment for the upcoming month based on historical financial records.

---

## 🧾 Input Dataset

The dataset contains **32,561** entries with the following features:

| Feature Name | Description |
|--------------|-------------|
| `LIMIT_BAL` | Credit Limit (Continuous) |
| `SEX` | 1 = Male, 2 = Female |
| `EDUCATION` | 1 = Graduate, 2 = University, 3 = High School, 4 = Others |
| `MARRIAGE` | 1 = Married, 2 = Single, 3 = Others |
| `AGE` | Age of the person |
| `PAY_0 to PAY_6` | Past monthly payment records |
| `BILL_AMT1 to BILL_AMT6` | Amount of bill statements |
| `PAY_AMT1 to PAY_AMT6` | Amount of previous payments |

**Target:**
- `default payment next month`: `1 = Yes`, `0 = No`

---

## 📊 Project Architecture

### 1. 🔎 Data Validation

Performed on training and prediction files using a **schema file**, including:

- **Filename** format & length checks
- **Number of columns**
- **Column names & data types**
- **Missing/null values**

Valid files → `Good_Data_Folder`  
Invalid files → `Bad_Data_Folder`

---

### 2. 🛢️ Database Operations

- Create/open database
- Create or reuse `Good_Data` table
- Insert valid files into DB

---

### 3. 🧪 Model Training Pipeline

- **Export Data from DB**
- **Preprocessing:**
  - Null value imputation
  - Standard scaling
  - Correlation check
- **Clustering:**
  - KMeans with `KneeLocator` for optimal cluster count
- **Model Selection:**
  - Naive Bayes and XGBoost trained for each cluster
  - Select best model based on AUC score

---

### 4. 🔮 Prediction Workflow

- Accept user-uploaded files or use default path
- Apply same preprocessing as training
- Predict cluster using saved KMeans model
- Load the appropriate model for each cluster
- Save predictions with IDs to CSV and return path

---

## 🖥️ Deployment Instructions

This project is deployed on **Render.com** (can also be deployed to Heroku):

1. Create `Procfile`:

2. Generate `requirements.txt`:
```bash
pip freeze > requirements.txt
Initialize Git & Push:

bash
Copy
Edit
git init
heroku login
heroku create <your-app-name>
git add .
git commit -am "Initial Commit"
git push heroku master
📂 Folder Structure
pgsql
Copy
Edit
├── Training_Batch_Files/
├── Prediction_Batch_Files/
├── Good_Raw/
├── Bad_Raw/
├── artifacts/
│   ├── models/
│   ├── predictions/
│   └── cluster_models/
├── main.py
├── templates/
│   └── index.html
├── static/
├── trainingModel.py
├── predictionFromModel.py
├── schema_training.json
├── schema_prediction.json
└── README.md
🧪 Tech Stack
Python

Flask

Gunicorn

XGBoost

Naive Bayes

KMeans Clustering

SQL/SQLite3

HTML/CSS + Bootstrap

Render.com / Heroku

⚠️ Note
All inputs must follow schema-based format for successful processing.

Invalid files are segregated and logged for user review.

📌 Credits
Project built and maintained by Omkar Biloor

