import pandas as pd


def preprocess_input(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])
    # Example: encode transaction_type
    df["transaction_type"] = df["transaction_type"].map({"transfer": 0, "cash_out": 1})
    df.fillna(0, inplace=True)
    return df
