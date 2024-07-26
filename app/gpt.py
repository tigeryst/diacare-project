import openai
from dotenv import load_dotenv
import os
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPEN_API_KEY")


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
    meal_recipe = get_meal_recipe(profile, daily_calorie_needs)
    st.write(meal_recipe)