
from MOSI.financial import (
    analyze_finances,
    choose_best_strategy
)

sample = {
    "Sunday Only": {
        "average_profit": 10000,
        "average_purchase_cost": 8000,
        "average_trips": 4,
        "weekly_risk": {
            "Water": 0.01,
            "Soft Drinks": 0.01,
            "Pancit": 0.10,
            "Magic Sarap": 0.20,
            "Candy": 0.15
        },
        "fulfillment": {}
    },

    "Risk-Based": {
        "average_profit": 10800,
        "average_purchase_cost": 8600,
        "average_trips": 4,
        "weekly_risk": {
            name: 0.02
            for name in [
                "Water", "Soft Drinks", "Pancit",
                "Magic Sarap", "Candy"
            ]
        },
        "fulfillment": {}
    },

    "Risk + Emergency": {
        "average_profit": 11000,
        "average_purchase_cost": 9500,
        "average_trips": 7,
        "weekly_risk": {
            name: 0.01
            for name in [
                "Water", "Soft Drinks", "Pancit",
                "Magic Sarap", "Candy"
            ]
        },
        "fulfillment": {}
    }
}

results = analyze_finances(
    sample,
    transport_share=0.5
)

# Test 1: Transportation calculation
assert results["Sunday Only"]["transport_cost"] == 400

# Test 2: Profit after transportation
assert results["Risk-Based"]["profit_after_transport"] == 10400

# Test 3: Stockout target counting
assert results["Sunday Only"]["products_passing"] == 2
assert results["Risk-Based"]["products_passing"] == 5

# Test 4: Strategy selection
best, qualified = choose_best_strategy(results)

assert qualified is True
assert best == "Risk-Based"

# Test 5: No transportation allocation
no_transport = analyze_finances(
    sample,
    transport_share=0
)

assert (
    no_transport["Sunday Only"]["profit_after_transport"]
    == 10000
)

print("All financial tests passed!")
