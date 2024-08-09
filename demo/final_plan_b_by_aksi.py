import streamlit as st
import os
from datetime import datetime
import openai
from dotenv import load_dotenv
import hashlib
from custom_css import apply_custom_css

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPEN_API_KEY")

# Function to get hashed password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check login credentials
def check_credentials(username, password):
    hashed_password = hash_password(password)
    user_file = f"user_profiles/{username}.txt"
    
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("Password:"):
                    stored_hashed_password = line.strip().split(": ")[1]
                    return hashed_password == stored_hashed_password
    return False

# # Function to get meal recipe
# def get_meal_recipe(profile, calorie_needs, food_preference, nationality, cuisine, category, ingredients=None):
#     # Define the prompt for the API
#     prompt = (
#         f"User profile: {profile}\n"
#         f"Calorie needs: {calorie_needs}\n"
#         f"Food preference: {food_preference}\n"
#         f"Nationality: {nationality}\n"
#         f"Cuisine: {cuisine}\n"
#         f"Category: {category}\n"
#         f"Ingredients: {ingredients}\n"
#         "Diabetes requirements: tailored meal recipe for people with diabetes."
#     )
    
#     # Make the API call using the latest model
#     response = openai.openai.Chat.create(
#         model="gpt-3.5-turbo",  # or "gpt-4" if you have access
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=300
#     )
    
#     # Extract and return the response text
#     return response.choices[0].message['content'].strip()


# Function to get meal recipe using the correct API interface
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
    
    # Make the API call using the correct method
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    
    # Extract and return the response text
    return response['choices'][0]['message']['content'].strip()


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
    return bmr * activity_multiplier.get(activity_level, 1.2)  # Default to Sedentary if not found

# Main app function
def main():
    st.set_page_config(page_title="DiaCare", layout="wide")
    apply_custom_css()
    
    # Double-check this title update
    st.markdown('<h1 class="custom-title">DiaCare - A Diabetes Management Application</h1>', unsafe_allow_html=True)    
    # Page navigation
    st.sidebar.header("Navigate")
    page = st.sidebar.selectbox("Select a page:", ["Register", "Login", "Generate Recipe"])
    
    # Page content based on selection
    if page == "Register":
        st.header("Register")
        username = st.text_input("Username:")
        email = st.text_input("Email:")
        password = st.text_input("Password:", type="password")
        name = st.text_input("Name:")
        age = st.number_input("Age:", min_value=0, max_value=120, value=25)
        weight = st.number_input("Weight (kg):", min_value=0, max_value=300, value=50)
        height = st.number_input("Height (cm):", min_value=0, max_value=300, value=150)
        sex = st.selectbox("Sex:", ["Male", "Female"])
        
        if st.button("Register"):
            if not os.path.exists("user_profiles"):
                os.makedirs("user_profiles")
            if os.path.exists(f"user_profiles/{username}.txt"):
                st.error("Username already exists. Please choose a different username.")
            else:
                with open(f"user_profiles/{username}.txt", "w") as file:
                    file.write(f"Username: {username}\n")
                    file.write(f"Email: {email}\n")
                    file.write(f"Name: {name}\n")
                    file.write(f"Age: {age}\n")
                    file.write(f"Weight: {weight}\n")
                    file.write(f"Height: {height}\n")
                    file.write(f"Sex: {sex}\n")
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
                st.session_state["profile"] = {}
                with open(f"user_profiles/{username}.txt", "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        parts = line.strip().split(": ")
                        if len(parts) == 2:
                            key, value = parts
                            if key == "Name":
                                st.session_state["profile"]["name"] = value
                            elif key == "Age":
                                st.session_state["profile"]["age"] = int(value)
                            elif key == "Sex":
                                st.session_state["profile"]["sex"] = value
                            elif key == "Height":
                                st.session_state["profile"]["height"] = int(value)
                            elif key == "Weight":
                                st.session_state["profile"]["weight"] = int(value)
            else:
                st.error("Invalid username or password.")

    elif page == "Generate Recipe":
        if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
            st.warning("Please login to access this page.")
        else:
            st.header("Generate Recipe")
            
            # Display saved profile details
            profile = st.session_state.get("profile", {})
            st.write("**Profile Details:**")
            st.write(f"**Name:** {profile.get('name', '')}")
            st.write(f"**Age:** {profile.get('age', '')}")
            st.write(f"**Sex:** {profile.get('sex', '')}")
            st.write(f"**Height (cm):** {profile.get('height', '')}")
            st.write(f"**Weight (kg):** {profile.get('weight', '')}")
            
            # Daily activity level input
            activity_level = st.selectbox("**Daily Activity Level:**", [
                "Sedentary (little or no exercise)",
                "Lightly active (light exercise/sports 1-3 days/week)",
                "Moderately active (moderate exercise/sports 3-5 days/week)",
                "Very active (hard exercise/sports 6-7 days a week)",
                "Super active (very hard exercise/sports & physical job or 2x training)"
            ])
            
            # Additional user preferences
            food_preference = st.text_input("**Food Preference:** (e.g., vegan, vegetarian, gluten-free)")
            nationality = st.text_input("**Nationality:**")
            cuisine = st.text_input("**Cuisine Preference:** (e.g., Italian, Chinese, Indian)")
            category = st.text_input("**Meal Category:** (e.g., breakfast, lunch, dinner)")
            ingredients = st.text_area("**Available Ingredients:** (e.g., tomato, lettuce, cucumber)")
            
            # Calculate BMR and daily calorie needs
            bmr = calculate_bmr(profile.get("weight", 50), profile.get("height", 150), profile.get("age", 25), profile.get("sex", "Male"))
            calorie_needs = calculate_daily_calorie_needs(bmr, activity_level)
            
            st.write(f"**BMR:** {bmr}")
            st.write(f"**Daily Calorie Needs:** {calorie_needs}")

            # Store input in local text file
            if st.button("Save Profile"):
                profile_data = (
                    f"{datetime.now()}\nActivity Level: {activity_level}\nFood Preference: {food_preference}\nNationality: {nationality}\n"
                    f"Cuisine: {cuisine}\nCategory: {category}\nIngredients: {ingredients}\n\n"
                )
                with open(f"user_profiles/{st.session_state['username']}_profile.txt", "a") as file:
                    file.write(profile_data)
                st.success("Profile saved successfully!")
            
            if st.button("Generate Recipe"):
                profile_str = ', '.join([f'{key}: {value}' for key, value in profile.items()])
                recipe = get_meal_recipe(profile_str, calorie_needs, food_preference, nationality, cuisine, category, ingredients)
                st.subheader("Generated Recipe")
                st.write(recipe)

if __name__ == "__main__":
    main()
