# 💧 Water Potability Prediction System

## 📌 Overview
This project is an end-to-end **Machine Learning application** that predicts whether water is safe for drinking based on physicochemical properties.  
It also includes an **interactive web dashboard** built using Streamlit for real-time prediction and visualization.

---

## 🚀 Features
- Real-time water quality prediction using ML model  
- Interactive dashboard with dynamic input sliders  
- pH level visualization with safety indicator  
- Confidence score and probability distribution graph  
- Hybrid validation system (Machine Learning + rule-based checks)  

---

## 🧠 Machine Learning Details
- Model Type: Classification Model  
- Preprocessing: StandardScaler  
- Input Features:  
  - pH  
  - Hardness  
  - Solids  
  - Chloramines  
  - Sulfate  
  - Conductivity  
  - Organic Carbon  
  - Trihalomethanes  
  - Turbidity  

---

## 🛠️ Tech Stack
- Python  
- NumPy  
- Scikit-learn  
- Matplotlib  
- Streamlit  

---

## 📊 How It Works
1. User inputs water quality parameters  
2. Data is scaled using StandardScaler  
3. ML model predicts water potability  
4. Additional rule-based checks validate safety  
5. Results displayed with confidence score and visualizations  

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
