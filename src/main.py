import csv
from pathlib import Path

from src.charts import make_charts
from src.metrics import compute_metrics, product_breakdown
from src.summarize import numbers_are_grounded, summarize

ROOT = Path(__file__).resolve().parent.parent
THIS_WEEK = ROOT / "incoming" / "sales_this_week.csv"
LAST_WEEK = ROOT / "incoming" / "sales_last_week.csv"
OUTPUT_DIR = ROOT / "output"
CHART_DIR = OUTPUT_DIR / "charts"
REPORT = OUTPUT_DIR / "weekly_digest.md"


def load(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def product_table(products):
    lines = ["| Product | Revenue this week | Revenue last week | Change | Return rate |",
             "|---|---|---|---|---|"]
    for p in products:
        change = "n/a" if p["revenue_change_pct"] is None else f"{p['revenue_change_pct']:+.1f}%"
        lines.append(f"| {p['product']} | {p['revenue_now']:,.0f} | "
                     f"{p['revenue_before']:,.0f} | {change} | {p['return_rate_pct']:.1f}% |")
    return "\n".join(lines)


def main():
    this_week, last_week = load(THIS_WEEK), load(LAST_WEEK)

    data = {
        "totals": compute_metrics(this_week, last_week),
        "products": product_breakdown(this_week, last_week),
    }

    charts = make_charts(this_week, data["products"], CHART_DIR)
    summary = summarize(data)

    if numbers_are_grounded(summary, data):
        body = summary
    else:
        body = "_Summary withheld: it contained figures not found in the data. Review manually._"

    sections = ["# Weekly Ops Digest", "", body, "", "## Product breakdown", "",
                product_table(data["products"]), "", "## Charts", ""]
    for title, path in charts:
        sections += [f"### {title}", "", f"![{title}](charts/{path.name})", ""]

    OUTPUT_DIR.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(sections), encoding="utf-8")
    print(f"Digest and {len(charts)} charts written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()