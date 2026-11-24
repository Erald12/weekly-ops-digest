from collections import defaultdict


def _totals(rows):
    return {
        "revenue": sum(float(r["revenue"]) for r in rows),
        "units": sum(int(r["units"]) for r in rows),
        "returns": sum(int(r["returns"]) for r in rows),
    }


def compute_metrics(this_week, last_week):
    now, before = _totals(this_week), _totals(last_week)

    by_product = defaultdict(float)
    for r in this_week:
        by_product[r["product"]] += float(r["revenue"])
    top_product = max(by_product, key=by_product.get)

    change = None
    if before["revenue"]:
        change = round((now["revenue"] - before["revenue"]) / before["revenue"] * 100, 1)

    return {
        "revenue": now["revenue"],
        "units": now["units"],
        "returns": now["returns"],
        "revenue_change_pct": change,
        "top_product": top_product,
        "top_product_revenue": by_product[top_product],
    }

def product_breakdown(this_week, last_week):
    def aggregate(rows):
        totals = defaultdict(lambda: {"revenue": 0.0, "units": 0, "returns": 0})
        for r in rows:
            t = totals[r["product"]]
            t["revenue"] += float(r["revenue"])
            t["units"] += int(r["units"])
            t["returns"] += int(r["returns"])
        return totals

    now, before = aggregate(this_week), aggregate(last_week)
    names = sorted(set(now) | set(before), key=lambda p: now[p]["revenue"], reverse=True)

    result = []
    for name in names:
        n, b = now[name], before[name]
        change = None
        if b["revenue"]:
            change = round((n["revenue"] - b["revenue"]) / b["revenue"] * 100, 1)
        return_rate = round(n["returns"] / n["units"] * 100, 1) if n["units"] else 0.0
        result.append({
            "product": name,
            "revenue_now": n["revenue"],
            "revenue_before": b["revenue"],
            "revenue_change_pct": change,
            "returns_now": n["returns"],
            "return_rate_pct": return_rate,
        })
    return result