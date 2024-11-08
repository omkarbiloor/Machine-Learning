# Credit Card Defaulters Classification

## Problem Statement

The objective of this project is to build a classification methodology to determine whether a person will default on their credit card payment for the next month. The solution utilizes data processing, clustering, and advanced modeling techniques to predict defaults and support decision-making in financial risk assessment.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Architecture](#architecture)
- [Data Description](#data-description)
- [Data Validation](#data-validation)
- [Data Insertion in Database](#data-insertion-in-database)
- [Model Training](#model-training)
- [Prediction Process](#prediction-process)
- [Dependencies](#dependencies)
- [Usage](#usage)

---
## Architecture
The architecture for the credit card defaulter prediction system is organized into multiple stages, represented by a flowchart with interconnected processes. The key stages include:

Training Phase:

Start → Data (Batches) for Training → Data Validation → Data Transformation → Data Insertion in Database → Export Data from Database to CSV for Training.
Data Preprocessing → Data Clustering → Get Best Model for Each Cluster → Hyperparameter Tuning → Model Saving → Cloud Setup → Pushing App to Cloud.
Prediction Phase:

Application Start → Data from Client to be Predicted → Data Validation → Data Transformation → Data Insertion in Database → Export Data from Database to CSV for Prediction.
Data Preprocessing → Data Clustering → Model Call for Specific Cluster → Prediction → Export Prediction to CSV → END.

---

## Data Description

The data used in this project is provided in multiple sets of files by the client, typically extracted from the census bureau. It contains 32,561 instances with the following attributes:

### Features

- **LIMIT_BAL**: Credit Limit (continuous)
- **SEX**: Gender (Categorical: 1 = male; 2 = female)
- **EDUCATION**: Education level (Categorical: 1 = graduate school; 2 = university; 3 = high school; 4 = others)
- **MARRIAGE**: Marital status (1 = married; 2 = single; 3 = others)
- **AGE**: Age of the person (continuous)
- **PAY_0 to PAY_6**: Past payment history (monthly records from April to September 2005)
- **BILL_AMT1 to BILL_AMT6**: Amount of bill statements (six months)
- **PAY_AMT1 to PAY_AMT6**: Amount of previous payments (six months)

### Target Label

- **default payment next month**: Whether a person defaults on their credit card payment next month (Yes = 1, No = 0)

### Additional Requirements

Apart from the training files, a "schema" file is required containing:
- File names
- Length of date and time values in filenames
- Number of columns
- Names and data types of columns

---

## Data Validation

Validation is performed on training files as per specifications in the "schema" file, covering:

1. **Name Validation**: Validates file names using regex patterns. Files are moved to `Good_Data_Folder` if valid; otherwise, to `Bad_Data_Folder`.
2. **Number of Columns**: Validates that the number of columns matches the schema specification.
3. **Name of Columns**: Validates that column names match those in the schema.
4. **Datatype of Columns**: Ensures data types are as specified. Invalid files are moved to `Bad_Data_Folder`.
5. **Null Values in Columns**: If all values in a column are NULL, the file is moved to `Bad_Data_Folder`.

---

## Data Insertion in Database

1. **Database Creation and Connection**: Creates or connects to the specified database.
2. **Table Creation**: Creates a "Good_Data" table for validated files based on schema specifications.
3. **Data Insertion**: Inserts files from `Good_Data_Folder` into the table. Invalid files (due to data type issues) are moved to `Bad_Data_Folder`.

---

## Model Training

1. **Data Export from DB**: Data is exported from the database as a CSV file for model training.
2. **Data Preprocessing**:
   - Handle null values using a categorical imputer.
   - Scale numeric values using a standard scaler.
   - Check for correlation among features.
3. **Clustering**:
   - Uses KMeans for clustering.
   - Optimal number of clusters is selected using the Elbow Plot and the `KneeLocator` function.
4. **Model Selection**:
   - For each cluster, "Naïve Bayes" and "XGBoost" models are trained.
   - Hyperparameter tuning is performed using GridSearch.
   - The best-performing model (based on AUC score) is saved for each cluster.

---

## Prediction Process

1. **Data Export from DB**: Prediction data is exported from the database as a CSV file.
2. **Data Preprocessing**:
   - Handle null values using a categorical imputer.
   - Scale numeric values.
   - Check for correlation.
3. **Clustering**:
   - Uses the pre-trained KMeans model to predict clusters for the data.
4. **Prediction**:
   - Loads the best model for each cluster to make predictions.
   - Saves predictions as a CSV file at a specified location.

---

## Dependencies

- Python 3.x
- pandas
- numpy
- scikit-learn
- XGBoost
- matplotlib
- SQLAlchemy

---

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/omkarbiloor/credit-card-defaulters.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run data validation, preprocessing, training, and prediction as per instructions in `src/`.

---

