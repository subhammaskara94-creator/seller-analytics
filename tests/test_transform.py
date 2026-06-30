from transform.silver import build_order_item


def test_transform():

    order = {
        "AmazonOrderId": "123"
    }

    item = {
        "OrderItemId": "456",
        "ASIN": "ABC",
        "SellerSKU": "SKU",
        "Title": "Test",
        "QuantityOrdered": 1,
        "QuantityShipped": 1
    }

    result = build_order_item(order, item)

    assert result["amazon_order_id"] == "123"