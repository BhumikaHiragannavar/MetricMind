from semantic_layer import calculate_by_dimension, calculate_metric
import pandas as pd


# Load the dataset
df = pd.read_csv("../data/superstore.csv")


# ---------------------------------------------------------
# 1. UNDERSTAND THE METRIC
# ---------------------------------------------------------

def understand_question(question):
    question_lower = question.lower()

    if "revenue" in question_lower or "sales" in question_lower:
        metric = "revenue"

    elif "profit" in question_lower:
        metric = "profit"

    elif "margin" in question_lower:
        metric = "margin"

    elif "quantity" in question_lower:
        metric = "quantity"

    elif "shipping cost" in question_lower:
        metric = "shipping_cost"

    elif "discount" in question_lower:
        metric = "discount"

    else:
        metric = None

    return {
        "question": question,
        "metric": metric
    }


# ---------------------------------------------------------
# 2. DETECT THE DIMENSION
# ---------------------------------------------------------

def detect_dimension(question):
    question_lower = question.lower()

    if "sub-category" in question_lower or "subcategory" in question_lower:
        return "sub_category"

    elif "category" in question_lower:
        return "category"

    elif "region" in question_lower:
        return "region"

    elif "country" in question_lower:
        return "country"

    elif "state" in question_lower:
        return "state"

    elif "city" in question_lower:
        return "city"

    elif "year" in question_lower:
        return "year"

    elif "month" in question_lower:
        return "month"

    elif "product" in question_lower:
        return "product"

    else:
        return None


# ---------------------------------------------------------
# 3. ANALYZE THE QUESTION
# ---------------------------------------------------------

def analyze_question(question):
    result = understand_question(question)

    result["dimension"] = detect_dimension(question)

    return result


# ---------------------------------------------------------
# 4. INVESTIGATE PROFIT
# ---------------------------------------------------------

def investigate_profit(df):
    # Profit by year
    yearly_profit = (
        df.groupby("Year")["Profit"]
        .sum()
        .sort_index()
    )

    # Profit by region
    region_profit = (
        df.groupby("Region")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    # Profit by category
    category_profit = (
        df.groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    # Profit by sub-category
    subcategory_profit = (
        df.groupby("Sub-Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    # Profit by market
    market_profit = (
        df.groupby("Market")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    highest_year = int(yearly_profit.idxmax())
    lowest_year = int(yearly_profit.idxmin())

    highest_year_profit = float(yearly_profit.max())
    lowest_year_profit = float(yearly_profit.min())

    top_region = str(region_profit.idxmax())
    top_region_profit = float(region_profit.max())

    bottom_region = str(region_profit.idxmin())
    bottom_region_profit = float(region_profit.min())

    top_category = str(category_profit.idxmax())
    top_category_profit = float(category_profit.max())

    bottom_category = str(category_profit.idxmin())
    bottom_category_profit = float(category_profit.min())

    top_subcategory = str(subcategory_profit.idxmax())
    top_subcategory_profit = float(subcategory_profit.max())

    bottom_subcategory = str(subcategory_profit.idxmin())
    bottom_subcategory_profit = float(subcategory_profit.min())

    top_market = str(market_profit.idxmax())
    top_market_profit = float(market_profit.max())

    bottom_market = str(market_profit.idxmin())
    bottom_market_profit = float(market_profit.min())

    # -----------------------------------------------------
    # Build a more useful business explanation
    # -----------------------------------------------------

    year_change = highest_year_profit - lowest_year_profit

    explanation = (
        f"Profit was lowest in {lowest_year} at "
        f"{lowest_year_profit:,.2f} and highest in {highest_year} at "
        f"{highest_year_profit:,.2f}. "
        f"The difference between these years was "
        f"{year_change:,.2f}. "
        f"By region, {top_region} generated the highest total profit "
        f"({top_region_profit:,.2f}), while {bottom_region} generated "
        f"the lowest ({bottom_region_profit:,.2f}). "
        f"By category, {top_category} generated the highest profit "
        f"({top_category_profit:,.2f}), while {bottom_category} "
        f"generated the lowest ({bottom_category_profit:,.2f}). "
        f"At the sub-category level, {top_subcategory} had the highest "
        f"profit ({top_subcategory_profit:,.2f}), while "
        f"{bottom_subcategory} had the lowest "
        f"({bottom_subcategory_profit:,.2f})."
    )

    return {
        "yearly_profit": {
            str(year): float(value)
            for year, value in yearly_profit.items()
        },

        "highest_profit_year": highest_year,
        "highest_profit_value": highest_year_profit,

        "lowest_profit_year": lowest_year,
        "lowest_profit_value": lowest_year_profit,

        "profit_change": float(year_change),

        "profit_by_region": {
            str(key): float(value)
            for key, value in region_profit.items()
        },

        "profit_by_category": {
            str(key): float(value)
            for key, value in category_profit.items()
        },

        "profit_by_subcategory": {
            str(key): float(value)
            for key, value in subcategory_profit.items()
        },

        "profit_by_market": {
            str(key): float(value)
            for key, value in market_profit.items()
        },

        "top_region": top_region,
        "top_region_profit": top_region_profit,

        "bottom_region": bottom_region,
        "bottom_region_profit": bottom_region_profit,

        "top_category": top_category,
        "top_category_profit": top_category_profit,

        "bottom_category": bottom_category,
        "bottom_category_profit": bottom_category_profit,

        "top_subcategory": top_subcategory,
        "top_subcategory_profit": top_subcategory_profit,

        "bottom_subcategory": bottom_subcategory,
        "bottom_subcategory_profit": bottom_subcategory_profit,

        "top_market": top_market,
        "top_market_profit": top_market_profit,

        "bottom_market": bottom_market,
        "bottom_market_profit": bottom_market_profit,

        "explanation": explanation
    }


# ---------------------------------------------------------
# 5. EXECUTE THE QUESTION
# ---------------------------------------------------------

def execute_question(question, df):
    result = analyze_question(question)

    question_lower = question.lower()

    # ---------------------------------------------
    # Investigation questions
    # ---------------------------------------------

    if "why" in question_lower:
        result["investigation"] = investigate_profit(df)

    # ---------------------------------------------
    # Metric + dimension questions
    # ---------------------------------------------

    if result["metric"] and result["dimension"]:

        values = calculate_by_dimension(
            df,
            result["metric"],
            result["dimension"]
        )

        result["values"] = {
            str(key): float(value)
            for key, value in values.items()
        }

    # ---------------------------------------------
    # Metric-only questions
    # ---------------------------------------------

    elif result["metric"] and not result["dimension"]:

        result["value"] = calculate_metric(
            df,
            result["metric"]
        )

    # ---------------------------------------------
    # Unknown question
    # ---------------------------------------------

    if not result["metric"]:
        result["message"] = (
            "I could not identify a supported metric. "
            "Try asking about revenue, profit, margin, "
            "quantity, shipping cost, or discount."
        )

    return result