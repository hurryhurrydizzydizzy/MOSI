
from products import PRODUCTS
from simulation import DAYS, simulate_four_weeks
from strategies import SUNDAY_ONLY, RISK_BASED
from research_analysis import mean_ci


def zero_demand_weeks():
    weeks = []

    for _ in range(4):
        week = []

        for day in DAYS:
            record = {"day": day, "type": "Normal"}

            for product in PRODUCTS:
                record[product] = 0

            week.append(record)

        weeks.append(week)

    return weeks


def test_zero_demand():
    weeks = zero_demand_weeks()

    daily, summary = simulate_four_weeks(
        targets=SUNDAY_ONLY,
        emergency=False,
        weeks=weeks
    )

    assert len(daily) == 28

    for name, info in PRODUCTS.items():
        assert summary[name]["sold"] == 0
        assert summary[name]["unfulfilled"] == 0
        assert (
            summary[name]["ending_stock"]
            == info["initial_stock"]
        )


def test_inventory_balance():
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
            data = summary[name]

            assert (
                info["initial_stock"]
                + data["purchased"]
                == data["sold"] + data["ending_stock"]
            )

            assert (
                data["demand"]
                == data["sold"] + data["unfulfilled"]
            )

            assert data["ending_stock"] >= 0

        # Verify accounting for every individual day
        for day in daily:
            for name, data in day["products"].items():
                assert (
                    data["starting_stock"]
                    + data["restocked"]
                    == data["sold"]
                    + data["remaining_stock"]
                )


def test_common_demand():
    from simulation import generate_week

    weeks = [generate_week() for _ in range(4)]

    _, a = simulate_four_weeks(
        targets=SUNDAY_ONLY,
        weeks=weeks
    )

    _, b = simulate_four_weeks(
        targets=RISK_BASED,
        weeks=weeks
    )

    for name in PRODUCTS:
        assert a[name]["demand"] == b[name]["demand"]


def test_statistics():
    average, low, high = mean_ci([10, 10, 10])

    assert average == 10
    assert low == 10
    assert high == 10


test_zero_demand()

for _ in range(100):
    test_inventory_balance()
    test_common_demand()

test_statistics()

print("All research verification tests passed!")
