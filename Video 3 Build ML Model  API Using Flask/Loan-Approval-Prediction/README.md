# 🏦 Loan Approval Prediction

A machine learning project that predicts whether a loan application will be **Approved** or **Rejected** based on an applicant's financial and demographic information. The project includes an end-to-end ML pipeline and a Flask web application for real-time predictions.

## ✨ Features

- 📊 Exploratory Data Analysis (EDA)
- 🧹 Data Cleaning & Preprocessing
- 🔠 Categorical Feature Encoding
- 📈 Outlier Handling using IQR
- ⚖️ Class Imbalance Handling with SMOTE
- 🤖 Random Forest & Logistic Regression Models
- 📋 Model Evaluation (Accuracy, Precision, Recall, F1-Score)
- 🌐 Flask-based Web Application for Predictions

---

## 🛠️ Tech Stack

- Python
- Pandas & NumPy
- Matplotlib & Seaborn
- Scikit-learn
- imbalanced-learn (SMOTE)
- Flask
- HTML & CSS

---

## 📂 Project Structure

```text
loan-approval-prediction/
│
├── models/
│   ├── loan_model.pkl
│   ├── education_encoder.pkl
│   ├── employment_encoder.pkl
│   ├── target_encoder.pkl
│   └── feature_names.pkl
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── .gitignore
├── app.py                     # Flask web application
├── data.csv                   # Loan approval dataset
├── final_report.md            # Project analysis & findings
├── loan_approval_prediction.ipynb   # EDA, preprocessing & model training
├── README.md
└── requirements.txt
```
---

## 📈 Model Performance

| Model | Accuracy |
|--------|---------:|
| Random Forest | **98.2%** |
| Logistic Regression | 81% |

### Key Insights

- ✅ Random Forest achieved **98.2% accuracy**.
- 💳 **CIBIL Score** is the most influential feature.
- ⚖️ SMOTE improved learning on the minority class.
- 📉 Random Forest significantly outperformed Logistic Regression.

---

## 🖥️ Web Application

The project includes a Flask-based web interface where users can:

- Enter applicant details
- Predict loan approval in real time
- Load a pre-trained machine learning model without retraining

---

## 🚀 Future Improvements

- Hyperparameter tuning
- Model explainability with SHAP
- Docker support
- REST API with prediction endpoint
- Unit & integration testing

---

## 👨‍💻 Author

**Asadullah**  
AI/ML Engineer | MLOps | Kaggle Grandmaster 
