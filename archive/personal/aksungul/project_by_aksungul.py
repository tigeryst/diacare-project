import streamlit as st
import os
from datetime import datetime
import openai
from dotenv import load_dotenv
from PIL import Image
import hashlib
import json
import requests

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPEN_API_KEY")

# Set your Image Recognition API details
image_recognition_api_url = "https://api.your-service.com/recognize"  # Replace with actual API endpoint
image_recognition_api_key = os.getenv("IMAGE_RECOGNITION_API_KEY")  # Add this to your .env file

# Function to get hashed password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check login credentials
def check_credentials(username, password):
    hashed_password = hash_password(password)
    if os.path.exists(f"user_profiles/{username}.txt"):
        with open(f"user_profiles/{username}.txt", "r") as file:
            lines = file.readlines()
            stored_hashed_password = lines[-1].strip().split(": ")[1]
            return hashed_password == stored_hashed_password
    return False

# Function to get meal recipe
def get_meal_recipe(
    profile,
    calorie_needs,
    food_preference,
    nationality,
    cuisine,
    category,
    ingredients=None,
):
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
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
    )

    # Extract and return the response text
    return response.choices[0].message["content"].strip()

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
        "Super active (very hard exercise/sports & physical job or 2x training)": 1.9,
    }
    return bmr * activity_multiplier[activity_level]

# Function to get ingredients from image
def get_ingredients_from_image(image):
    image.save("temp_image.jpg")
    try:
        with open("temp_image.jpg", "rb") as img_file:
            response = requests.post(
                image_recognition_api_url,
                headers={"Authorization": f"Bearer {image_recognition_api_key}"},
                files={"image": img_file}
            )
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            ingredients = data.get("ingredients", [])
            return ingredients
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the image recognition service: {e}")
        return []

# Main app function
def main():
    st.title("DiaCare - *your assistant in the fight against diabetes!*")

    page = st.sidebar.selectbox(
        "Select a page:", ["Register", "Login", "Generate Recipe"]
    )

    if page == "Register":
        st.header("Register")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        if st.button("Register"):
            if not os.path.exists("user_profiles"):
                os.makedirs("user_profiles")
            if os.path.exists(f"user_profiles/{username}.txt"):
                st.error("Username already exists. Please choose a different username.")
            else:
                with open(f"user_profiles/{username}.txt", "w") as file:
                    file.write(f"Username: {username}\n")
                    file.write(f"Password: {hash_password(password)}\n")
                st.success("Registration successful! Please proceed to login.")

    elif page == "Login":
        st.header("Login")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        if st.button("Login"):
            if check_credentials(username, password):
                st.success("Login successful!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
            else:
                st.error("Invalid username or password.")

    elif page == "Generate Recipe":
        if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
            st.warning("Please login to access this page.")
        else:
            st.header("Generate Recipe")

            username = st.session_state["username"]

            profile_data = {}
            try:
                if os.path.exists(f"user_profiles/{username}.txt"):
                    with open(f"user_profiles/{username}.txt", "r") as file:
                        profile_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                st.error(f"Error reading profile data: {str(e)}")

            name = st.text_input("**Name:**", value=profile_data.get("name", ""))
            age = st.number_input("**Age:**", min_value=0, max_value=120, value=profile_data.get("age", 10))
            sex = st.selectbox("**Sex:**", ["Male", "Female"], index=["Male", "Female"].index(profile_data.get("sex", "Male")))
            height = st.number_input("**Height (cm):**", min_value=0, max_value=300, value=profile_data.get("height", 150))
            weight = st.number_input("**Weight (kg):**", min_value=0, max_value=300, value=profile_data.get("weight", 50))

            activity_level = st.selectbox(
                "**Daily Activity Level:**",
                [
                    "Sedentary (little or no exercise)",
                    "Lightly active (light exercise/sports 1-3 days/week)",
                    "Moderately active (moderate exercise/sports 3-5 days/week)",
                    "Very active (hard exercise/sports 6-7 days a week)",
                    "Super active (very hard exercise/sports & physical job or 2x training)",
                ],
            )

            food_preference = st.text_input(
                "**Food Preference:** (e.g., vegan, vegetarian, gluten-free)"
            )
            nationality = st.text_input("**Nationality:**")
            cuisine = st.text_input(
                "**Cuisine Preference:** (e.g., Italian, Chinese, Indian)"
            )
            category = st.text_input(
                "**Meal Category:** (e.g., breakfast, lunch, dinner)"
            )

            uploaded_file = st.file_uploader(
                "**Upload an image of ingredients:**", type=["jpg", "jpeg", "png"]
            )
            ingredients = None
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Ingredients", use_column_width=True)
                ingredients = get_ingredients_from_image(image)

            if st.button("Save Profile"):
                profile_data = {
                    "username": st.session_state["username"],
                    "name": name,
                    "age": age,
                    "sex": sex,
                    "height": height,
                    "weight": weight,
                }
                with open(f"user_profiles/{st.session_state['username']}.txt", "w") as file:
                    json.dump(profile_data, file)
                st.success("***Profile saved successfully!***")

            bmr = calculate_bmr(weight, height, age, sex)
            daily_calorie_needs = calculate_daily_calorie_needs(bmr, activity_level)

            st.header("Results")
            st.write(f"Estimated BMR: {bmr:.2f} calories/day")
            st.write(
                f"Estimated Daily Calorie Needs: {daily_calorie_needs:.2f} calories/day"
            )

            if st.button("Get Meal Recipe"):
                profile = {
                    "name": name,
                    "age": age,
                    "sex": sex,
                    "height": height,
                    "weight": weight,
                    "activity_level": activity_level,
                }
                st.header("Personalized Meal Recipe")
                meal_recipe = get_meal_recipe(
                    profile,
                    daily_calorie_needs,
                    food_preference,
                    nationality,
                    cuisine,
                    category,
                    ingredients,
                )
                st.write(meal_recipe)
                st.image(
                    "path_to_image_of_recipe.jpg",
                    caption="Recipe Image",
                    use_column_width=True,
                )
                st.image(
                    "path_to_image_of_cooking_process.jpg",
                    caption="Cooking Process",
                    use_column_width=True,
                )

if __name__ == "__main__":
    main()


