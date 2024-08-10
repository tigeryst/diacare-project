import streamlit as st


def main():
    st.set_page_config(page_title="CSS Styling Demo")

    css = """
    <style>
        .main {
            background-image: linear-gradient(#110f14, #33113d);
        }

        h1#css-styling-demo {
            text-transform: uppercase;
            text-align: center;
            letter-spacing: 0.3rem;
        }

        div[data-testid="stTextInput-RootElement"]:focus-within {
            background: red;
            animation: gradient-animation 3s infinite;
            border-image: linear-gradient(45deg, #ff6ec4, #7873f5, #66e8e4, #f7ff00) 1;
            padding-right: 0;
        }

        @keyframes gradient-animation {
            0% {
                border-image-source: linear-gradient(45deg, #ff6ec4, #7873f5, #66e8e4, #f7ff00);
            }
            50% {
                border-image-source: linear-gradient(45deg, #f7ff00, #66e8e4, #7873f5, #ff6ec4);
            }
            100% {
                border-image-source: linear-gradient(45deg, #ff6ec4, #7873f5, #66e8e4, #f7ff00);
            }
        }
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

    st.title("CSS Styling Demo")

    st.markdown("This is a demo of how to use CSS styling in Streamlit.")

    st.markdown("### Login Form")

    st.text_input("Username", key="username")

    st.text_input("Password", key="password", type="password")

    if st.button("Login", key="login"):
        st.success("Logged in successfully")


if __name__ == "__main__":
    main()
