from amazon.orders import OrdersClient
from amazon.finances import FinancesClient

from pipelines.order_pipeline import build_gold_orders
from reports.profitability import summarize_by_asin


def main():

    print("Connecting to Amazon...\n")

    orders_client = OrdersClient()
    finance_client = FinancesClient()

    response = orders_client.get_recent_orders(days=30)

    orders = response.payload.get(
        "Orders",
        [],
    )

    print(f"Retrieved {len(orders)} orders.\n")

    gold_df = build_gold_orders(
        orders,
        orders_client,
        finance_client,
    )

    print(
        gold_df[
            [
                "amazon_order_id",
                "settlement_status",
                "order_outcome",
                "amazon_net_revenue",
                "total_landed_cost",
                "ecommerce_profit",
            ]
        ].head(20)
    )

#     pygmy = gold_df[
#     gold_df["asin"] == "B08VRGH6NM"
# ]

#     print(
#         pygmy[
#             [
#                 "amazon_order_id",
#                 "order_status",
#                 "financial_status",
#                 "gross_sales",
#                 "amazon_net_revenue",
#                 "ecommerce_profit",
#             ]
#         ]
#     )

    # order_id = "408-9997704-8934743"

    # financials = finance_client.get_order_financial_events(order_id)

    # from utils.pretty import show 

    # show(financials.payload)


if __name__ == "__main__":
    main()