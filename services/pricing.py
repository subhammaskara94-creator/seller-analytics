import pandas as pd


def load_pricing_history(filepath="data/product_master.csv"):

    df = pd.read_csv(filepath)

    df["effective_from"] = pd.to_datetime(
        df["effective_from"]
    )

    df["landed_cost"] = df["landed_cost"].astype(float)

    df["offline_selling_price"] = (
        df["offline_selling_price"]
        .astype(float)
    )

    return df


def find_effective_price(
    asin,
    purchase_date,
    pricing_df,
):
    """
    Returns the pricing row effective on the purchase date.
    """

    purchase_date = (
        pd.to_datetime(purchase_date)
        .tz_localize(None)
    )

    product_prices = pricing_df[
        pricing_df["asin"] == asin
    ]

    if product_prices.empty:
        return None

    valid_prices = product_prices[
        product_prices["effective_from"] <= purchase_date
    ]

    if valid_prices.empty:
        return None

    valid_prices = valid_prices.sort_values(
        "effective_from",
        ascending=False,
    )

    return valid_prices.iloc[0].to_dict()