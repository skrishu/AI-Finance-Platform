import streamlit as st
from auth.authentication import create_user


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
            st.success(
                "Account created!"
            )
        else:
            st.error(
                "Email already exists"
            )


signup()