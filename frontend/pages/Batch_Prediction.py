import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Batch Prediction", page_icon="📂", layout="wide")

st.title("📂 Batch Loan Risk Prediction")
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
                response = requests.post("http://127.0.0.1:8000/predict/batch", files=files)
                
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