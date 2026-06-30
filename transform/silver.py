def build_order_item(order, item):

    return {

        "amazon_order_id": order["AmazonOrderId"],
        "order_item_id": item["OrderItemId"],

        "purchase_date": order["PurchaseDate"],
        "last_update_date": order["LastUpdateDate"],

        "order_status": order["OrderStatus"],
        "shipment_status": order.get("EasyShipShipmentStatus"),

        "asin": item["ASIN"],
        "seller_sku": item["SellerSKU"],
        "title": item["Title"],

        "quantity_ordered": item["QuantityOrdered"],
        "quantity_shipped": item["QuantityShipped"],

        "selling_price": float(
            item.get("ItemPrice", {}).get("Amount", 0)
        ),

        "promotion_discount": float(
            item.get("PromotionDiscount", {}).get("Amount", 0)
        ),

        "item_tax": float(
            item.get("ItemTax", {}).get("Amount", 0)
        ),

        "payment_method": order.get("PaymentMethod"),
        "fulfillment_channel": order.get("FulfillmentChannel"),
        "marketplace_id": order.get("MarketplaceId"),
    }