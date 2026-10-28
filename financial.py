from MOSI.analysis import compare_strategies

TRANSPORT_PER_TRIP = 200
TARGET_RISK = 0.05


def analyze_finances(results, transport_share=0.5):
    financial_results = {}

    for strategy, data in results.items():

        # Average transportation expenses
        transport_cost = (
            data["average_trips"]
            * TRANSPORT_PER_TRIP
            * transport_share
        )

        # Gross profit minus allocated transport
        profit_after_transport = (
            data["average_profit"] - transport_cost
        )

        # Count products that meet the 95% target
        products_passing = sum(
            risk <= TARGET_RISK
            for risk in data["weekly_risk"].values()
        )

        financial_results[strategy] = {
            "gross_profit": data["average_profit"],
            "purchase_cost": data["average_purchase_cost"],
            "trips": data["average_trips"],
            "transport_cost": transport_cost,
            "profit_after_transport": profit_after_transport,
            "products_passing": products_passing,
            "all_targets_met": products_passing == 5,
            "weekly_risk": data["weekly_risk"],
            "fulfillment": data["fulfillment"]
        }

    return financial_results


def choose_best_strategy(results):
    # Prefer strategies meeting all five targets
    qualified = {
        name: data
        for name, data in results.items()
        if data["all_targets_met"]
    }

    if qualified:
        # Highest profit among qualified strategies
        best = max(
            qualified,
            key=lambda name: qualified[name][
                "profit_after_transport"
            ]
        )
        return best, True

    # Otherwise choose the strategy that meets
    # the most targets, then has the highest profit
    best = max(
        results,
        key=lambda name: (
            results[name]["products_passing"],
            results[name]["profit_after_transport"]
        )
    )

    return best, False
