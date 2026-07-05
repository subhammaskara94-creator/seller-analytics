import pandas as pd


def summarize_by_asin(gold_df):
    """
    Summarize profitability by ASIN.
    """

    report = (
        gold_df.groupby(
            [
                "asin",
                "product_name",
                "supplier",
            ],
            dropna=False,
        )
        .agg(
            orders=("amazon_order_id", "nunique"),
            units_sold=("quantity_ordered", "sum"),
            gross_sales=("gross_sales", "sum"),
            amazon_settlement=("amazon_net_revenue", "sum"),
            ecommerce_profit=("ecommerce_profit", "sum"),
            offline_profit=("offline_profit", "sum"),
            channel_premium=("channel_premium", "sum"),
        )
        .reset_index()
    )

    report = report.sort_values(
        "ecommerce_profit",
        ascending=False,
    )

    return report