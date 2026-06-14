import streamlit as st
import pandas as pd
import plotly.express as px

from utils.insights import generate_insights
from database.db import SessionLocal
from database.models import Expense, Income, Goal

from models.expense_model import (
    train_expense_model,
    predict_next_month
)

from utils.health_score import calculate_health_score
from utils.recommendations import generate_recommendations
from models.anomaly_detection import detect_anomalies

from utils.export import export_transactions
from utils.report import create_report


# ---------------- LOGIN CHECK ----------------

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/login.py")


user_id = st.session_state.user_id


# ---------------- PAGE ----------------

st.title("💰 AI Finance Dashboard")


# ---------------- DATABASE ----------------

db = SessionLocal()


expenses = db.query(Expense).filter(
    Expense.user_id == user_id
).all()


income = db.query(Income).filter(
    Income.user_id == user_id
).all()


goals = db.query(Goal).filter(
    Goal.user_id == user_id
).all()


db.close()



expense_df = pd.DataFrame(
    [
        {
            "Date": e.date,
            "Amount": e.amount,
            "Category": e.category,
            "Description": e.description
        }
        for e in expenses
    ]
)


income_df = pd.DataFrame(
    [
        {
            "Date": i.date,
            "Amount": i.amount
        }
        for i in income
    ]
)



if expense_df.empty and income_df.empty:

    st.info(
        "No transactions yet. Add income or expenses first."
    )

    st.stop()



# ---------------- CALCULATIONS ----------------


total_income = (
    income_df["Amount"].sum()
    if not income_df.empty
    else 0
)


total_expense = (
    expense_df["Amount"].sum()
    if not expense_df.empty
    else 0
)


savings = total_income - total_expense


savings_rate = (
    savings / total_income * 100
    if total_income > 0
    else 0
)



# ---------------- TOP CARDS ----------------


st.subheader("📌 Financial Overview")


c1,c2,c3,c4 = st.columns(4)


c1.metric(
    "💰 Income",
    f"₹{total_income:,.0f}"
)


c2.metric(
    "💸 Expenses",
    f"₹{total_expense:,.0f}"
)


c3.metric(
    "🏦 Savings",
    f"₹{savings:,.0f}"
)


c4.metric(
    "📈 Savings Rate",
    f"{savings_rate:.1f}%"
)



# ---------------- HEALTH ----------------


score, breakdown = calculate_health_score(
    total_income,
    total_expense,
    savings,
    expense_df
)



st.subheader(
    "🩺 Financial Health"
)


h1,h2 = st.columns([2,1])


with h1:

    st.metric(
        "Financial Health Score",
        f"{score}/100",
        help="""
Calculated using:

• Savings behaviour
• Expense control
• Emergency fund
• Debt management

This is a personal wellness indicator,
not a credit score.
"""
    )



with h2:

    st.write("Score Breakdown")

    for k,v in breakdown.items():

        st.write(
            f"{k}: {v}"
        )



# ---------------- CHARTS ----------------


if not expense_df.empty:


    left,right = st.columns(2)


    category_data = (
        expense_df
        .groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )


    fig1 = px.pie(
        category_data,
        values="Amount",
        names="Category",
        title="Expense Breakdown"
    )


    left.plotly_chart(
        fig1,
        use_container_width=True
    )



    expense_df["Date"] = pd.to_datetime(
        expense_df["Date"]
    )


    monthly = (
        expense_df
        .groupby(
            expense_df["Date"].dt.to_period("M")
        )["Amount"]
        .sum()
        .reset_index()
    )


    monthly["Date"] = monthly["Date"].astype(str)


    fig2 = px.line(
        monthly,
        x="Date",
        y="Amount",
        markers=True,
        title="Monthly Spending Trend"
    )


    right.plotly_chart(
        fig2,
        use_container_width=True
    )



# ---------------- AI SECTION ----------------


st.subheader(
    "🤖 AI Financial Assistant"
)


for item in generate_insights(
    total_income,
    total_expense,
    expense_df
):

    st.info(item)



# ---------------- ALERTS ----------------


st.subheader(
    "🚨 Spending Alerts"
)


anomalies = detect_anomalies(
    expense_df
)


if anomalies is None:

    st.info(
        "Add more transactions for anomaly detection."
    )


elif anomalies.empty:

    st.success(
        "No unusual spending detected 🎉"
    )


else:

    st.warning(
        "Unusual transactions found"
    )

    st.dataframe(
        anomalies,
        use_container_width=True
    )



# ---------------- FORECAST ----------------


st.subheader(
    "🔮 Expense Forecast"
)


model = train_expense_model(
    expense_df
)


prediction = predict_next_month(
    model,
    expense_df
)


if prediction:

    st.success(
        f"Expected next month spending: ₹{prediction:,.0f}"
    )



# ---------------- GOALS ----------------


st.subheader(
    "🎯 Savings Goals"
)



if not goals:

    st.info(
        "Create a goal to track savings."
    )


else:

    for goal in goals:

        progress = min(
            goal.saved_amount /
            goal.target_amount,
            1
        )


        st.write(
            goal.goal_name
        )


        st.progress(
            progress
        )


        st.caption(
            f"₹{goal.saved_amount:,.0f} / ₹{goal.target_amount:,.0f}"
        )



# ---------------- TRANSACTIONS ----------------


st.subheader(
    "🧾 Recent Transactions"
)


if not expense_df.empty:

    st.dataframe(
        expense_df.sort_values(
            "Date",
            ascending=False
        ),
        use_container_width=True
    )



# ---------------- EXPORT ----------------


st.subheader(
    "⬇️ Export"
)


csv = export_transactions(
    expense_df
)


if csv:

    st.download_button(
        "Download CSV",
        csv,
        file_name="expenses.csv"
    )



if st.button("Generate PDF Report"):


    create_report(
        "finance_report.pdf",
        total_income,
        total_expense,
        savings,
        score
    )


    with open(
        "finance_report.pdf",
        "rb"
    ) as f:

        st.download_button(
            "Download PDF",
            f,
            file_name="finance_report.pdf"
        )