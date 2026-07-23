import streamlit as st
import requests

st.set_page_config(page_title="Single Prediction", page_icon="👤", layout="centered")

st.title("👤 Single Loan Applicant Risk Assessment")
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
        st.error("Could not connect to the FastAPI backend. Make sure your FastAPI server is running.")