def flatten_order(order: dict) -> dict:
    return {
        "amazon_order_id": order.get("AmazonOrderId"),
        "purchase_date": order.get("PurchaseDate"),
        "last_update_date": order.get("LastUpdateDate"),
        "order_status": order.get("OrderStatus"),
        "shipment_status": order.get("EasyShipShipmentStatus"),
        "payment_method": order.get("PaymentMethod"),
        "fulfillment_channel": order.get("FulfillmentChannel"),
        "marketplace_id": order.get("MarketplaceId"),
        "order_total": float(
            order.get("OrderTotal", {}).get("Amount", 0)
        )
    }

from transform.order_items import flatten_order_item


def build_silver_order(order: dict, item: dict) -> dict:
    """
    Combine a flattened order and a flattened order item
    into a single Silver Order record.
    """

    silver_order = {}

    silver_order.update(flatten_order(order))
    silver_order.update(flatten_order_item(item))

    return silver_order