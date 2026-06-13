import streamlit as st
from database.db import engine
from database.models import Base


Base.metadata.create_all(engine)



if "logged_in" not in st.session_state:
    st.session_state.logged_in=False
    st.page_link(
    "pages/goals.py",
    label="🎯 Savings Goals"
)



if not st.session_state.logged_in:

    st.title(
        "AI Personal Finance Platform"
    )


    st.write(
        "Please login or signup"
    )


    option = st.selectbox(
        "Choose",
        [
            "Login",
            "Signup"
        ]
    )


    if option=="Login":
        st.switch_page(
            "pages/login.py"
        )

    else:
        st.switch_page(
            "pages/signup.py"
        )


else:

    st.title(
        f"Welcome {st.session_state.user_name}"
    )


    st.page_link(
    "pages/add_expense.py",
    label="➕ Add Transaction"
)

st.page_link(
    "pages/dashboard.py",
    label="📊 Dashboard"
)