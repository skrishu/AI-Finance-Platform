import streamlit as st
from database.db import SessionLocal
from database.models import Expense, Income
from datetime import date


st.title("Add Transaction")


if "logged_in" not in st.session_state:
    st.stop()


transaction_type = st.selectbox(
    "Type",
    [
        "Expense",
        "Income"
    ]
)


amount = st.number_input(
    "Amount",
    min_value=0.0
)


transaction_date = st.date_input(
    "Date",
    date.today()
)


if transaction_type == "Expense":

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Healthcare",
            "Other"
        ]
    )


    description = st.text_input(
        "Description"
    )


if st.button("Save"):

    db = SessionLocal()


    if transaction_type == "Expense":

        new_expense = Expense(
            user_id=st.session_state.user_id,
            amount=amount,
            category=category,
            description=description,
            date=transaction_date
        )

        db.add(new_expense)



    else:

        new_income = Income(
            user_id=st.session_state.user_id,
            amount=amount,
            date=transaction_date
        )

        db.add(new_income)


    db.commit()
    db.close()


    st.success(
        "Transaction added!"
    )