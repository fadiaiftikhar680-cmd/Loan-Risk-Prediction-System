# 🏦 Intelligent Loan Risk Prediction System

An end-to-end Machine Learning and Deep Learning web application powered by an **Artificial Neural Network (ANN)** model, featuring a FastAPI backend and a multi-page Streamlit frontend.

**Developed by:** [Fadia Iftikhar]

---

## 📁 Project Directory Structure

```text
LOAN_RISK_PREDICTION/
│
├── backend/
│   ├── __pycache__/
│   └── main.py              # FastAPI backend endpoints (/predict/single, /predict/batch)
│
├── frontend/
│   ├── pages/
│   │   ├── Batch_Prediction.py    # Multi-applicant CSV upload page
│   │   └── Single_Prediction.py   # Interactive single applicant form page
│   └── app.py                     # Streamlit Home Page
│
├── model_artifacts/
│   ├── label_encoders.pkl         # Categorical label encoders
│   ├── loan_risk_ann_model.keras  # Trained ANN model file
│   └── scaler.pkl                 # Feature scaling object
│
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation
## 🛠️ Prerequisites & Installation

* Clone or download this repository.
* Open your project folder in your terminal or **VS Code**.
* Install the required dependencies using pip:

```bash
pip install -r requirements.txt
## 🚀 How to Run the Project

You need to run both the Backend (FastAPI) and Frontend (Streamlit) concurrently in two separate terminal windows.

### Step 1: Start the FastAPI Backend
Navigate to the backend directory and start the server using Uvicorn:

```bash
cd backend
uvicorn main:app --reload
## 💡 Features

* **Home Page:** Overview of the credit risk assessment platform.
* **Single Prediction:** Interactive form to evaluate an individual loan applicant's risk score and probability.
* **Batch Prediction:** CSV file upload support to evaluate multiple applicants simultaneously with downloadable results.
