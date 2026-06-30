from amazon.orders import OrdersClient
from amazon.finances import FinancesClient
from transform.financial_events import flatten_financial_events

import pandas as pd


def main():

    orders_client = OrdersClient()
    finance_client = FinancesClient()

    # Get a recent non-cancelled order
    response = orders_client.get_recent_orders(days=30)

    orders = response.payload["Orders"]

    order = next(
        (o for o in orders if o["OrderStatus"] != "Canceled"),
        orders[0]
    )

    print(f"Testing Order: {order['AmazonOrderId']}")

    financials = finance_client.get_order_financial_events(
        order["AmazonOrderId"]
    )

    rows = flatten_financial_events(financials.payload)

    print(f"\nParsed {len(rows)} financial rows\n")

    df = pd.DataFrame(rows)

    print(df)


if __name__ == "__main__":
    main()