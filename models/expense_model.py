import pandas as pd
from sklearn.linear_model import LinearRegression


def prepare_expense_data(expense_df):

    if expense_df.empty:
        return None, None


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


    monthly["month_number"] = range(
        len(monthly)
    )


    monthly["Date"] = (
        monthly["Date"]
        .astype(str)
    )


    X = monthly[
        ["month_number"]
    ]

    y = monthly["Amount"]


    return X, y



def train_expense_model(expense_df):

    X, y = prepare_expense_data(
        expense_df
    )


    if X is None:
        return None


    if len(X) < 2:
        return None


    model = LinearRegression()


    model.fit(
        X,
        y
    )


    return model



def predict_next_month(model, expense_df):

    if model is None:
        return None


    next_month = len(expense_df)


    prediction = model.predict(
        [[next_month]]
    )


    return prediction[0]