import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Loan Risk Prediction System", page_icon="💳", layout="wide")

st.title("💳 Intelligent Loan Risk Prediction System")
st.write("Select the prediction mode from the sidebar below.")

# Sidebar navigation for Single or Batch
app_mode = st.sidebar.selectbox("Choose Prediction Mode", ["Single Prediction", "Batch Prediction"])

# ----------------- SINGLE PREDICTION -----------------
if app_mode == "Single Prediction":
    st.header("👤 Single Loan Applicant Risk Assessment")
    st.write("Enter the applicant's details below to check their credit risk status.")

    with st.form("single_prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            income = st.number_input("Income", min_value=0, value=5000000, step=10000)
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            experience = st.number_input("Experience (Years)", min_value=0, max_value=50, value=5)
            current_job_yrs = st.number_input("Current Job Years", min_value=0, max_value=50, value=3)
            
        with col2:
            current_house_yrs = st.number_input("Current House Years", min_value=0, max_value=50, value=2)
            married_single = st.selectbox("Marital Status", ["single", "married"])
            house_ownership = st.selectbox("House Ownership", ["rented", "owned", "norent_noown"])
            car_ownership = st.selectbox("Car Ownership", ["yes", "no"])
            
        profession = st.text_input("Profession", value="Software_Developer")
        
        submit_button = st.form_submit_button(label="Predict Risk")

    if submit_button:
        payload = {
            "Income": income,
            "Age": age,
            "Experience": experience,
            "CURRENT_JOB_YRS": current_job_yrs,
            "CURRENT_HOUSE_YRS": current_house_yrs,
            "Married_Single": married_single,
            "House_Ownership": house_ownership,
            "Car_Ownership": car_ownership,
            "Profession": profession
        }
        
        try:
            response = requests.post("https://loan-risk-prediction-system-production.up.railway.app/predict/single", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                st.markdown("---")
                st.subheader("Prediction Results")
                
                risk_flag = result["risk_flag"]
                if risk_flag == "High Risk":
                    st.error(f"**Risk Status:** {risk_flag}")
                else:
                    st.success(f"**Risk Status:** {risk_flag}")
                    
                st.metric(label="Risk Probability", value=f"{result['risk_percentage']}%")
                st.write(f"**Recommendation:** {result['recommendation']}")
            else:
                st.error(f"Error from server: {response.json().get('detail', 'Unknown error')}")
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI backend.")

# ----------------- BATCH PREDICTION -----------------
elif app_mode == "Batch Prediction":
    st.header("📂 Batch Loan Risk Prediction")
    st.write("Upload a CSV file containing multiple applicant profiles to get bulk risk evaluations.")

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file is not None:
        df_preview = pd.read_csv(uploaded_file)
        st.write("### Uploaded Data Preview:")
        st.dataframe(df_preview.head())
        
        if st.button("Process Batch Predictions"):
            with st.spinner("Processing predictions through backend..."):
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                
                try:
                    response = requests.post("https://loan-risk-prediction-system-production.up.railway.app/predict/batch", files=files)
                    
                    if response.status_code == 200:
                        res_data = response.json()
                        result_df = pd.DataFrame(res_data["data"])
                        
                        st.success(f"Successfully processed {res_data['total_records']} records!")
                        st.write("### Results:")
                        st.dataframe(result_df)
                        
                        csv_data = result_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Results as CSV",
                            data=csv_data,
                            file_name="loan_risk_predictions.csv",
                            mime="text/csv"
                        )
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the FastAPI backend.")