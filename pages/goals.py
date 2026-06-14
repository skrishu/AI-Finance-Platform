import streamlit as st
from datetime import date

from database.db import SessionLocal
from database.models import Goal

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/login.py")

st.title("🎯 Savings Goals")


if "logged_in" not in st.session_state:
    st.stop()


# ---------------- CREATE GOAL ----------------

st.subheader("Create New Goal")


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

    st.rerun()



# ---------------- FETCH GOALS ----------------

db = SessionLocal()

goals = db.query(Goal).filter(
    Goal.user_id == st.session_state.user_id
).all()

db.close()



# ---------------- DISPLAY GOALS ----------------

st.subheader("📌 Your Goals")


if not goals:

    st.info(
        "No goals created yet."
    )


else:

    for goal in goals:

        progress = (
            goal.saved_amount /
            goal.target_amount
        )

        progress = min(progress, 1.0)


        st.write(
            f"### {goal.goal_name}"
        )


        st.progress(progress)


        st.caption(
            f"₹{goal.saved_amount:,.0f} saved "
            f"out of ₹{goal.target_amount:,.0f}"
        )



# ---------------- UPDATE GOAL ----------------

st.subheader("✏️ Update Goal")


goal_options = {
    goal.goal_name: goal.id
    for goal in goals
}



if goal_options:

    selected_goal = st.selectbox(
        "Select Goal",
        goal_options.keys()
    )


    selected_id = goal_options[selected_goal]


    new_saved = st.number_input(
        "Update Saved Amount",
        min_value=0.0
    )



    if st.button("Update Goal"):

        db = SessionLocal()


        goal = db.query(Goal).filter(
            Goal.id == selected_id
        ).first()


        goal.saved_amount = new_saved


        db.commit()
        db.close()


        st.success(
            "Goal updated!"
        )

        st.rerun()