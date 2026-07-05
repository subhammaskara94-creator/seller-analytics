from config.fee_mapping import FEE_MAPPING


def aggregate_ledger(ledger_rows):
    """
    Aggregate Silver Ledger rows into business metrics.
    """

    metrics = {
        "gross_sales": 0.0,
        "refunded_sales": 0.0,

        "commission": 0.0,
        "commission_refund": 0.0,

        "closing_fee": 0.0,
        "closing_fee_refund": 0.0,

        "shipping_fee": 0.0,
        "shipping_refund": 0.0,

        "tds": 0.0,

        "other_fees": 0.0,
    }

    for row in ledger_rows:

        key = (
            row["event_type"],
            row["event_category"],
        )

        metric = FEE_MAPPING.get(key)

        if metric:
            metrics[metric] += row["amount"]
        else:
            metrics["other_fees"] += row["amount"]

    return metrics


def calculate_financial_summary(metrics):
    """
    Calculate financial summary metrics from aggregated ledger.
    """

    summary = metrics.copy()

    summary["net_sales"] = (
        summary["gross_sales"]
        + summary["refunded_sales"]
    )

    summary["net_commission"] = (
        summary["commission"]
        + summary["commission_refund"]
    )

    summary["net_closing_fee"] = (
        summary["closing_fee"]
        + summary["closing_fee_refund"]
    )

    summary["net_shipping_fee"] = (
        summary["shipping_fee"]
        + summary["shipping_refund"]
    )

    summary["amazon_net_revenue"] = (
        summary["net_sales"]
        + summary["net_commission"]
        + summary["net_closing_fee"]
        + summary["net_shipping_fee"]
        + summary["tds"]
        + summary["other_fees"]
    )

    return summary

def build_gold_order(
    silver_order,
    financial_summary,
    pricing=None,
):
    """
    Build a Gold Order row.
    """

    gold = silver_order.copy()

    # Add all financial metrics
    gold.update(financial_summary)

    # Add pricing attributes
    pricing = pricing or {}

    gold["landed_cost"] = pricing.get("landed_cost")
    gold["offline_selling_price"] = pricing.get("offline_selling_price")
    gold["mrp"] = pricing.get("mrp")
    gold["supplier"] = pricing.get("supplier")
    gold["remarks"] = pricing.get("remarks")

    # --------------------------------------------------
    # Settlement Status
    # --------------------------------------------------

    gold["settlement_status"] = (
        "SETTLED"
        if financial_summary["gross_sales"] != 0
        else "PENDING"
    )

    # --------------------------------------------------
    # Business Outcome
    # --------------------------------------------------

    gold["order_outcome"] = "COMPLETED"

    # Fully refunded order
    if (
        financial_summary["gross_sales"] > 0
        and financial_summary["net_sales"] == 0
    ):
        gold["order_outcome"] = "RETURNED"

    # Settlement not yet generated
    if gold["settlement_status"] == "PENDING":
        gold["order_outcome"] = "PENDING_SETTLEMENT"

    return gold

def calculate_profitability(gold_order):
    """
    Calculate profitability metrics for a Gold Order.
    """

    order = gold_order.copy()

    landed_cost = order.get("landed_cost")
    offline_price = order.get("offline_selling_price")

    # Initialize output columns for every row
    order["total_landed_cost"] = None
    order["offline_revenue"] = None
    order["ecommerce_profit"] = None
    order["offline_profit"] = None
    order["channel_premium"] = None
    
    # If pricing is unavailable, skip calculations
    if landed_cost is None or offline_price is None:
        return order
    
    # Don't calculate profitability until Amazon has settled the order
    if order["settlement_status"] == "PENDING":
        return order

    if order["order_outcome"] == "COMPLETED":

        order["total_landed_cost"] = (
            landed_cost
            * order["quantity_ordered"]
        )

    else:

        order["total_landed_cost"] = 0

    order["offline_revenue"] = (
        offline_price
        * order["quantity_ordered"]
    )

    order["ecommerce_profit"] = (
        order["amazon_net_revenue"]
        - order["total_landed_cost"]
    )

    order["offline_profit"] = (
        order["offline_revenue"]
        - order["total_landed_cost"]
    )

    order["channel_premium"] = (
        order["ecommerce_profit"]
        - order["offline_profit"]
    )

    return order