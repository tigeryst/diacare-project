import streamlit as st

from services import auth as auth_service


def render():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            auth_service.login(email, password)
            st.success("Logged in successfully")
            st.session_state["logged_in"] = True
            st.session_state["email"] = email
        except:
            st.error("Invalid email or password")
