import streamlit as st
import os
from datetime import datetime
import openai
from dotenv import load_dotenv
from PIL import Image
import hashlib

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPEN_API_KEY")

# Function to get hashed password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check login credentials
def check_credentials(username, password):
    hashed_password = hash_password(password)
    if os.path.exists(f"user_profiles/{username}.txt"):
        with open(f"user_profiles/{username}.txt", "r") as file:
            lines = file.readlines()
            stored_hashed_password = lines[1].strip().split(": ")[1]
            return hashed_password == stored_hashed_password
    return False

# Function to get meal recipe
def get_meal_recipe(profile, calorie_needs, food_preference, nationality, cuisine, category, ingredients=None):
    # Define the prompt for the API
    prompt = (
        f"User profile: {profile}\n"
        f"Calorie needs: {calorie_needs}\n"
        f"Food preference: {food_preference}\n"
        f"Nationality: {nationality}\n"
        f"Cuisine: {cuisine}\n"
        f"Category: {category}\n"
        f"Ingredients: {ingredients}\n"
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

# Function to get ingredients from image (placeholder, needs real implementation)
def get_ingredients_from_image(image):
    # This is a placeholder function. In a real implementation, you would use an image recognition model.
    return "tomato, lettuce, cucumber"

# Main app function
def main():
    st.title("DiaCare - *your assistant in the fight against diabetes!*")

    # Page selection
    page = st.sidebar.selectbox("Select a page:", ["Register", "Login", "Generate Recipe"])

    if page == "Register":
        st.header("Register")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        name = st.text_input("**Name:**")
        age = st.number_input("**Age:**", min_value=0, max_value=120, value=10)
        sex = st.selectbox("**Sex:**", ["Male", "Female"])
        height = st.number_input("**Height (cm):**", min_value=0, max_value=300, value=150)
        weight = st.number_input("**Weight (kg):**", min_value=0, max_value=300, value=50)
        activity_level = st.selectbox("**Daily Activity Level:**", [
            "Sedentary (little or no exercise)",
            "Lightly active (light exercise/sports 1-3 days/week)",
            "Moderately active (moderate exercise/sports 3-5 days/week)",
            "Very active (hard exercise/sports 6-7 days a week)",
            "Super active (very hard exercise/sports & physical job or 2x training)"
        ])
        if st.button("Register"):
            if not os.path.exists("user_profiles"):
                os.makedirs("user_profiles")
            if os.path.exists(f"user_profiles/{username}.txt"):
                st.error("Username already exists. Please choose a different username.")
            else:
                with open(f"user_profiles/{username}.txt", "w") as file:
                    file.write(f"Username: {username}\n")
                    file.write(f"Password: {hash_password(password)}\n")
                    file.write(f"Name: {name}\n")
                    file.write(f"Age: {age}\n")
                    file.write(f"Sex: {sex}\n")
                    file.write(f"Height: {height}\n")
                    file.write(f"Weight: {weight}\n")
                    file.write(f"Activity Level: {activity_level}\n")
                st.success("Registration successful! Please proceed to login.")
                st.experimental_rerun()

    elif page == "Login":
        st.header("Login")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        if st.button("Login"):
            if check_credentials(username, password):
                st.success("Login successful!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")

    elif page == "Generate Recipe":
        if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
            st.warning("Please login to access this page.")
        else:
            st.header("Generate Recipe")

            username = st.session_state["username"]
            with open(f"user_profiles/{username}.txt", "r") as file:
                lines = file.readlines()
                name = lines[2].strip().split(": ")[1]
                age = int(lines[3].strip().split(": ")[1])
                sex = lines[4].strip().split(": ")[1]
                height = int(lines[5].strip().split(": ")[1])
                weight = int(lines[6].strip().split(": ")[1])
                activity_level = lines[7].strip().split(": ")[1]

            st.write(f"Name: {name}")
            st.write(f"Age: {age}")
            st.write(f"Sex: {sex}")
            st.write(f"Height: {height} cm")
            st.write(f"Weight: {weight} kg")
            st.write(f"Activity Level: {activity_level}")

            # Additional user preferences
            food_preference = st.text_input("**Food Preference:** (e.g., vegan, vegetarian, gluten-free)")
            nationality = st.text_input("**Nationality:**")
            cuisine = st.text_input("**Cuisine Preference:** (e.g., Italian, Chinese, Indian)")
            category = st.text_input("**Meal Category:** (e.g., breakfast, lunch, dinner)")

            # Image upload for ingredient recognition or manual input
            option = st.selectbox("Would you like to upload an image of ingredients or enter them manually?", ["Upload Image", "Enter Manually"])
            ingredients = None
            if option == "Upload Image":
                uploaded_file = st.file_uploader("**Upload an image of ingredients:**", type=["jpg", "jpeg", "png"])
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Uploaded Ingredients", use_column_width=True)
                    ingredients = get_ingredients_from_image(image)
            else:
                ingredients = st.text_input("**Enter ingredients you have at home:**")

            # Calculate BMR and daily calorie needs
            bmr = calculate_bmr(weight, height, age, sex)
            daily_calorie_needs = calculate_daily_calorie_needs(bmr, activity_level)

            # Display BMR and daily calorie needs
            st.header("Results")
            st.write(f"Estimated BMR: {bmr:.2f} calories/day")
            st.write(f"Estimated Daily Calorie Needs: {daily_calorie_needs:.2f} calories/day")

            if st.button("Get Meal Recipe"):
                profile = {
                    "name": name,
                    "age": age,
                    "sex": sex,
                    "height": height,
                    "weight": weight,
                    "activity_level": activity_level
                }
                st.header("Personalized Meal Recipe")
                meal_recipe = get_meal_recipe(profile, daily_calorie_needs, food_preference, nationality, cuisine, category, ingredients)


