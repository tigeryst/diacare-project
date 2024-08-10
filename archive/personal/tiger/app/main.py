from dotenv import load_dotenv
import os
import streamlit as st
import sys

path_components = os.path.dirname(__file__).split(os.sep)
root_index = path_components.index("app")
root_dir = os.sep.join(path_components[: root_index + 1])
sys.path.append(root_dir)

from views.profile import render as render_profile
from views.recipe import render as render_recipe
from views.login import render as render_login
from views.register import render as render_register

load_dotenv()


def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    st.set_page_config(page_title="DiaCare | Recipe Generator")

    st.sidebar.title("Navigation")
    if st.session_state["logged_in"]:
        page = st.sidebar.radio("Go to", ["User Profile", "Generate Recipe", "Logout"])
        if page == "User Profile":
            render_profile()
        elif page == "Generate Recipe":
            render_recipe()
        elif page == "Logout":
            st.session_state["logged_in"] = False
            st.success("Logged out successfully")
    else:
        page = st.sidebar.radio("Go to", ["Login", "Register"])
        if page == "Login":
            render_login()
            if st.session_state["logged_in"]:
                st.rerun()

        elif page == "Register":
            render_register()


if __name__ == "__main__":
    main()
