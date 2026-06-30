FEE_MAPPING = {
    ("Shipment", "Principal"): "gross_sales",
    ("Refund", "Principal"): "refunded_sales",

    ("Shipment", "Commission"): "commission",
    ("Refund", "Commission"): "commission_refund",

    ("Shipment", "FixedClosingFee"): "closing_fee",
    ("Refund", "FixedClosingFee"): "closing_fee_refund",

    ("ServiceFee", "MFNPostageFee"): "shipping_fee",
    ("Adjustment", "PostageRefund"): "shipping_refund",

    ("Shipment", "ItemTDS"): "tds",
}