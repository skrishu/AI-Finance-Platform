def generate_insights(
    income,
    expenses,
    expense_df
):

    insights = []


    # No data case
    if income == 0:
        return [
            "Add your income to generate insights."
        ]


    total_expense = expenses


    savings = income - total_expense


    savings_rate = (
        savings / income
    ) * 100



    # Savings insight

    if savings_rate >= 30:

        insights.append(
            "🎉 Great job! Your savings rate is healthy."
        )

    elif savings_rate >= 10:

        insights.append(
            "👍 You are saving, but there is room for improvement."
        )

    else:

        insights.append(
            "⚠️ Your savings rate is low. Consider reducing unnecessary expenses."
        )



    # Expense category insight

    if not expense_df.empty:


        category_total = (
            expense_df
            .groupby("Category")["Amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )


        highest_category = (
            category_total.index[0]
        )


        highest_amount = (
            category_total.iloc[0]
        )


        insights.append(
            f"💡 Your highest spending category is {highest_category} "
            f"(₹{highest_amount:,.0f})."
        )


    # Budget warning

    if total_expense > income:

        insights.append(
            "🚨 You have exceeded your income. Review your spending."
        )


    elif total_expense > income * 0.8:

        insights.append(
            "⚠️ You have used more than 80% of your income."
        )


    return insights