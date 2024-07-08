import streamlit as st

# Title of the Streamlit app
st.title("Quick Streamlit App")

# Input box to take user input
user_input = st.text_input("Enter some text:")

# Button to trigger an action
if st.button("Submit"):
    st.write("You entered:", user_input)
