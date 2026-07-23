import streamlit as st

st.set_page_config(
    page_title="Loan Risk Prediction System",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Intelligent Loan Risk Prediction System")
st.write("Welcome to the ANN-powered Credit Risk Assessment platform.")

st.markdown("---")

st.subheader("Overview")
st.write("""
This application uses an advanced **Artificial Neural Network (ANN)** model to predict whether a loan applicant falls into a **High Risk** or **Low Risk** category based on their demographic and financial profile.
""")

col1, col2 = st.columns(2)

with col1:
    st.info("### 👤 Single Prediction")
    st.write("Evaluate an individual applicant by filling out a simple interactive form.")

with col2:
    st.success("### 📂 Batch Prediction")
    st.write("Upload a CSV file containing multiple applicant records to process batch predictions instantly.")

st.markdown("---")
st.markdown("Use the sidebar on the left to navigate between pages.")