
from MOSI.products import PRODUCTS
from MOSI.simulation import simulate_four_weeks


def test_four_weeks():
    daily, summary = simulate_four_weeks()

    # Test 1: Four weeks must have 28 days
    assert len(daily) == 28

    # Test 2: There must be 4 Sundays
    sundays = [
        day for day in daily
        if day["day"] == "Sunday"
    ]
    assert len(sundays) == 4

    # Test 3: All stock values must be non-negative
    for day in daily:
        for name, data in day["products"].items():
            assert data["remaining_stock"] >= 0
            assert data["sold"] >= 0
            assert data["unfulfilled"] >= 0

            # Every request is sold or unfulfilled
            assert (
                data["sold"] + data["unfulfilled"]
                == data["demand"]
            )

    # Test 4: Every Sunday reaches the stock target
    for sunday in sundays:
        for name, info in PRODUCTS.items():
            data = sunday["products"][name]

            assert "restocked" in data
            assert data["restocked"] >= 0
            assert (
                data["remaining_stock"]
                >= info["initial_stock"]
            )

    # Test 5: Inventory conservation
    for name, info in PRODUCTS.items():
        result = summary[name]

        assert (
            info["initial_stock"] + result["purchased"]
            == result["sold"] + result["ending_stock"]
        )

        assert (
            result["sold"] + result["unfulfilled"]
            == result["demand"]
        )

        assert 0 <= result["stockout_days"] <= 28

    print("All four-week inventory tests passed!")


for i in range(100):
    test_four_weeks()

print("Successfully tested 100 simulated periods.")
