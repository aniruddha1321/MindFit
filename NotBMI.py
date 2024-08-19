import streamlit as st
import pandas as pd
from fpdf import FPDF as fpdf
import base64
from io import BytesIO

# Set page config
st.set_page_config(page_title="BMI Calculator", layout="centered")

# Custom CSS to improve the app's appearance based on theme
st.markdown("""
<style>
    /* Default light mode styles */
    .stApp {
        background-color: #f0f8ff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        color: black;
    }

    /* Dark mode adjustments */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #1e1e1e;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stTextInput>div>div>input {
            background-color: #333333;
            color: white;
        }
    }
</style>
""", unsafe_allow_html=True)

# App title
st.title("BMI Calculator")

# Input fields
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=1, max_value=120, step=1)
gender = st.selectbox("Select your gender", ["Male", "Female", "Other"])
weight = st.number_input("Enter your weight (kg)", min_value=1.0, max_value=500.0, step=0.1)
height = st.number_input("Enter your height (cm)", min_value=1.0, max_value=300.0, step=0.1)

# Calculate BMI
if st.button("Calculate BMI"):
    bmi = weight / ((height / 100) ** 2)
    
    st.subheader("Your BMI Results")
    st.write(f"Name: {name}")
    st.write(f"Age: {age}")
    st.write(f"Gender: {gender}")
    st.write(f"Weight: {weight:.1f} kg")
    st.write(f"Height: {height:.1f} cm")
    st.write(f"BMI: {bmi:.2f}")
    
    # BMI category
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    st.write(f"Category: {category}")
    
    # Create a PDF receipt
    def create_download_link(val, filename):
        b64 = base64.b64encode(val)
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download PDF</a>'

    def create_pdf(name, age, gender, weight, height, bmi, category):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="BMI Calculation Receipt", ln=1, align="C")
        pdf.cell(200, 10, txt=f"Name: {name}", ln=1)
        pdf.cell(200, 10, txt=f"Age: {age}", ln=1)
        pdf.cell(200, 10, txt=f"Gender: {gender}", ln=1)
        pdf.cell(200, 10, txt=f"Weight: {weight:.1f} kg", ln=1)
        pdf.cell(200, 10, txt=f"Height: {height:.1f} cm", ln=1)
        pdf.cell(200, 10, txt=f"BMI: {bmi:.2f}", ln=1)
        pdf.cell(200, 10, txt=f"Category: {category}", ln=1)
        return pdf.output(dest="S").encode("latin-1")
    
    # Generate PDF and create download link
    pdf = create_pdf(name, age, gender, weight, height, bmi, category)
    html = create_download_link(pdf, "BMI_receipt")
    st.markdown(html, unsafe_allow_html=True)

# Add some information about BMI
st.sidebar.header("About BMI")
st.sidebar.write("""
Body Mass Index (BMI) is a simple way to measure body fat based on height and weight that applies to adult men and women.

BMI Categories:
- Underweight: < 18.5
- Normal weight: 18.5 - 24.9
- Overweight: 25 - 29.9
- Obese: ≥ 30

Please note that BMI is not a perfect measure and doesn't account for factors like muscle mass, bone density, and overall body composition.
""")
