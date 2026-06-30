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