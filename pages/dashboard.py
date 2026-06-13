import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.insights import generate_insights
from database.db import SessionLocal
from database.models import Expense, Income
from models.expense_model import (
    train_expense_model,
    predict_next_month
)
from models.anomaly_detection import detect_anomalies
from utils.health_score import calculate_health_score
from utils.recommendations import generate_recommendations
from database.models import Goal
from utils.export import export_transactions
from utils.report import create_report

st.title("📊 Finance Dashboard")


if "logged_in" not in st.session_state:
    st.stop()


user_id = st.session_state.user_id


db = SessionLocal()


# Fetch user transactions
expenses = db.query(Expense).filter(
    Expense.user_id == user_id
).all()


income = db.query(Income).filter(
    Income.user_id == user_id
).all()


db.close()


# Convert to dataframe

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



# Empty state

if expense_df.empty and income_df.empty:

    st.info(
        "No transactions yet. Add income or expenses first."
    )

    st.stop()



# Metrics

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


balance = total_income - total_expense
savings = balance

savings_rate = (
    (savings / total_income) * 100
    if total_income > 0
    else 0
)



col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "💰 Total Income",
    f"₹{total_income:,.0f}"
)


col2.metric(
    "💸 Total Expense",
    f"₹{total_expense:,.0f}"
)


col3.metric(
    "🏦 Remaining Balance",
    f"₹{balance:,.0f}"
)

col4.metric(
    "📈 Savings Rate",
    f"{savings_rate:.1f}%"
)


st.subheader(
    "Financial Health Score",
    help="""
Financial Health Score is a custom metric calculated using:

• Savings Behaviour
• Budget Control
• Emergency Fund Coverage
• Debt Management

Formula:

Score =
35% × Savings Score
+ 25% × Budget Score
+ 20% × Emergency Fund Score
+ 20% × Debt Score

Higher score indicates healthier financial habits.
"""
)
st.caption(
    "This score is an internal financial wellness indicator based on your spending patterns and is not a credit score."
)


score, breakdown = calculate_health_score(
    total_income,
    total_expense,
    savings,
    expense_df
)


st.metric(
    "Health Score",
    f"{score}/100",
    help="Calculated from savings rate, budget usage, emergency fund, and debt indicators."
)


for key,value in breakdown.items():

    st.write(
        f"{key}: {value} points"
    )

st.subheader(
    "📄 Monthly Report"
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
    ) as file:

        st.download_button(
            "Download PDF",
            file,
            file_name="finance_report.pdf"
        )

    
# Financial insights    

st.subheader(
    "🤖 Financial Insights"
)


insights = generate_insights(
    total_income,
    total_expense,
    expense_df
)


for insight in insights:

    st.info(insight)
    

st.subheader(
    "🚨 Spending Alerts"
)


anomalies = detect_anomalies(
    expense_df
)


if anomalies is None:

    st.info(
        "Add more transactions to detect unusual spending."
    )


elif anomalies.empty:

    st.success(
        "No unusual spending detected 🎉"
    )


else:

    st.warning(
        "Unusual transactions found!"
    )


    st.dataframe(
        anomalies[
            [
                "Date",
                "Category",
                "Amount"
            ]
        ],
        use_container_width=True
    )

st.subheader(
    "💡 Smart Recommendations"
)


recommendations = generate_recommendations(
    total_income,
    total_expense,
    expense_df,
    savings
)


for item in recommendations:

    st.info(item)
    

st.subheader(
    "🎯 Savings Goals"
)


db = SessionLocal()


goals = db.query(Goal).filter(
    Goal.user_id == user_id
).all()


db.close()



if not goals:

    st.info(
        "Create a savings goal to track progress."
    )


else:

    for goal in goals:


        progress = (
            goal.saved_amount /
            goal.target_amount
        )


        progress = min(
            progress,
            1.0
        )


        st.write(
            goal.goal_name
        )


        st.progress(
            progress
        )


        st.caption(
            f"₹{goal.saved_amount:,.0f} "
            f"saved out of "
            f"₹{goal.target_amount:,.0f}"
        )
    
# Expense chart

if not expense_df.empty:

    st.subheader(
        "Spending by Category"
    )

    category_data = (
        expense_df
        .groupby("Category")
        ["Amount"]
        .sum()
        .reset_index()
    )


    fig = px.pie(
        category_data,
        values="Amount",
        names="Category",
        title="Expense Distribution"
    )


    st.plotly_chart(fig)

if not expense_df.empty:

    st.subheader(
        "Monthly Expense Trend"
    )


    expense_df["Date"] = pd.to_datetime(
        expense_df["Date"]
    )


    monthly_expense = (
        expense_df
        .groupby(
            expense_df["Date"].dt.to_period("M")
        )
        ["Amount"]
        .sum()
        .reset_index()
    )


    monthly_expense["Date"] = (
        monthly_expense["Date"]
        .astype(str)
    )


    fig2 = px.line(
        monthly_expense,
        x="Date",
        y="Amount",
        markers=True,
        title="Monthly Spending"
    )


    st.plotly_chart(fig2)
    
    
st.subheader(
    "Budget Usage"
)


if total_income > 0:

    usage = (
        total_expense / total_income
    )


    st.progress(
        min(usage,1.0)
    )


    st.write(
        f"You have used {usage*100:.1f}% of your income."
    )

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

else:

    st.info(
        "Add more monthly data to generate forecast."
    )
    
# Expense table

st.subheader(
    "Recent Transactions"
)


if not expense_df.empty:

    st.dataframe(
        expense_df.sort_values(
            "Date",
            ascending=False
        ),
        use_container_width=True
    )
st.subheader(
    "⬇️ Export Data"
)


csv_file = export_transactions(
    expense_df
)


if csv_file:

    st.download_button(
        label="Download Expenses CSV",
        data=csv_file,
        file_name="my_expenses.csv",
        mime="text/csv"
    )