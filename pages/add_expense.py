import streamlit as st
from database.db import SessionLocal
from database.models import Expense, Income
from datetime import date

from models.expense_classifier import ExpenseClassifier
from models.training_data import descriptions, categories
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/login.py")

classifier = ExpenseClassifier()

classifier.train(
    descriptions,
    categories
)


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


description = ""


if transaction_type == "Expense":

    description = st.text_input(
        "Description",
        placeholder="Example: Swiggy order, Uber ride..."
    )


predicted_category = None
category = None


if transaction_type == "Expense":

    predicted_category = classifier.predict(
        description
    )


    category = st.selectbox(
        "Confirm Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Healthcare",
            "Other"
        ],
        index=[
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Healthcare",
            "Other"
        ].index(predicted_category)
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


        st.success(
            f"Transaction added! Category saved as {category}"
        )


    else:

        new_income = Income(
            user_id=st.session_state.user_id,
            amount=amount,
            date=transaction_date
        )


        db.add(new_income)


        st.success(
            "Income added!"
        )


    db.commit()
    db.close()