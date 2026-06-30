from amazon.orders import OrdersClient
from transform.silver import build_order_item

import pandas as pd


def main():

    orders_client = OrdersClient()

    # Get recent orders
    response = orders_client.get_recent_orders(days=30)
    orders = response.payload.get("Orders", [])

    print(f"\nFound {len(orders)} orders.\n")

    # Pick first non-cancelled order
    order = next(
        (o for o in orders if o["OrderStatus"] != "Canceled"),
        orders[0]
    )

    # Get order items
    items_response = orders_client.get_order_items(
        order["AmazonOrderId"]
    )

    items = items_response.payload["OrderItems"]

    # Build ONE silver row
    silver_order = build_order_item(
        order,
        items[0]
    )

    # Display nicely
    df = pd.DataFrame([silver_order])

    print(df.T)


if __name__ == "__main__":
    main()