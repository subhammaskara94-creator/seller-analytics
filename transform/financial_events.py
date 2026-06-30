"""
Transforms Amazon SP-API Financial Events into a normalized ledger.

Output grain:
    One row = One accounting entry (charge, fee or adjustment)
"""

def build_financial_row(
    amazon_order_id,
    order_item_id,
    posted_date,
    event_type,
    event_category,
    amount,
):
    return {
        "amazon_order_id": amazon_order_id,
        "order_item_id": order_item_id,
        "posted_date": posted_date,
        "event_type": event_type,
        "event_category": event_category,
        "amount": float(amount),
    }


def parse_shipment_events(events):

    rows = []

    for shipment in events.get("ShipmentEventList", []):

        order_id = shipment.get("AmazonOrderId")
        posted_date = shipment.get("PostedDate")

        for item in shipment.get("ShipmentItemList", []):

            order_item_id = item.get("OrderItemId")

            # Charges
            for charge in item.get("ItemChargeList", []):

                amount = charge["ChargeAmount"]["CurrencyAmount"]

                if amount == 0:
                    continue

                rows.append(
                    build_financial_row(
                        order_id,
                        order_item_id,
                        posted_date,
                        "Shipment",
                        charge["ChargeType"],
                        amount,
                    )
                )

            # Fees
            for fee in item.get("ItemFeeList", []):

                amount = fee["FeeAmount"]["CurrencyAmount"]

                if amount == 0:
                    continue

                rows.append(
                    build_financial_row(
                        order_id,
                        order_item_id,
                        posted_date,
                        "Shipment",
                        fee["FeeType"],
                        amount,
                    )
                )

    return rows


def parse_refund_events(events):

    rows = []

    for refund in events.get("RefundEventList", []):

        order_id = refund.get("AmazonOrderId")
        posted_date = refund.get("PostedDate")

        for item in refund.get("ShipmentItemAdjustmentList", []):

            order_item_id = (
                item.get("OrderItemId")
                or item.get("OrderAdjustmentItemId")
            )

            # Charge Adjustments
            for charge in item.get("ItemChargeAdjustmentList", []):

                amount = charge["ChargeAmount"]["CurrencyAmount"]

                if amount == 0:
                    continue

                rows.append(
                    build_financial_row(
                        order_id,
                        order_item_id,
                        posted_date,
                        "Refund",
                        charge["ChargeType"],
                        amount,
                    )
                )

            # Fee Adjustments
            for fee in item.get("ItemFeeAdjustmentList", []):

                amount = fee["FeeAmount"]["CurrencyAmount"]

                if amount == 0:
                    continue

                rows.append(
                    build_financial_row(
                        order_id,
                        order_item_id,
                        posted_date,
                        "Refund",
                        fee["FeeType"],
                        amount,
                    )
                )

    return rows


def parse_service_fee_events(events):

    rows = []

    for service in events.get("ServiceFeeEventList", []):

        order_id = service.get("AmazonOrderId")

        for fee in service.get("FeeList", []):

            amount = fee["FeeAmount"]["CurrencyAmount"]

            if amount == 0:
                continue

            rows.append(
                build_financial_row(
                    order_id,
                    None,
                    None,
                    "ServiceFee",
                    fee["FeeType"],
                    amount,
                )
            )

    return rows


def parse_adjustment_events(events):

    rows = []

    for adjustment in events.get("AdjustmentEventList", []):

        amount = adjustment["AdjustmentAmount"]["CurrencyAmount"]

        if amount == 0:
            continue

        rows.append(
            build_financial_row(
                None,
                None,
                adjustment.get("PostedDate"),
                "Adjustment",
                adjustment["AdjustmentType"],
                amount,
            )
        )

    return rows


def flatten_financial_events(payload):
    """
    Converts the Amazon Financial Events payload
    into a normalized ledger.
    """

    events = payload.get("FinancialEvents", {})

    rows = []

    rows.extend(parse_shipment_events(events))
    rows.extend(parse_refund_events(events))
    rows.extend(parse_service_fee_events(events))
    rows.extend(parse_adjustment_events(events))

    return rows