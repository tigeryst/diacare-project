import streamlit as st

def apply_custom_css():
    css = """
    <style>
        .main {
            background-image: linear-gradient(#87CEEB, #E0F7FA);
            color: #000000;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #000000;
        }

        .stTitle {
            text-align: center;
            color: #000000;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            font-size: 36px;
        }

        .stSidebar {
            background-color: #87CEEB;
            color: #000000;
        }

        .stTextInput > div > input, .stNumberInput > div > input, .stSelectbox > div > select, .stTextArea > div > textarea {
            border: 2px solid #E0F7FA;
            padding: 10px;
            border-radius: 5px;
            background-color: #ffffff;
            color: #000000;
        }

        .stButton > button {
            background-color: #E0F7FA;
            color: #000000;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }

        .stButton > button:hover {
            background-color: #b2ebf2;
        }

        .stError {
            color: #ff0000;
        }

        .stSuccess {
            color: #00ff00;
        }

        /* Custom title style */
        .custom-title {
            font-family: 'Georgia', serif;
            font-size: 42px;
            font-weight: bold;
            color: #333333;  /* Dark grey */
            text-align: center;
            margin-top: 20px;
            margin-bottom: 20px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)