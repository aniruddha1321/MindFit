import streamlit as st
import google.generativeai as genai
import requests

# Google Gemini AI API Key
API_KEY = "AIzaSyB1Isus048X-roH-iK4JR_e9y5Xk6mAsec"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Nutritionix API credentials
app_id = 'f9f1895e'
api_key = 'c8cdaff4b8d656b4b7f9d0e53405f424'

def calculate_bmi(weight, height):
    height_m = height / 100  # converting height to meters
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def generate_diet_plan(bmi, diet_preference, name, age, gender):
    # Construct the prompt for the Gemini AI model
    prompt = (
        f"Hi, {name}! Based on the following details:\n"
        f"Age: {age}\n"
        f"Gender: {gender}\n"
        f"BMI: {bmi}\n"
        f"Diet Preference: {diet_preference}\n\n"
        f"Please provide a personalized diet plan that is nutritionally balanced "
        f"and suitable for their health status. Include specific food items and meals."
    )

    # Generate the response using Gemini AI
    response = model.generate_content(prompt)
    
    return response.text

def get_nutritional_info(food_item):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": app_id,
        "x-app-key": api_key,
        "Content-Type": "application/json"
    }
    body = {
        "query": food_item,
        "timezone": "US/Eastern"
    }
    
    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data['foods']:
            food = data['foods'][0]
            return {
                "calories": food.get('nf_calories'),
                "protein": food.get('nf_protein'),
                "carbohydrates": food.get('nf_total_carbohydrate'),
                "fat": food.get('nf_total_fat')
            }
        else:
            return None
    else:
        return None

def main():
    # Welcome Note
    st.title("BMI & Diet Recommender")
    st.write("Welcome to the BMI & Diet Recommender App! This app calculates your BMI and provides a personalized diet plan based on your details. You can also check the nutritional content of various food items.")

    # Sidebar Calorie Counter
    st.sidebar.header("Nutritional Information")
    food_item = st.sidebar.text_input("Enter food item:")
    if st.sidebar.button("Get Nutritional Info"):
        if food_item:
            nutrition = get_nutritional_info(food_item)
            if nutrition:
                st.sidebar.write(f"**{food_item.title()}**")
                st.sidebar.write(f"Calories: {nutrition['calories']} kcal")
                st.sidebar.write(f"Protein: {nutrition['protein']} g")
                st.sidebar.write(f"Carbohydrates: {nutrition['carbohydrates']} g")
                st.sidebar.write(f"Fat: {nutrition['fat']} g")
            else:
                st.sidebar.write("Sorry, don’t have nutritional information for that.")
        else:
            st.sidebar.write("Please enter a food item.")

    # Main app inputs
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=1, max_value=120, step=1)
    gender = st.selectbox("Select your gender", ["Male", "Female", "Other"])
    weight = st.number_input("Enter your weight (kg)", min_value=1.0, step=0.1)
    height = st.number_input("Enter your height (cm)", min_value=50.0, step=0.1)
    diet_preference = st.selectbox("Do you prefer a vegetarian or non-vegetarian diet?", ["Veg", "Non-Veg"])
    
    if st.button("Calculate BMI and Get Diet Plan"):
        if name and age and weight and height and diet_preference:
            # Calculate BMI
            bmi = calculate_bmi(weight, height)
            st.write(f"Hello {name}, your BMI is: {bmi}")
            
            # Generate a personalized diet plan
            diet_plan = generate_diet_plan(bmi, diet_preference, name, age, gender)
            st.write(diet_plan)
        else:
            st.write("Please fill in all the details.")

if __name__ == "__main__":
    main()
