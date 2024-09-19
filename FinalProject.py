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

def generate_diet_plan(bmi, diet_preference, name, age, gender, additional_input=None):
    # Construct the prompt for the Gemini AI model
    prompt = (
        f"Hi, {name}! Based on the following details:\n"
        f"Age: {age}\n"
        f"Gender: {gender}\n"
        f"BMI: {bmi}\n"
        f"Diet Preference: {diet_preference}\n"
        f"Location: India\n"  # Specify the location
    )

    if additional_input:
        prompt += f"Additional Input: {additional_input}\n"

    prompt += (
        f"\nPlease provide a personalized diet plan that is nutritionally balanced, "
        f"affordable, and suitable for their health status. Include common and affordable "
        f"Indian food items and easy-to-make recipes that are adaptable to daily life in India."
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
    # Initialize session state
    if 'bmi' not in st.session_state:
        st.session_state.bmi = None
    if 'diet_plan' not in st.session_state:
        st.session_state.diet_plan = None
    if 'food_info' not in st.session_state:
        st.session_state.food_info = None
    if 'recommendation_generated' not in st.session_state:
        st.session_state.recommendation_generated = False

    # Welcome Note
    st.title("NutriFit")
    st.write("Welcome to the Fitness & Diet Recommender App! This app calculates your BMI and provides a personalized diet and workout plan based on your details. You can also check the nutritional content of various food items.")

    # Sidebar Calorie Counter
    st.sidebar.header("Nutritional Information")
    food_item = st.sidebar.text_input("Enter food item:")
    if st.sidebar.button("Get Nutritional Info"):
        if food_item:
            nutrition = get_nutritional_info(food_item)
            if nutrition:
                st.session_state.food_info = {
                    "item": food_item.title(),
                    "calories": nutrition['calories'],
                    "protein": nutrition['protein'],
                    "carbohydrates": nutrition['carbohydrates'],
                    "fat": nutrition['fat']
                }
            else:
                st.session_state.food_info = "Sorry, don’t have nutritional information for that."
        else:
            st.session_state.food_info = "Please enter a food item."

    # Display Nutritional Information from Sidebar
    if st.session_state.food_info:
        if isinstance(st.session_state.food_info, dict):
            st.sidebar.write(f"**{st.session_state.food_info['item']}**")
            st.sidebar.write(f"Calories: {st.session_state.food_info['calories']} kcal")
            st.sidebar.write(f"Protein: {st.session_state.food_info['protein']} g")
            st.sidebar.write(f"Carbohydrates: {st.session_state.food_info['carbohydrates']} g")
            st.sidebar.write(f"Fat: {st.session_state.food_info['fat']} g")
        else:
            st.sidebar.write(st.session_state.food_info)

    # Main app inputs
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=1, max_value=120, step=1)
    gender = st.selectbox("Select your gender", ["Male", "Female", "Other"])
    weight = st.number_input("Enter your weight (kg)", min_value=1.0, step=0.1)
    height = st.number_input("Enter your height (cm)", min_value=50.0, step=0.1)
    diet_preference = st.selectbox("Do you prefer a vegetarian or non-vegetarian diet?", ["Veg", "Non-Veg"])

    # Additional Input Box for Custom Preferences
    additional_input = st.text_area("Enter any additional preferences or restrictions (e.g., allergies, dislikes):")

    if st.button("Calculate BMI and Get Diet Plan"):
        if name and age and weight and height and diet_preference:
            # Calculate BMI
            bmi = calculate_bmi(weight, height)
            st.session_state.bmi = bmi
            st.write(f"Hello {name}, your BMI is: {bmi}")

            # Generate a personalized diet plan only if it hasn't been generated already
            if not st.session_state.recommendation_generated:
                diet_plan = generate_diet_plan(bmi, diet_preference, name, age, gender, additional_input)
                st.session_state.diet_plan = diet_plan
                st.session_state.recommendation_generated = True  # Set flag to prevent regeneration
                st.write(diet_plan)
        else:
            st.write("Please fill in all the details.")

    # Ensure the diet plan persists even after fetching nutritional information
    if st.session_state.diet_plan:
        st.write(st.session_state.diet_plan)

if __name__ == "__main__":
    main()
