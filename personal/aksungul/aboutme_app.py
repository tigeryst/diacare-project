import streamlit as st
import pandas as pd

st.title("WELCOME EVERYONE!!!")
st.header("Hi! My name is Aksungul!")
st.markdown("> About me!")
st.markdown("*Well, as you've already known, i'm Aksungul. I am 15 years old and i am from the beautiful city of Karakalpakstan - Nukus!*")
st.markdown("*I am really interested in STEM subjects, especially in **Maths**, **IT** and **Physics**. In the future, I want to be software engineer!*")
st.markdown("---")

st.markdown("> My hobbies!")
table1=pd.DataFrame({"my hobbies": ["playing violin", "drawing and taking pictures", "singing", "do synchronozed swimming", "reading books"]})
st.table(table1)
st.markdown("---")

st.markdown("> My achievements!")
dataframe1=pd.DataFrame({"my achievements": ["Girls in research'24", "The Ethical Leadership experience'24", "Technovation Girls'24"]})
st.dataframe(dataframe1)

def changes():
    print("CHANGED")
state = st.checkbox("Do you want to continue reading?", value = True, on_change=changes)
if state:
    st.write("wow! thank you for your interest!")
else:
    pass

radio_btn = st.radio("In which country Do you live?", options=("US", "UK", "Canada", "Uzbekistan", "Other"))
print(radio_btn)

def btn_click():
    print("button to go for telegram channel clicked")
btn = st.button("say hello!)", on_click=btn_click)

