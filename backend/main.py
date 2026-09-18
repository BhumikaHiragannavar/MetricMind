from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from semantic_layer import (
    SEMANTIC_LAYER,
    calculate_metric,
    calculate_by_dimension,
)

from agent import execute_question


# ============================================================
# METRICMIND API
# ============================================================

app = FastAPI(
    title="MetricMind API",
    description="Agentic Semantic BI Engine",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATASET
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "data" / "superstore.csv"

df = pd.read_csv(DATA_PATH)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "message": "MetricMind API is running",
        "dataset": "superstore.csv",
        "rows": int(len(df)),
    }


# ============================================================
# SUMMARY
# ============================================================

@app.get("/summary")
def summary():

    return {
        "total_sales": float(df["Sales"].sum()),
        "total_profit": float(df["Profit"].sum()),
        "total_quantity": int(df["Quantity"].sum()),
        "profit_margin": float(
            (df["Profit"].sum() /
             df["Sales"].sum()) * 100
        ),
    }


# ============================================================
# SEMANTIC LAYER
# ============================================================

@app.get("/semantic-layer")
def semantic_layer():

    return SEMANTIC_LAYER


# ============================================================
# SINGLE METRIC
# ============================================================

@app.get("/metric/{metric_name}")
def metric(metric_name: str):

    try:

        value = calculate_metric(
            df,
            metric_name
        )

        return {
            "metric": metric_name,
            "value": value,
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# METRIC BY DIMENSION
# ============================================================

@app.get("/metric/{metric_name}/by/{dimension}")
def metric_by_dimension(
    metric_name: str,
    dimension: str
):

    try:

        values = calculate_by_dimension(
            df,
            metric_name,
            dimension
        )

        return {
            "metric": metric_name,
            "dimension": dimension,
            "values": values,
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# ASK METRICMIND
# ============================================================

@app.post("/ask")
def ask(question: str):

    try:

        return execute_question(
            question,
            df
        )

    except Exception as error:

        # Return a useful error instead of an unexplained
        # "Internal Server Error".
        raise HTTPException(
            status_code=500,
            detail=f"MetricMind could not process the question: {error}"
        )


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,
    )