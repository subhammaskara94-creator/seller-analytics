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

    Pricing is optional for now. It will be joined in the next commit.
    """

    gold = silver_order.copy()

    gold.update(financial_summary)

    pricing = pricing or {}

    gold["landed_cost"] = pricing.get("landed_cost")
    gold["offline_selling_price"] = pricing.get("offline_selling_price")

    # Placeholder fields (next commit)
    gold["ecommerce_profit"] = None
    gold["offline_profit"] = None
    gold["channel_premium"] = None

    return gold