
from analysis import compare_strategies
from financial import (
    analyze_finances,
    choose_best_strategy
)

print("SARI-SARI STORE MONTE CARLO SIMULATOR")
print("STEP 7 - FINANCIAL COMPARISON")
print("=" * 60)

# STEP 1: Run the Monte Carlo experiment
simulation_results = compare_strategies(10000)

# STEP 2: Calculate financial performance
results = analyze_finances(
    simulation_results,
    transport_share=0.5
)

# STEP 3: Display each strategy's results
for strategy, data in results.items():
    print(f"\nSTRATEGY: {strategy}")
    print("-" * 50)

    print(
        f"Gross Profit:        "
        f"PHP {data['gross_profit']:,.2f}"
    )

    print(
        f"Purchasing Cost:     "
        f"PHP {data['purchase_cost']:,.2f}"
    )

    print(
        f"Average Trips:       "
        f"{data['trips']:.2f}"
    )

    print(
        f"Transport Expense:   "
        f"PHP {data['transport_cost']:,.2f}"
    )

    print(
        f"Profit After Travel: "
        f"PHP {data['profit_after_transport']:,.2f}"
    )

    print(
        f"Products Meeting 95% Target: "
        f"{data['products_passing']}/5"
    )

    for product, risk in data["weekly_risk"].items():
        print(f"  {product}: {risk:.2%} stockout risk")

# STEP 4: Select the best strategy
best, qualified = choose_best_strategy(results)

print("\n" + "=" * 60)

if qualified:
    print("BEST STRATEGY MEETING ALL TARGETS:")
else:
    print("BEST AVAILABLE COMPROMISE:")
    print("(No strategy meets all five targets)")

print(best)

print(
    "Expected Profit After Travel: PHP "
    f"{results[best]['profit_after_transport']:,.2f}"
)


print("\nTRANSPORTATION COST SENSITIVITY")
print("=" * 60)

for share in [0, 0.5, 1.0]:
    financial = analyze_finances(
        simulation_results,
        transport_share=share
    )

    best, qualified = choose_best_strategy(financial)

    print(f"\nTransport Allocation: {share:.0%}")
    print(f"Selected Strategy: {best}")
    print(
        f"Profit After Transport: PHP "
        f"{financial[best]['profit_after_transport']:,.2f}"
    )
