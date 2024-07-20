import streamlit as st
import os
from datetime import datetime
import openai

# Set your OpenAI API key
openai.api_key = 'sk-proj-s4ThvdJJBj458bJt3wQRT3BlbkFJIZutaaw7uDWEPBoNgcJD'

def get_meal_recipe(profile, calorie_needs):
    # Define the prompt for the API
    prompt = (
        f"User profile: {profile}\n"
        f"Calorie needs: {calorie_needs}\n"
        "Diabetes requirements: tailored meal recipe for people with diabetes."
    )
    
    # Make the API call using the latest model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    
    # Extract and return the response text
    return response.choices[0].message['content'].strip()

# Function to calculate BMR
def calculate_bmr(weight, height, age, sex):
    if sex == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

# Function to calculate daily calorie needs
def calculate_daily_calorie_needs(bmr, activity_level):
    activity_multiplier = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly active (light exercise/sports 1-3 days/week)": 1.375,
        "Moderately active (moderate exercise/sports 3-5 days/week)": 1.55,
        "Very active (hard exercise/sports 6-7 days a week)": 1.725,
        "Super active (very hard exercise/sports & physical job or 2x training)": 1.9
    }
    return bmr * activity_multiplier[activity_level]

# Streamlit interface
st.title("DiaCare - *your assistant in the fight against diabetes!*")

# User profile input
st.header("User Profile")
name = st.text_input("**Name:**")
age = st.number_input("**Age:**", min_value=0, max_value=120, value=10)
sex = st.selectbox("**Sex:**", ["Male", "Female"])
height = st.number_input("**Height (cm):**", min_value=0, max_value=300, value=150)
weight = st.number_input("**Weight (kg):**", min_value=0, max_value=300, value=50)

# Daily activity level input
activity_level = st.selectbox("**Daily Activity Level:**", [
    "Sedentary (little or no exercise)",
    "Lightly active (light exercise/sports 1-3 days/week)",
    "Moderately active (moderate exercise/sports 3-5 days/week)",
    "Very active (hard exercise/sports 6-7 days a week)",
    "Super active (very hard exercise/sports & physical job or 2x training)"
])

# Store input in local text file
if st.button("Save Profile"):
    profile_data = f"{datetime.now()}\nName: {name}\nAge: {age}\nSex: {sex}\nHeight: {height}\nWeight: {weight}\nActivity Level: {activity_level}\n\n"
    with open("user_profiles.txt", "a") as file:
        file.write(profile_data)
    st.success("***Profile saved successfully!***")

# Calculate BMR and daily calorie needs
bmr = calculate_bmr(weight, height, age, sex)
daily_calorie_needs = calculate_daily_calorie_needs(bmr, activity_level)

# Display BMR and daily calorie needs
st.header("Results")
st.write(f"Estimated BMR: {bmr:.2f} calories/day")
st.write(f"Estimated Daily Calorie Needs: {daily_calorie_needs:.2f} calories/day")

# Get meal recipe from ChatGPT
 Meal Recipe"):
    profile = {if st.button("Get
        "name": name,
        "age": age,
        "sex": sex,
        "height": height,
        "weight": weight,
        "activity_level": activity_level
    }
    st.header("Personalized Meal Recipe")
    meal_recipe = get_meal_recipe(profile, daily_calorie_needs)
    st.write(meal_recipe)



