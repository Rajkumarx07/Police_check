# 🚓 SecureCheck: A Python-SQL Digital Ledger for Police Post Logs

## 📌 Project Description

SecureCheck is a real-time digital dashboard for police traffic stop monitoring and analysis. It replaces manual logbooks by connecting a cleaned dataset (via Jupyter Notebook) to a live MySQL database, with a frontend built using Streamlit. The app provides insights, live SQL query execution, and a prediction system based on past traffic stop data.

---

## 🚀 Features

* 📊 Real-time Metrics: Total Stops, Arrests, Searches, Drug-Related Stops
* 📁 Query Explorer: 20+ categorized SQL query options with instant visual results
* 📈 Interactive Charts: Pie, Bar, Line using Plotly
* 🧠 Predictive Module: Predicts Stop Outcome and Violation Type based on user input
* 🌐 Live SQL Integration: Every query runs directly on MySQL
* 🧹 Cleaned Dataset: Preprocessed using Jupyter Notebook (pandas)

---

## 🧰 Technologies Used

* Python 3.x
* Streamlit
* MySQL
* pandas
* Plotly Express
* Jupyter Notebook

---

## 🗃️ Project Structure

```
SecureCheck/
├── Police_check.py          # Main Streamlit App
├── Police_check.ipynb       # Data cleaning & transformation
├── requirements.txt         # Python dependencies (optional)
├── README.md                # Project Documentation
```

---

## ⚙️ How to Run

1. **Start MySQL Server** (e.g., XAMPP)
2. **Create Database & Table**

   ```sql
   CREATE DATABASE TS;
   -- Create table and insert cleaned data from `Police_check.ipynb`
   ```
3. **Install Dependencies**

   ```bash
   pip install streamlit mysql-connector-python pandas plotly
   ```
4. **Run the App**

   ```bash
   streamlit run Police_check.py
   ```

---

## 🔍 Pages Overview

### 1. Home

* Project introduction, objectives, and feature list

### 2. Overview

* Metrics: Total Stops, Arrests, etc.
* Dataset display
* Charts: Daily Arrests, Arrest Rate by Country, Drug Stops by Gender

### 3. Query Explorer

* 20 predefined live SQL queries
* Covers time, demographics, vehicle patterns, violations
* Results shown using Streamlit DataFrame

### 4. Prediction Module

* User fills form with details
* Based on historical match, predicts outcome & violation type

---

## 🖼️ Screenshots (Add Manually)

* Dashboard Overview
* Query Dropdown & Results
* Prediction Summary Output

---

## 📈 Future Improvements

* ML-based advanced prediction
* Cloud MySQL integration (AWS RDS)
* Role-based access control (officer login)
* Upload new logs directly via UI
* Error handling and validation improvements

---

## 👨‍💻 Developed By

**Rajkumar**
Final Project for Live Evaluation (GUVI / Internship / Academic)

---

> "Stay secure. Stay accountable."
