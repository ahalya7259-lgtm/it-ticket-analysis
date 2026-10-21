"""Creates a dummy (synthetic) IT service desk ticket dataset.
Run: python generate_data.py
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 5000

categories = ["Password Reset", "Software Issue", "Network Issue", "Hardware Issue", "Email Issue", "Access Request"]
cat_prob = [0.30, 0.22, 0.14, 0.12, 0.12, 0.10]
priorities = ["Critical", "High", "Medium", "Low"]
agents = ["Ravi", "Priya", "Arjun", "Meena", "Kiran", "Divya", "Suresh", "Anita"]

# base resolution hours by category (Network and Hardware take longer)
base = {"Password Reset": 1, "Software Issue": 6, "Network Issue": 12,
        "Hardware Issue": 18, "Email Issue": 4, "Access Request": 8}
pr_mult = {"Critical": 0.6, "High": 0.8, "Medium": 1.0, "Low": 1.4}

# more tickets on Mondays, fewer on weekends
start = pd.Timestamp("2025-01-01")
days = pd.date_range(start, "2025-12-31")
w = np.array([1.5 if d.dayofweek == 0 else 0.3 if d.dayofweek >= 5 else 1.0 for d in days])
opened_day = rng.choice(days, size=N, p=w / w.sum())
opened = pd.to_datetime(opened_day) + pd.to_timedelta(rng.integers(8 * 60, 19 * 60, N), unit="m")

cat = rng.choice(categories, size=N, p=cat_prob)
pri = rng.choice(priorities, size=N, p=[0.05, 0.20, 0.50, 0.25])
agent = rng.choice(agents, size=N)

hours = np.array([base[c] * pr_mult[p] for c, p in zip(cat, pri)]) * rng.lognormal(0, 0.6, N)
hours = np.where(agent == "Suresh", hours * 1.6, hours)   # one slower agent
hours = np.where(agent == "Priya", hours * 0.75, hours)   # one faster agent
closed = opened + pd.to_timedelta(hours, unit="h")

status = rng.choice(["Closed", "Resolved", "Open"], size=N, p=[0.62, 0.34, 0.04])
closed = pd.Series(closed).where(status != "Open")

# rating: lower when slow
rating = np.clip(np.round(5 - hours / 12 + rng.normal(0, 0.8, N)), 1, 5).astype(float)
rating[status == "Open"] = np.nan

df = pd.DataFrame({
    "ticket_id": [f"INC{100000 + i}" for i in range(N)],
    "date_opened": opened,
    "date_closed": closed,
    "category": cat,
    "priority": pri,
    "agent": agent,
    "status": status,
    "customer_rating": rating,
})

# ---- make the data a little messy so cleaning is real practice ----
df.loc[rng.choice(N, 60, replace=False), "category"] = df["category"].str.upper()
df.loc[rng.choice(N, 40, replace=False), "priority"] = df["priority"].str.lower()
df.loc[rng.choice(N, 80, replace=False), "customer_rating"] = np.nan
df.loc[rng.choice(N, 30, replace=False), "agent"] = None
df = pd.concat([df, df.sample(50, random_state=1)], ignore_index=True)  # duplicates

df.to_csv("data/tickets_raw.csv", index=False)
print("Saved data/tickets_raw.csv with", len(df), "rows")
