import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Loan Risk Prediction System", page_icon="💳", layout="wide")

st.title("💳 Intelligent Loan Risk Prediction System")
st.write("Professional Credit Risk Assessment Dashboard powered by Artificial Neural Networks.")

# Professional Sidebar Navigation
app_mode = st.sidebar.radio("Navigation Menu", ["Single Prediction", "Batch Prediction"])

# ----------------- SINGLE PREDICTION PAGE -----------------
if app_mode == "Single Prediction":
    st.header("👤 Single Loan Applicant Risk Assessment")
    st.write("Enter individual applicant details below to analyze risk profile and probability distribution.")

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
        
        submit_button = st.form_submit_button(label="Analyze Applicant Risk")

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
                st.subheader("Assessment Results")
                
                risk_flag = result["risk_flag"]
                prob_pct = result["risk_percentage"]
                
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    if risk_flag == "High Risk":
                        st.error(f"**Risk Status:** {risk_flag}")
                    else:
                        st.success(f"**Risk Status:** {risk_flag}")
                    st.metric(label="Default Probability", value=f"{prob_pct}%")
                    st.write(f"**Recommendation:** {result['recommendation']}")
                
                with res_col2:
                    # Professional Gauge / Bar Chart for Single Prediction
                    chart_data = pd.DataFrame({
                        "Metric": ["Risk Probability", "Safety Margin"],
                        "Percentage": [prob_pct, 100 - prob_pct]
                    })
                    fig = px.bar(
                        chart_data, 
                        x="Percentage", 
                        y="Metric", 
                        orientation="h", 
                        title="Risk vs Safety Breakdown",
                        text="Percentage",
                        color="Metric",
                        color_discrete_map={"Risk Probability": "#ff4b4b", "Safety Margin": "#00CC96"}
                    )
                    fig.update_layout(xaxis_range=[0, 100], showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"Error from server: {response.json().get('detail', 'Unknown error')}")
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI backend.")

# ----------------- BATCH PREDICTION PAGE -----------------
elif app_mode == "Batch Prediction":
    st.header("📂 Batch Loan Risk Prediction & Analytics")
    st.write("Upload a CSV file containing multiple applicant records for bulk evaluation and visual analytics.")

    uploaded_file = st.file_uploader("Upload Batch CSV File", type=["csv"])

    if uploaded_file is not None:
        df_preview = pd.read_csv(uploaded_file)
        st.write("### Uploaded Data Preview:")
        st.dataframe(df_preview.head())
        
        if st.button("Process Batch Predictions"):
            with st.spinner("Processing batch records through neural network backend..."):
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                
                try:
                    response = requests.post("https://loan-risk-prediction-system-production.up.railway.app/predict/batch", files=files)
                    
                    if response.status_code == 200:
                        res_data = response.json()
                        result_df = pd.DataFrame(res_data["data"])
                        
                        st.success(f"Successfully processed {res_data['total_records']} records!")
                        
                        # Professional Visualizations
                        st.markdown("---")
                        st.subheader("📊 Batch Analytics Dashboard")
                        
                        graph_col1, graph_col2 = st.columns(2)
                        
                        with graph_col1:
                            # Pie Chart for Risk Distribution
                            risk_counts = result_df['Risk_Flag'].value_counts().reset_index()
                            risk_counts.columns = ['Risk_Flag', 'Count']
                            fig_pie = px.pie(
                                risk_counts, 
                                names='Risk_Flag', 
                                values='Count', 
                                title="Overall Risk Distribution Ratio",
                                hole=0.4,
                                color='Risk_Flag',
                                color_discrete_map={'High Risk': '#ff4b4b', 'Low Risk': '#00CC96'}
                            )
                            st.plotly_chart(fig_pie, use_container_width=True)
                            
                        with graph_col2:
                            # Histogram for Probability Spread
                            fig_hist = px.histogram(
                                result_df, 
                                x='Risk_Probability (%)', 
                                nbins=20, 
                                title="Risk Probability Distribution Spread",
                                color_discrete_sequence=['#636EFA']
                            )
                            st.plotly_chart(fig_hist, use_container_width=True)

                        st.write("### Detailed Result Records:")
                        st.dataframe(result_df)
                        
                        csv_data = result_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Full Results as CSV",
                            data=csv_data,
                            file_name="loan_risk_batch_predictions.csv",
                            mime="text/csv"
                        )
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the FastAPI backend.")