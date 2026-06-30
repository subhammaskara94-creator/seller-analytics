from amazon.orders import OrdersClient
from amazon.finances import FinancesClient

from pipelines.order_pipeline import build_gold_orders


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

    print("\n========== GOLD ORDERS ==========\n")

    print(gold_df.head())

    print("\n")

    print(gold_df.info())

    print("\n========== PIPELINE SUMMARY ==========\n")

    print(f"Orders Retrieved       : {len(orders)}")
    print(f"Gold Rows Created      : {len(gold_df)}")
    print(f"Cancelled Orders       : (calculate this)")
    print(f"Skipped (API Errors)   : (calculate this)")

if __name__ == "__main__":
    main()