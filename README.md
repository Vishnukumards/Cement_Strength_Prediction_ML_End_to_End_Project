# 🏗️ Cement_Strength_Prediction_ML_End_to_End_Project

A machine learning-powered web application for predicting concrete compressive strength based on composition parameters and age.  
Built with **FastAPI**, **Streamlit**, and **XGBoost**.

![Project Status](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python Version](https://img.shields.io/badge/Python-3.9-blue)
![ML Framework](https://img.shields.io/badge/ML-XGBoost-orange)

---

## 🌐 Live Demo

- **Web Application**: [https://cement-strength-app-kxqx.onrender.com](https://cement-strength-app-kxqx.onrender.com)  
- **API Documentation**: [https://cement-strength-api-utch.onrender.com/docs](https://cement-strength-api-utch.onrender.com/docs)  
- **API Health Check**: [https://cement-strength-api-utch.onrender.com/health](https://cement-strength-api-utch.onrender.com/health)

---

## 📊 Project Overview

This project predicts the **compressive strength of concrete (in MPa)** based on its composition and age using machine learning.  
The model achieves **89% accuracy (R² score)** with an **RMSE of 4.23 MPa**.

### Key Features
- 🎯 **Accurate Predictions** – XGBoost model with 89% R² score  
- 🌐 **Web Interface** – User-friendly Streamlit frontend  
- 🔧 **REST API** – Fully documented FastAPI backend  
- 📈 **Smart Validation** – Water-cement ratio and strength classification  
- 🧪 **Test Scenarios** – Pre-built concrete mix examples  
- 📊 **Mix Design Insights** – Ratio and performance breakdown  
- 🚀 **Production Ready** – CI/CD deployment via Render  

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** – Modern async web framework  
- **XGBoost** – ML regression model  
- **Pydantic** – Data validation  
- **Uvicorn** – ASGI server  

### Frontend
- **Streamlit** – Interactive web interface  
- **Plotly** – Data visualization  
- **Pandas** – Data manipulation  

### Deployment
- **Render.com** – Cloud hosting  
- **GitHub** – Version control & CI/CD  

---

## 📁 Project Structure

```plaintext
cement_strength_predictor/
├── app/                     # FastAPI backend
│   ├── main.py              # API server and endpoints
│   └── ...
│
├── streamlit_app/           # Streamlit frontend
│   ├── app.py               # Web application
│   └── ...
│
├── src/                     # Core functionality
│   ├── predict.py           # Prediction logic
│   ├── schemas.py           # Pydantic models
│   └── ...
│
├── models/                  # Trained ML models
│
├── tests/                   # Test suite
│
├── notebooks/               # Jupyter notebooks for EDA
│
├── requirements.txt          # Python dependencies
├── render.yaml               # Render deployment config
├── runtime.txt               # Python version specification
└── README.md                 # Project documentation
````

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Vishnukumards/Cement_Strength_Prediction_ML_End_to_End_Project.git
cd Cement_Strength_Prediction_ML_End_to_End_Project
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Start the Backend API

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Start the Frontend (in a new terminal)

```bash
streamlit run streamlit_app/app.py
```

### 6. Access the Application

* **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Web App**: [http://localhost:8501](http://localhost:8501)

---

## 📊 Model Performance

| Metric        | Value                                |
| ------------- | ------------------------------------ |
| **Algorithm** | XGBoost Regressor                    |
| **R² Score**  | 0.89                                 |
| **RMSE**      | 4.23 MPa                             |
| **Features**  | 11 parameters (8 raw + 3 engineered) |
| **Target**    | Concrete compressive strength (MPa)  |

---

## 🎯 Usage Examples

### Example Input (High-Strength Concrete)

```json
{
  "Cement (component 1)(kg in a m^3 mixture)": 102,
  "Blast Furnace Slag (component 2)(kg in a m^3 mixture)": 359.4,
  "Fly Ash (component 3)(kg in a m^3 mixture)": 200.1,
  "Water  (component 4)(kg in a m^3 mixture)": 121.75,
  "Superplasticizer (component 5)(kg in a m^3 mixture)": 32.2,
  "Coarse Aggregate  (component 6)(kg in a m^3 mixture)": 801,
  "Fine Aggregate (component 7)(kg in a m^3 mixture)": 594,
  "Age (day)": 0
}
```

### Strength Classification

| Class       | Range (MPa) | Typical Use           |
| ----------- | ----------- | --------------------- |
| **C12/15**  | < 20        | Non-structural        |
| **C25/30**  | 25–30       | General construction  |
| **C30/37**  | 30–37       | Reinforced structures |
| **C40/50**  | 40–50       | High-rise buildings   |
| **C50/60+** | > 50        | Special structures    |

---

## 🚀 Deployment

The project is deployed on **Render.com** with:

* Automatic CI/CD from GitHub
* Zero-downtime deployments
* Automatic HTTPS/SSL
* Environment variable management
* Health checks and monitoring

### Health Check

```bash
curl https://cement-strength-api-utch.onrender.com/health
```

### Prediction Test

```bash
curl -X POST https://cement-strength-api-utch.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Cement (component 1)(kg in a m^3 mixture)": 540.0,
    "Blast Furnace Slag (component 2)(kg in a m^3 mixture)": 0.0,
    "Fly Ash (component 3)(kg in a m^3 mixture)": 0.0,
    "Water  (component 4)(kg in a m^3 mixture)": 162.0,
    "Superplasticizer (component 5)(kg in a m^3 mixture)": 2.5,
    "Coarse Aggregate  (component 6)(kg in a m^3 mixture)": 1040.0,
    "Fine Aggregate (component 7)(kg in a m^3 mixture)": 676.0,
    "Age (day)": 28
  }'
```

---

## 📈 Model Training

The **XGBoost** model was trained with:

* Domain-specific feature engineering (e.g., water-cement ratio)
* Cross-validation for robustness
* Hyperparameter tuning for accuracy
* Multiple evaluation metrics for validation

---

## ❤️ Built With

* **Python**
* **FastAPI**
* **Streamlit**
* **XGBoost**

> Predicting stronger concrete, building better futures 🏗️✨

---

## 💾 How to Use This README

1. Copy the entire content above
2. Create a new file named `README.md` in your project root
3. Paste the content
4. Save and commit to GitHub

---

## 🎯 Key Sections Included

* ✅ Project overview with badges
* ✅ Live demo links
* ✅ Tech stack breakdown
* ✅ Installation guide
* ✅ API + frontend setup
* ✅ Deployment instructions
* ✅ Test examples
* ✅ Model details
* ✅ Strength classification

---

**Author:** Vishnu Kumar D S

**Repository:** [GitHub - Cement Strength Prediction Project](https://github.com/Vishnukumards/Cement_Strength_Prediction_ML_End_to_End_Project)


