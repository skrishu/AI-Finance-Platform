import streamlit as st
from datetime import date

from database.db import SessionLocal
from database.models import Goal



st.title("🎯 Savings Goals")


if "logged_in" not in st.session_state:
    st.stop()



goal_name = st.text_input(
    "Goal Name"
)


target = st.number_input(
    "Target Amount",
    min_value=0.0
)


saved = st.number_input(
    "Current Savings",
    min_value=0.0
)


deadline = st.date_input(
    "Deadline",
    date.today()
)



if st.button("Create Goal"):


    db = SessionLocal()


    goal = Goal(
        user_id=st.session_state.user_id,
        goal_name=goal_name,
        target_amount=target,
        saved_amount=saved,
        deadline=deadline
    )


    db.add(goal)

    db.commit()

    db.close()


    st.success(
        "Goal created!"
    )