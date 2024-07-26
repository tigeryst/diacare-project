import streamlit as st

from services import user as user_service


def render():
    st.title("User Profile")

    user_data = user_service.get_user(st.session_state["email"])
    new_user_data = {
        "email": st.text_input("Email", value=user_data["email"], disabled=True),
        "age": st.number_input(
            "Age", value=user_data.get("age", 18), min_value=18, max_value=100
        ),
        "weight": st.number_input(
            "Weight (kg)",
            value=user_data.get("weight", 70),
            min_value=30,
            max_value=300,
        ),
        "height": st.number_input(
            "Height (cm)",
            value=user_data.get("height", 150),
            min_value=100,
            max_value=250,
        ),
        "nationality": st.text_input(
            "Nationality", value=user_data.get("nationality", "")
        ),
        "food_preferences": st.text_input(
            "Food Preferences", value=user_data.get("food_preferences", "")
        ),
    }

    if st.button("Save Profile"):
        user_service.update_user(new_user_data)
        st.success(f"Profile saved for user: {new_user_data['email']}")
