import pandas as pd


def export_transactions(expense_df):

    if expense_df.empty:
        return None


    csv = expense_df.to_csv(
        index=False
    )

    return csv