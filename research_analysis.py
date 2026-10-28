import csv
import math
import os
import random
import statistics

from products import PRODUCTS
from simulation import generate_week, simulate_four_weeks
from strategies import SUNDAY_ONLY, RISK_BASED

TRIALS = 10000
SEED = 42
TRANSPORT_COST = 200
TRANSPORT_SHARE = 0.50

STRATEGIES = {
    "Sunday Only": (SUNDAY_ONLY, False),
    "Risk-Based": (RISK_BASED, False),
    "Risk + Emergency": (RISK_BASED, True)
}


def mean_ci(values):
    """95% confidence interval for a simulated mean."""
    average = statistics.mean(values)

    if len(values) < 2:
        return average, average, average

    error = (
        1.96 * statistics.stdev(values)
        / math.sqrt(len(values))
    )

    return average, average - error, average + error


def save_csv(filename, rows):
    """Save results in a CSV file."""
    if not rows:
        return

    os.makedirs("results", exist_ok=True)

    path = os.path.join("results", filename)

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys())
        )

        writer.writeheader()
        writer.writerows(rows)

    print("Saved:", path)


def run_research_analysis(trials=TRIALS):
    random.seed(SEED)

    # Independent trial results for each strategy
    records = {
        name: {
            "profit": [],
            "purchase_cost": [],
            "trips": [],
            "transport": [],
            "products": {
                product: {
                    "weekly_risk": [],
                    "unfulfilled": [],
                    "ending_stock": [],
                    "purchased": [],
                    "demand": 0,
                    "sold": 0
                }
                for product in PRODUCTS
            }
        }
        for name in STRATEGIES
    }

    for trial in range(trials):
        # Reuse demand for fair policy comparisons
        weeks = [generate_week() for _ in range(4)]

        for strategy, (targets, emergency) in STRATEGIES.items():
            daily, summary = simulate_four_weeks(
                targets=targets,
                emergency=emergency,
                weeks=weeks
            )

            record = records[strategy]

            gross_profit = sum(
                data["gross_profit"]
                for data in summary.values()
            )

            purchase_cost = sum(
                summary[name]["purchased"]
                * PRODUCTS[name]["cost"]
                for name in PRODUCTS
            )

            last_day = daily[-1]

            trips = (
                last_day["total_sunday_trips"]
                + last_day["total_emergency_trips"]
            )

            transport = (
                trips * TRANSPORT_COST * TRANSPORT_SHARE
            )

            record["profit"].append(
                gross_profit - transport
            )
            record["purchase_cost"].append(purchase_cost)
            record["trips"].append(trips)
            record["transport"].append(transport)

            for product in PRODUCTS:
                data = summary[product]
                item = record["products"][product]

                # Count stockout weeks inside this trial
                stockout_weeks = 0

                for week_number in range(1, 5):
                    had_stockout = any(
                        day["week"] == week_number
                        and day["products"][product][
                            "unfulfilled"
                        ] > 0
                        for day in daily
                    )

                    if had_stockout:
                        stockout_weeks += 1

                # Each trial produces a weekly risk fraction
                item["weekly_risk"].append(
                    stockout_weeks / 4
                )

                item["unfulfilled"].append(
                    data["unfulfilled"]
                )
                item["ending_stock"].append(
                    data["ending_stock"]
                )
                item["purchased"].append(
                    data["purchased"]
                )
                item["demand"] += data["demand"]
                item["sold"] += data["sold"]

    product_rows = []
    strategy_rows = []

    # Product-level statistics
    for strategy, record in records.items():
        passing = 0
        supported = 0

        for product, item in record["products"].items():
            risk, low, high = mean_ci(
                item["weekly_risk"]
            )

            # Bounds for a probability
            low = max(0, low)
            high = min(1, high)

            fulfillment = (
                item["sold"] / item["demand"]
                if item["demand"] else 1
            )

            meets_target = risk <= 0.05
            statistically_supported = high <= 0.05

            if meets_target:
                passing += 1

            if statistically_supported:
                supported += 1

            product_rows.append({
                "Strategy": strategy,
                "Product": product,
                "Weekly Risk (%)": round(risk * 100, 2),
                "95% CI Lower (%)": round(low * 100, 2),
                "95% CI Upper (%)": round(high * 100, 2),
                "Fulfillment (%)": round(
                    fulfillment * 100, 2
                ),
                "Avg Unfulfilled (4 weeks)": round(
                    statistics.mean(item["unfulfilled"]), 2
                ),
                "Avg Purchased (4 weeks)": round(
                    statistics.mean(item["purchased"]), 2
                ),
                "Avg Ending Stock": round(
                    statistics.mean(item["ending_stock"]), 2
                ),
                "Target Met": meets_target,
                "CI Supports Target": statistically_supported
            })

        # Strategy-level financial statistics
        profit, profit_low, profit_high = mean_ci(
            record["profit"]
        )

        strategy_rows.append({
            "Strategy": strategy,
            "Average Profit": round(profit, 2),
            "Profit CI Lower": round(profit_low, 2),
            "Profit CI Upper": round(profit_high, 2),
            "Average Purchase Cost": round(
                statistics.mean(record["purchase_cost"]), 2
            ),
            "Average Trips": round(
                statistics.mean(record["trips"]), 2
            ),
            "Average Transport": round(
                statistics.mean(record["transport"]), 2
            ),
            "Products Meeting Target": passing,
            "Targets Supported by CI": supported
        })

    save_csv("product_results.csv", product_rows)
    save_csv("strategy_results.csv", strategy_rows)

    return product_rows, strategy_rows


if __name__ == "__main__":
    products, strategies = run_research_analysis()

    print("\nPRODUCT RESULTS")
    for row in products:
        print(row)

    print("\nSTRATEGY RESULTS")
    for row in strategies:
        print(row)
