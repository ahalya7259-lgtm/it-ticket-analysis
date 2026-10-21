"""Clean the data, find insights and save charts.
Run: python generate_data.py  then  python analysis.py
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
df = pd.read_csv("data/tickets_raw.csv", parse_dates=["date_opened", "date_closed"])
print("Raw rows:", len(df))

# ---------- 1. CLEANING ----------
df = df.drop_duplicates()
df["category"] = df["category"].str.title()
df["priority"] = df["priority"].str.title()
df["agent"] = df["agent"].fillna("Unassigned")

# ---------- 2. NEW COLUMNS ----------
df["resolution_hours"] = (df["date_closed"] - df["date_opened"]).dt.total_seconds() / 3600
df["month"] = df["date_opened"].dt.to_period("M").astype(str)
df["weekday"] = df["date_opened"].dt.day_name()

# SLA targets (hours) by priority
sla = {"Critical": 4, "High": 8, "Medium": 24, "Low": 48}
df["sla_target"] = df["priority"].map(sla)
# 1 = breached, 0 = within SLA, blank = ticket still open
df["sla_breached"] = (df["resolution_hours"] > df["sla_target"]).astype(float).where(df["resolution_hours"].notna())

print("Clean rows:", len(df))
df.to_csv("data/tickets_clean.csv", index=False)

closed = df.dropna(subset=["resolution_hours"])

# ---------- 3. KEY NUMBERS ----------
print("\n--- KEY NUMBERS ---")
print("Total tickets:", len(df))
print("Avg resolution (hrs):", round(closed["resolution_hours"].mean(), 1))
print("SLA breach %:", round(closed["sla_breached"].astype(float).mean() * 100, 1))
print("Avg rating:", round(df["customer_rating"].mean(), 2))
print("\nTickets by category (%):")
print((df["category"].value_counts(normalize=True) * 100).round(1))
print("\nAvg resolution hrs by category:")
print(closed.groupby("category")["resolution_hours"].mean().round(1).sort_values())
print("\nSLA breach % by priority:")
print((closed.groupby("priority")["sla_breached"].apply(lambda s: s.astype(float).mean()) * 100).round(1))
print("\nAvg resolution hrs by agent:")
print(closed.groupby("agent")["resolution_hours"].mean().round(1).sort_values())
print("\nTickets by weekday:")
print(df["weekday"].value_counts())
print("\nAvg rating by SLA breached:")
print(closed.groupby("sla_breached")["customer_rating"].mean().round(2))

# ---------- 4. CHARTS ----------
plt.figure(figsize=(8, 4.5))
order = df["category"].value_counts().index
sns.countplot(data=df, y="category", order=order, color="#2E75B6")
plt.title("Tickets by Category"); plt.xlabel("Tickets"); plt.ylabel("")
plt.tight_layout(); plt.savefig("images/01_tickets_by_category.png", dpi=150); plt.close()

plt.figure(figsize=(8, 4.5))
avg = closed.groupby("category")["resolution_hours"].mean().sort_values()
avg.plot(kind="barh", color="#ED7D31")
plt.title("Average Resolution Time by Category (hours)"); plt.ylabel("")
plt.tight_layout(); plt.savefig("images/02_resolution_by_category.png", dpi=150); plt.close()

plt.figure(figsize=(8, 4.5))
m = df.groupby("month").size()
m.plot(marker="o", color="#2E75B6")
plt.title("Monthly Ticket Volume"); plt.xticks(rotation=45); plt.xlabel(""); plt.ylabel("Tickets")
plt.tight_layout(); plt.savefig("images/03_monthly_volume.png", dpi=150); plt.close()

plt.figure(figsize=(7, 4.5))
b = (closed.groupby("priority")["sla_breached"].apply(lambda s: s.astype(float).mean() * 100)
     .reindex(["Critical", "High", "Medium", "Low"]))
b.plot(kind="bar", color="#C0392B")
plt.title("SLA Breach % by Priority"); plt.ylabel("%"); plt.xlabel(""); plt.xticks(rotation=0)
plt.tight_layout(); plt.savefig("images/04_sla_by_priority.png", dpi=150); plt.close()

plt.figure(figsize=(8, 4.5))
ag = closed.groupby("agent")["resolution_hours"].mean().sort_values()
ag.plot(kind="bar", color="#70AD47")
plt.title("Average Resolution Time by Agent (hours)"); plt.xlabel(""); plt.xticks(rotation=45)
plt.tight_layout(); plt.savefig("images/05_agent_performance.png", dpi=150); plt.close()

plt.figure(figsize=(7, 4.5))
sns.heatmap(df.pivot_table(index="weekday", columns="category", values="ticket_id", aggfunc="count")
            .reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]),
            annot=True, fmt="d", cmap="Blues")
plt.title("Tickets: Weekday vs Category"); plt.xlabel(""); plt.ylabel("")
plt.tight_layout(); plt.savefig("images/06_weekday_heatmap.png", dpi=150); plt.close()
print("\nCharts saved in images/")
