import json
import requests
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go

#------------Title------------------
st.markdown("<h1 style='text-align: center; color: black;'>Default Detective</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Predict if a loan will be paid in full or not</h2>", unsafe_allow_html=True)

#----------Option tab---------------
selected2 = option_menu(None, ["Predict", "Data", "About"], 
    icons=['search', 'database', 'person'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

#---------About section-------------
if selected2 == "About":
    st.write("# About")
    st.image("static/images/money.jpeg")
    
#------------Sidebar----------------

st.sidebar.header("Input Features for Loan")

# Startup or established company?
companyAge = ["Startup", "Established Business"]
isStartup = st.sidebar.selectbox("Is the business a startup or an established company?", companyAge)

# Mortgage or real estate-backed loan?
security = ["Real Estate", "Mortgage"]
isBacked = st.sidebar.selectbox("Is this a mortgage or real estate-backed loan?", security)

# Active or not active during recession?
recessionState = ["Active", "Not Active"]
wasActive = st.sidebar.selectbox("Was the loan active during recession of 2007-2009?", recessionState)

# NAICS code
naics_code = st.sidebar.number_input("Industry (NAICS code)", min_value=11, max_value=92)
st.sidebar.markdown("[NAICS CODE LIST](https://www.census.gov/naics/?58967?yearbck=2022)")

# Number of employees
no_emp = st.sidebar.number_input("How many employees does the business have?", min_value=0, max_value=9945)

# Amounts
disb_gross = st.sidebar.number_input("What is the disbursed amount in $")

# Gross amount of loan approved by bank
grappv_gross = st.sidebar.number_input("What is gross amount approved by the bank in $?")

# SBA's guaranteed amount of approved loan
sba_appv = st.sidebar.number_input("What is SBA's guaranteed amount of approved loan in $?")

# Loan term in months
term = st.sidebar.slider("What is the Loan term in months?", min_value=0, max_value=527)

#---------------Prediction----------------
if selected2 == "Predict":
    st.image("static/images/pred2.jpeg")
    
    # Prediction button
    prediction = st.button("Get Predictions", use_container_width=True)

    if prediction:
        
        data = {
                'NAICS_code': naics_code,
                'Term': term,
                'NoEmp':no_emp,
                'New': 1 if isStartup == "Startup" else 0,
                'DisbursementGross':disb_gross,
                'GrAppv':grappv_gross,
                'SBA_Appv':sba_appv,
                'Recession': 1 if wasActive == "Active" else 0, 
                'RealEstate':1 if isBacked == "Real Estate" else 0,
                'SBA_Guaranteed_Portion': (sba_appv/grappv_gross)
                }
        
        st.write("### Loan Details:")
        st.markdown(f"""
                    <ol style='text-align: left; color: black;'>
                        <li>Industry(NAICS code): {naics_code}</li>
                        <li>Loan term in months: {term}</li>
                        <li>Number of Business Employees: {no_emp}</li>
                        <li>Startup or Established Business: {isStartup}</li>
                        <li>Amount Disbursed [$]: {disb_gross}</li>
                        <li>Gross Amount of Loan Approved by Bank [$]: {grappv_gross}</li>
                        <li>SBA's Guaranteed Amount of Approved Loan [$]: {sba_appv}</li>
                        <li>State of Loan During Recession (2007-2009): {wasActive}</li>
                        <li>Mortage or Real-Estate Backed: {isBacked}</li>
                        <li>SBA Guaranteed Portion: {(sba_appv/grappv_gross)}</li>
                    </ol>""",
                    unsafe_allow_html=True)

        # API call
        post_rest = requests.post("http://127.0.0.1:8000/inferece", json = data)
        rest_str = json.dumps(post_rest.json())
        response = json.loads(rest_str)

        #-----------------Output-------------------
        barcolour = "green"
        if response["score"] < 90 and response["score"] >= 75:
            barcolour = "orange"
        elif response["score"] < 75:
            barcolour = "red"
            
        status = response["status"]   
        
        # Score
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = response["score"],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Score", 'font': {'size': 24}},
            gauge = {
                'axis': {'range': [0, 100],},
                'bar': {'color': barcolour},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "white",
                'threshold': {
                    'line': {'color': "green", 'width': 4},
                    'thickness': 0.75,
                    'value': 99.9}}))

        st.plotly_chart(fig)
        st.markdown(f"<h2 style='text-align: center; color: black;'>Status: {status}</h2>", unsafe_allow_html=True)