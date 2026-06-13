import streamlit as st
from auth.authentication import login_user
from utils.session import login_session


def login():

    st.title("Login")


    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button("Login"):

        user = login_user(
            email,
            password
        )


        if user:

            login_session(user)

            st.success(
                "Login successful"
            )

            st.switch_page(
                "app.py"
            )


        else:
            st.error(
                "Invalid credentials"
            )



login()