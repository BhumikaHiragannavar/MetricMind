import pandas as pd


# ============================================================
# METRICMIND - SEMANTIC LAYER
# ============================================================

# ------------------------------------------------------------
# BUSINESS METRICS
# ------------------------------------------------------------

METRICS = {
    "revenue": "Sales",
    "profit": "Profit",
    "quantity": "Quantity",
    "shipping_cost": "Shipping.Cost",
    "discount": "Discount",
}


# ------------------------------------------------------------
# BUSINESS DIMENSIONS
# ------------------------------------------------------------

DIMENSIONS = {
    "time": "Order.Date",
    "month": "Order.Date",
    "year": "Year",

    "region": "Region",
    "country": "Country",
    "state": "State",
    "city": "City",
    "market": "Market",

    "category": "Category",
    "sub_category": "Sub-Category",
    "product": "Product.Name",

    "segment": "Segment",
    "ship_mode": "Ship.Mode",
}


# ------------------------------------------------------------
# DERIVED METRICS
# ------------------------------------------------------------

DERIVED_METRICS = {
    "margin": "Profit / Sales * 100",
}


# Complete semantic definition
SEMANTIC_LAYER = {
    "metrics": METRICS,
    "dimensions": DIMENSIONS,
    "derived_metrics": DERIVED_METRICS,
}


# ============================================================
# HELPERS
# ============================================================

def _clean_value(value):
    """
    Convert Pandas / NumPy values into normal Python values
    so FastAPI can safely return JSON.
    """

    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        value = value.item()

    if isinstance(value, (int, float)):
        return value

    return str(value)


# ============================================================
# SINGLE METRIC
# ============================================================

def calculate_metric(df, metric_name):
    """
    Calculate a metric for the complete dataset.
    """

    metric_name = metric_name.lower().strip()

    if metric_name == "revenue":
        return float(df["Sales"].sum())

    if metric_name == "profit":
        return float(df["Profit"].sum())

    if metric_name == "quantity":
        return int(df["Quantity"].sum())

    if metric_name == "shipping_cost":
        return float(df["Shipping.Cost"].sum())

    if metric_name == "discount":
        return float(df["Discount"].sum())

    # Margin is calculated from aggregated profit and sales.
    if metric_name == "margin":

        total_sales = float(df["Sales"].sum())
        total_profit = float(df["Profit"].sum())

        if total_sales == 0:
            return 0.0

        return float((total_profit / total_sales) * 100)

    raise ValueError(f"Unknown metric: {metric_name}")


# ============================================================
# METRIC BY DIMENSION
# ============================================================

def calculate_by_dimension(df, metric_name, dimension_name):
    """
    Calculate a metric grouped by a semantic dimension.
    """

    metric_name = metric_name.lower().strip()
    dimension_name = dimension_name.lower().strip()

    if dimension_name not in DIMENSIONS:
        raise ValueError(f"Unknown dimension: {dimension_name}")

    working_df = df.copy()

    # --------------------------------------------------------
    # MONTH
    # --------------------------------------------------------

    if dimension_name == "month":

        working_df["Month"] = (
            pd.to_datetime(
                working_df["Order.Date"],
                errors="coerce"
            ).dt.month
        )

        dimension_column = "Month"

    else:
        dimension_column = DIMENSIONS[dimension_name]

    # --------------------------------------------------------
    # MARGIN
    # --------------------------------------------------------

    if metric_name == "margin":

        grouped = (
            working_df
            .groupby(dimension_column)
            .agg(
                Profit=("Profit", "sum"),
                Sales=("Sales", "sum")
            )
        )

        result = {}

        for key, row in grouped.iterrows():

            sales = float(row["Sales"])
            profit = float(row["Profit"])

            if sales == 0:
                margin = 0.0
            else:
                margin = (profit / sales) * 100

            result[str(_clean_value(key))] = round(float(margin), 4)

        return result

    # --------------------------------------------------------
    # NORMAL METRICS
    # --------------------------------------------------------

    if metric_name not in METRICS:
        raise ValueError(f"Unknown metric: {metric_name}")

    metric_column = METRICS[metric_name]

    grouped = (
        working_df
        .groupby(dimension_column)[metric_column]
        .sum()
    )

    result = {}

    for key, value in grouped.items():

        clean_key = str(_clean_value(key))

        if metric_name == "quantity":
            result[clean_key] = int(value)
        else:
            result[clean_key] = round(float(value), 4)

    return result