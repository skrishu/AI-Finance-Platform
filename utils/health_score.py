def calculate_health_score(
    income,
    expenses,
    savings,
    expense_df
):

    score = 0

    breakdown = {}


    # 1. Savings score (30 points)

    if income > 0:

        savings_rate = (
            savings / income
        ) * 100


        if savings_rate >= 30:
            savings_score = 30

        elif savings_rate >= 20:
            savings_score = 25

        elif savings_rate >= 10:
            savings_score = 15

        else:
            savings_score = 5


    else:
        savings_score = 0


    score += savings_score

    breakdown["Savings"] = savings_score



    # 2. Budget control (30 points)

    if income > 0:

        expense_ratio = (
            expenses / income
        )


        if expense_ratio <= 0.5:
            budget_score = 30

        elif expense_ratio <= 0.75:
            budget_score = 20

        elif expense_ratio <= 1:
            budget_score = 10

        else:
            budget_score = 0


    else:
        budget_score = 0



    score += budget_score

    breakdown["Budget Control"] = budget_score



    # 3. Spending consistency (40 points)

    if not expense_df.empty:

        categories = (
            expense_df["Category"]
            .nunique()
        )


        if categories >= 5:
            consistency_score = 40

        elif categories >= 3:
            consistency_score = 30

        else:
            consistency_score = 15


    else:
        consistency_score = 0


    score += consistency_score

    breakdown["Spending Diversity"] = consistency_score



    return score, breakdown