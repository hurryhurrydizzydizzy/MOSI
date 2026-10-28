import os
import matplotlib.pyplot as plt  # type: ignore[reportMissingModuleSource]

from products import PRODUCTS
from analysis import compare_strategies
from financial import analyze_finances


def create_graphs():
    print("Running Monte Carlo Simulation...")

    # Run the same experiment used in Step 7
    simulation_results = compare_strategies(10000)

    financial_results = analyze_finances(
        simulation_results,
        transport_share=0.5
    )

    # Create the output folder
    os.makedirs("graphs", exist_ok=True)

    strategies = list(financial_results.keys())
    products = list(PRODUCTS.keys())

    # GRAPH 1: Stockout probability
    fig, ax = plt.subplots(figsize=(12, 6))

    for strategy in strategies:
        risks = [
            financial_results[strategy]["weekly_risk"][p] * 100
            for p in products
        ]

        ax.plot(
            products,
            risks,
            marker="o",
            label=strategy
        )

    ax.axhline(
        5,
        linestyle="--",
        label="5% maximum stockout risk"
    )

    ax.set_title("Weekly Stockout Probability by Product")
    ax.set_xlabel("Product")
    ax.set_ylabel("Stockout Probability (%)")
    ax.set_ylim(bottom=0)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    fig.savefig(
        "graphs/stockout_probability.png",
        dpi=300
    )
    plt.close(fig)

    # GRAPH 2: Demand fulfillment
    fig, ax = plt.subplots(figsize=(12, 6))

    for strategy in strategies:
        fulfillment = [
            financial_results[strategy]["fulfillment"][p] * 100
            for p in products
        ]

        ax.plot(
            products,
            fulfillment,
            marker="o",
            label=strategy
        )

    ax.set_title("Demand Fulfillment Rate by Product")
    ax.set_xlabel("Product")
    ax.set_ylabel("Demand Fulfillment (%)")
    ax.set_ylim(0, 105)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    fig.savefig(
        "graphs/demand_fulfillment.png",
        dpi=300
    )
    plt.close(fig)

    # GRAPH 3: Profit comparison
    profits = [
        financial_results[s]["profit_after_transport"]
        for s in strategies
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(strategies, profits)

    for bar, value in zip(bars, profits):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"PHP {value:,.0f}",
            ha="center",
            va="bottom"
        )

    ax.set_title("Average Four-Week Profit After Transportation")
    ax.set_ylabel("Profit Contribution (PHP)")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    fig.savefig(
        "graphs/profit_comparison.png",
        dpi=300
    )
    plt.close(fig)

    # GRAPH 4: Purchasing trips
    trips = [
        financial_results[s]["trips"]
        for s in strategies
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(strategies, trips)

    for bar, value in zip(bars, trips):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.2f}",
            ha="center",
            va="bottom"
        )

    ax.set_title("Average Purchasing Trips Over Four Weeks")
    ax.set_ylabel("Number of Trips")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    fig.savefig(
        "graphs/purchasing_trips.png",
        dpi=300
    )
    plt.close(fig)

    print("\nAll four graphs have been saved!")
    return simulation_results, financial_results


if __name__ == "__main__":
    create_graphs()
