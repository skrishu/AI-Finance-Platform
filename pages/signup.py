import streamlit as st
from auth.authentication import create_user, login_user
from utils.session import login_session


def signup():

    st.title("Create Account")


    name = st.text_input("Name")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button("Signup"):

        success = create_user(
            name,
            email,
            password
        )


        if success:

            user = login_user(
            email,
            password
            )

            login_session(user)

            st.success(
            "Account created!"
            )

            st.switch_page(
            "pages/dashboard.py"
            )
        else:
            st.error(
                "Email already exists"
            )


signup()