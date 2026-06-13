def generate_recommendations(
    income,
    expenses,
    expense_df,
    savings
):

    recommendations = []


    if income == 0:
        return [
            "Add income details to generate recommendations."
        ]


    savings_rate = (
        savings / income
    ) * 100


    # Savings advice

    if savings_rate < 20:

        target = income * 0.2

        difference = target - savings


        recommendations.append(
            f"💡 Try increasing savings by "
            f"₹{difference:,.0f} to reach a 20% savings rate."
        )



    # Category advice

    if not expense_df.empty:

        category_total = (
            expense_df
            .groupby("Category")["Amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )


        top_category = category_total.index[0]

        top_amount = category_total.iloc[0]


        saving_opportunity = (
            top_amount * 0.1
        )


        recommendations.append(
            f"📌 {top_category} is your highest expense category. "
            f"Reducing it by 10% can save around "
            f"₹{saving_opportunity:,.0f}."
        )



    # Overspending

    if expenses > income:

        recommendations.append(
            "🚨 Your expenses exceed income. "
            "Review your spending immediately."
        )


    return recommendations