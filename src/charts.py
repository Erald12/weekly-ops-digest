from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def daily_revenue(rows):
    totals = defaultdict(float)
    for r in rows:
        totals[r["date"]] += float(r["revenue"])
    return dict(sorted(totals.items()))


def make_charts(this_week, breakdown, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    charts = []
    products = [p["product"] for p in breakdown]
    x = list(range(len(products)))
    width = 0.4

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar([i - width / 2 for i in x], [p["revenue_before"] for p in breakdown],
           width, label="Last week")
    ax.bar([i + width / 2 for i in x], [p["revenue_now"] for p in breakdown],
           width, label="This week")
    ax.set_xticks(x)
    ax.set_xticklabels(products, rotation=15, ha="right")
    ax.set_ylabel("Revenue")
    ax.set_title("Revenue by product")
    ax.legend()
    fig.tight_layout()
    path = out_dir / "revenue_by_product.png"
    fig.savefig(path, dpi=120)
    plt.close(fig)
    charts.append(("Revenue by product", path))

    daily = daily_revenue(this_week)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(list(daily.keys()), list(daily.values()), marker="o")
    ax.set_title("Daily revenue, this week")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    path = out_dir / "daily_revenue.png"
    fig.savefig(path, dpi=120)
    plt.close(fig)
    charts.append(("Daily revenue", path))

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(products, [p["returns_now"] for p in breakdown], color="tab:red")
    ax.set_title("Returns by product, this week")
    ax.set_ylabel("Units returned")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    path = out_dir / "returns_by_product.png"
    fig.savefig(path, dpi=120)
    plt.close(fig)
    charts.append(("Returns by product", path))

    return charts
