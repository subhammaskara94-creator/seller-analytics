import pandas as pd

from transform.orders import build_silver_order
from transform.financial_events import flatten_financial_events

from services.profitability import (
    aggregate_ledger,
    calculate_financial_summary,
    build_gold_order,
    calculate_profitability,
)

from services.pricing import (
    load_pricing_history,
    find_effective_price,
)

def build_gold_orders(
    orders,
    orders_client,
    finance_client,
):
    """
    Build a Gold Orders DataFrame for all non-cancelled orders.
    """

    pricing_df = load_pricing_history()
    gold_orders = []

    for order in orders:

        if order["OrderStatus"] == "Canceled":
            continue

        try:

            # Get order items
            items_response = orders_client.get_order_items(
                order["AmazonOrderId"]
            )

            items = items_response.payload.get("OrderItems", [])

            if not items:
                continue

            # Get financial events once per order
            financials = finance_client.get_order_financial_events(
                order["AmazonOrderId"]
            )

            ledger_rows = flatten_financial_events(
                financials.payload
            )

            ledger = aggregate_ledger(
                ledger_rows
            )

            financial_summary = calculate_financial_summary(
                ledger
            )
            financial_summary["financial_status"] = "COMPLETE"

            # Build one Gold row per item
            for item in items:

                silver_order = build_silver_order(
                    order,
                    item,
                )

                pricing = find_effective_price(
                    asin=silver_order["asin"],
                    purchase_date=silver_order["purchase_date"],
                    pricing_df=pricing_df,
                )

                gold_order = build_gold_order(
                    silver_order,
                    financial_summary,
                    pricing,
                )

                gold_order = calculate_profitability(
                    gold_order
                )

                gold_orders.append(
                    gold_order
                )

        except Exception as e:

            print(
                f"Skipping Order {order['AmazonOrderId']} -> {e}"
            )

            continue

    return pd.DataFrame(gold_orders)