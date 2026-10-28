import math
from products import PRODUCTS
from simulation import simulate_four_weeks
from simulation import generate_week
from strategies import SUNDAY_ONLY, RISK_BASED


def confidence_interval(values):
    # Calculate a 95% confidence interval for the mean
    n = len(values)
    average = sum(values) / n

    if n < 2:
        return average, average

    variance = sum(
        (x - average) ** 2 for x in values
    ) / (n - 1)

    standard_error = math.sqrt(variance / n)
    margin = 1.96 * standard_error

    return average - margin, average + margin


def run_monte_carlo(trials=10000):
    # Store results from all trials
    results = {}

    for name in PRODUCTS:
        results[name] = {
            "stockout_count": 0,
            "weekly_stockout_count": 0,
            "weekly_observations": 0,
            "unfulfilled": [],
            "ending_stock": [],
            "purchased": [],
            "gross_profit": [],
            "total_demand": 0,
            "total_sold": 0
        }

    # Repeat the four-week simulation
    for trial in range(trials):
        daily, summary = simulate_four_weeks()

        for name in PRODUCTS:
            data = summary[name]
            result = results[name]

            # Did this product have a stockout
            # at least once during the 28 days?
            if data["stockout_days"] > 0:
                result["stockout_count"] += 1

            result["unfulfilled"].append(
                data["unfulfilled"]
            )
            result["ending_stock"].append(
                data["ending_stock"]
            )
            result["purchased"].append(
                data["purchased"]
            )
            result["gross_profit"].append(
                data["gross_profit"]
            )

            result["total_demand"] += data["demand"]
            result["total_sold"] += data["sold"]

            # Check stockouts in each of the four weeks
            for week_number in range(1, 5):
                had_stockout = False

                for day in daily:
                    if day["week"] == week_number:
                        if (
                            day["products"][name]["unfulfilled"]
                            > 0
                        ):
                            had_stockout = True
                            break

                result["weekly_observations"] += 1

                if had_stockout:
                    result["weekly_stockout_count"] += 1

    # Calculate final statistics
    statistics = {}

    for name, result in results.items():
        weekly_count = result["weekly_observations"]

        # Probability across four-week periods
        month_stockout_probability = (
            result["stockout_count"] / trials
        )

        # Probability across all simulated weeks
        week_stockout_probability = (
            result["weekly_stockout_count"] / weekly_count
        )

        # Demand fulfillment across all trials
        demand = result["total_demand"]
        sold = result["total_sold"]

        fulfillment_rate = sold / demand if demand else 1.0

        statistics[name] = {
            "monthly_stockout_probability":
                month_stockout_probability,
            "weekly_stockout_probability":
                week_stockout_probability,
            "fulfillment_rate":
                fulfillment_rate,
            "average_unfulfilled":
                sum(result["unfulfilled"]) / trials,
            "average_ending_stock":
                sum(result["ending_stock"]) / trials,
            "average_purchased":
                sum(result["purchased"]) / trials,
            "average_gross_profit":
                sum(result["gross_profit"]) / trials,
            "profit_ci":
                confidence_interval(
                    result["gross_profit"]
                ),
            "unfulfilled_ci":
                confidence_interval(
                    result["unfulfilled"]
                )
        }

    return statistics

def compare_strategies(trials=10000):
    strategies = {
        "Sunday Only": (SUNDAY_ONLY, False),
        "Risk-Based": (RISK_BASED, False),
        "Risk + Emergency": (RISK_BASED, True)
    }

    results = {}

    for strategy in strategies:
        results[strategy] = {
            "stockouts": {name: 0 for name in PRODUCTS},
            "unfulfilled": {name: 0 for name in PRODUCTS},
            "demand": {name: 0 for name in PRODUCTS},
            "sold": {name: 0 for name in PRODUCTS},
            "profit": 0,
            "purchased_cost": 0,
            "trips": 0
        }

    for trial in range(trials):

        # Generate the same demand for all strategies
        weeks = [generate_week() for _ in range(4)]

        for strategy, settings in strategies.items():
            targets, emergency = settings

            daily, summary = simulate_four_weeks(
                targets=targets,
                emergency=emergency,
                weeks=weeks
            )

            result = results[strategy]

            # Record weekly stockout occurrences
            for name, info in PRODUCTS.items():
                data = summary[name]

                result["unfulfilled"][name] += data["unfulfilled"]
                result["demand"][name] += data["demand"]
                result["sold"][name] += data["sold"]
                result["profit"] += data["gross_profit"]

                result["purchased_cost"] += (
                    data["purchased"] * info["cost"]
                )

                for week_number in range(1, 5):
                    had_stockout = any(
                        day["week"] == week_number
                        and day["products"][name]["unfulfilled"] > 0
                        for day in daily
                    )

                    if had_stockout:
                        result["stockouts"][name] += 1

            # Read trip counts from the last daily record
            last_day = daily[-1]

            result["trips"] += (
                last_day["total_sunday_trips"]
                + last_day["total_emergency_trips"]
            )

    # Convert totals into averages and probabilities
    comparison = {}

    for strategy, data in results.items():
        weekly_risk = {}
        fulfillment = {}

        for name in PRODUCTS:
            weekly_risk[name] = (
                data["stockouts"][name] / (trials * 4)
            )

            if data["demand"][name] > 0:
                fulfillment[name] = (
                    data["sold"][name] / data["demand"][name]
                )
            else:
                fulfillment[name] = 1.0

        comparison[strategy] = {
            "weekly_risk": weekly_risk,
            "fulfillment": fulfillment,
            "average_profit": data["profit"] / trials,
            "average_purchase_cost":
                data["purchased_cost"] / trials,
            "average_trips": data["trips"] / trials
        }

    return comparison
