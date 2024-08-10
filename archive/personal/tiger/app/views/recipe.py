import streamlit as st

from services import recipe as recipe_service
from services import user as user_service


def render():
    st.title("Generate Recipe")

    if not st.session_state.get("logged_in"):
        st.warning("You need to log in to generate a recipe.")
        return

    user_data = user_service.get_user(st.session_state["email"])

    if st.button("Generate Recipe"):
        try:
            recipe = recipe_service.generate_recipe(user_data)
            st.success("Generated Recipe:")
            st.write(recipe)
        except:
            st.error("Could not generate a recipe. Please try again.")
