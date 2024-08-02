import streamlit as st
import json
from gpt import get

# Function to calculate BMR
def calculate_bmr(sex, weight, height, age):
    if sex == 'Male':
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

# Function to calculate daily calorie needs
def calculate_daily_calories(bmr, activity_level):
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly active": 1.375,
        "Moderately active": 1.55,
        "Very active": 1.725,
        "Super active": 1.9
    }
    return bmr * activity_multipliers[activity_level]

# Streamlit interface
st.title("Diacare App")

# User input fields for MVP1
name = st.text_input("Name")
age = st.number_input("Age", min_value=0, max_value=120, value=25)
sex = st.selectbox("Sex", ["Male", "Female"])
height = st.number_input("Height (cm)", min_value=0, max_value=300, value=170)
weight = st.number_input("Weight (kg)", min_value=0, max_value=300, value=70)
activity_level = st.selectbox("Daily Activity Level", ["Sedentary", "Lightly active", "Moderately active", "Very active", "Super active"])

# User input fields for MVP2
food_preference = st.text_input("Food Preference (e.g., vegetarian, vegan, non-vegetarian)")
nationality = st.text_input("Nationality")
cuisine = st.text_input("Preferred Cuisine (e.g., Italian, Indian, Chinese)")
category = st.text_input("Category (e.g., breakfast, lunch, dinner)")

# Calculate BMR and daily calorie needs
if st.button("Calculate"):
    bmr = calculate_bmr(sex, weight, height, age)
    daily_calories = calculate_daily_calories(bmr, activity_level)
    
    # Display results
    st.write(f"Estimated BMR: {bmr:.2f} calories/day")
    st.write(f"Estimated Daily Calorie Needs: {daily_calories:.2f} calories/day")
    
    # Save user data to local text file
    user_data = {
        "name": name,
        "age": age,
        "sex": sex,
        "height": height,
        "weight": weight,
        "activity_level": activity_level,
        "bmr": bmr,
        "daily_calories": daily_calories,
        "food_preference": food_preference,
        "nationality": nationality,
        "cuisine": cuisine,
        "category": category
    }
    
    with open('user_data.txt', 'w') as f:
        json.dump(user_data, f)
    
    # Generate meal recipe using ChatGPT
    recipe = generate_response(user_data)
    st.write("Generated Meal Recipe:")
    st.write(recipe)