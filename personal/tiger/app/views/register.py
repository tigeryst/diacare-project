import streamlit as st

from services import auth as auth_service


def render():
    st.title("Register")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        try:
            auth_service.register(email, password)
            st.success("Registered successfully")
        except:
            st.error("User already exists")
