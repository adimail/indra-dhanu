import streamlit as st
from modules.pages import home_page
from modules.pages import model_page
from modules.pages import program_code
from streamlit_option_menu import option_menu


st.set_page_config(
    page_title="Indra Dhanu",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    with st.sidebar:
        page = option_menu(
            "Indra Dhanu", ["Home", "Model", "Code"],
            icons=["house-door-fill", "tools", "code-slash"],
            menu_icon="camera",
            default_index=1
        )

    if page == "Home":
        home_page()
    elif page == "Model":
        model_page()
    elif page == "Code":
        program_code()


if __name__ == "__main__":
    main()