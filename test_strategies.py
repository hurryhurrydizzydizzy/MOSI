
from MOSI.products import PRODUCTS
from MOSI.simulation import DAYS, simulate_four_weeks
from MOSI.strategies import SUNDAY_ONLY, RISK_BASED
from MOSI.analysis import compare_strategies


def test_strategies():
    # Create 4 weeks with zero demand
    weeks = []

    for i in range(4):
        week = []

        for day in DAYS:
            record = {"day": day, "type": "Normal"}

            for name in PRODUCTS:
                record[name] = 0

            week.append(record)

        weeks.append(week)

    # No demand should cause no sales or shortages
    daily, summary = simulate_four_weeks(
        targets=SUNDAY_ONLY,
        emergency=False,
        weeks=weeks
    )

    assert len(daily) == 28

    for name, info in PRODUCTS.items():
        assert summary[name]["sold"] == 0
        assert summary[name]["unfulfilled"] == 0
        assert summary[name]["ending_stock"] == info["initial_stock"]

    # Test inventory conservation under random demand
    for targets, emergency in [
        (SUNDAY_ONLY, False),
        (RISK_BASED, False),
        (RISK_BASED, True)
    ]:
        daily, summary = simulate_four_weeks(
            targets=targets,
            emergency=emergency
        )

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

            assert result["ending_stock"] >= 0

    # Test the comparison output
    results = compare_strategies(20)

    assert len(results) == 3

    for strategy, data in results.items():
        assert data["average_trips"] >= 4

        for name in PRODUCTS:
            assert 0 <= data["weekly_risk"][name] <= 1
            assert 0 <= data["fulfillment"][name] <= 1

    print("All strategy tests passed!")


test_strategies()
