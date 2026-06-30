def flatten_financial_events(payload):
    rows = []

    events = payload.get("FinancialEvents", {})

    # Shipment Events
    for shipment in events.get("ShipmentEventList", []):

        order_id = shipment["AmazonOrderId"]
        posted_date = shipment["PostedDate"]

        for item in shipment.get("ShipmentItemList", []):

            order_item_id = item["OrderItemId"]

            # Charges (Principal, Tax, etc.)
            for charge in item.get("ItemChargeList", []):
                rows.append({
                    "amazon_order_id": order_id,
                    "order_item_id": order_item_id,
                    "event_type": "Shipment",
                    "event_category": charge["ChargeType"],
                    "amount": charge["ChargeAmount"]["CurrencyAmount"],
                    "posted_date": posted_date,
                })

            # Fees (Commission, Closing Fee, etc.)
            for fee in item.get("ItemFeeList", []):
                rows.append({
                    "amazon_order_id": order_id,
                    "order_item_id": order_item_id,
                    "event_type": "Shipment",
                    "event_category": fee["FeeType"],
                    "amount": fee["FeeAmount"]["CurrencyAmount"],
                    "posted_date": posted_date,
                })

    return rows