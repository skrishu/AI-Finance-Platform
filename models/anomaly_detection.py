import pandas as pd
from sklearn.ensemble import IsolationForest



def detect_anomalies(expense_df):

    if expense_df.empty:
        return expense_df


    if len(expense_df) < 5:
        return None


    data = expense_df[
        ["Amount"]
    ]


    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )


    expense_df["anomaly"] = model.fit_predict(
        data
    )


    anomalies = expense_df[
        expense_df["anomaly"] == -1
    ]


    return anomalies