import pandas as pd
from database import engine


def get_visit_metrics():
    """Queries Postgres logs and computes metrics using Pandas."""
    query = "SELECT id, path, referrer, user_agent, timestamp FROM visitlog"
    df = pd.read_sql(query, engine)

    if df.empty:
        return {"total_visits": 0}

    total_visits = len(df)

    return {
        "total_visits": total_visits,
    }
