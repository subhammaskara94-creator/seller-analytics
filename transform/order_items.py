def flatten_order_item(item: dict) -> dict:
    return {
        "order_item_id": item.get("OrderItemId"),
        "asin": item.get("ASIN"),
        "seller_sku": item.get("SellerSKU"),
        "title": item.get("Title"),
        "quantity_ordered": item.get("QuantityOrdered"),
        "quantity_shipped": item.get("QuantityShipped"),
        "item_price": float(
            item.get("ItemPrice", {}).get("Amount", 0)
        ),
        "promotion_discount": float(
            item.get("PromotionDiscount", {}).get("Amount", 0)
        ),
        "item_tax": float(
            item.get("ItemTax", {}).get("Amount", 0)
        )
    }