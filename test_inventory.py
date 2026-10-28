from products import PRODUCTS
from simulation import DAYS, simulate_week


def test_inventory():

    # Test 1: A week with zero customer demand
    week = []

    for day in DAYS:
        record = {"day": day, "type": "Normal"}

        for product in PRODUCTS:
            record[product] = 0

        week.append(record)

    daily, summary = simulate_week(week)

    assert len(daily) == 7

    for name, info in PRODUCTS.items():
        assert summary[name]["sold"] == 0
        assert summary[name]["unfulfilled"] == 0
        assert summary[name]["stockout_days"] == 0
        assert summary[name]["ending_stock"] == info["initial_stock"]

    # Test 2: Daily demand exceeds all starting stocks
    week = []

    for i, day in enumerate(DAYS):
        record = {"day": day, "type": "Busy"}

        for name, info in PRODUCTS.items():
            if i == 0:
                record[name] = info["initial_stock"] + 10
            else:
                record[name] = 0

        week.append(record)

    daily, summary = simulate_week(week)

    for name, info in PRODUCTS.items():
        assert summary[name]["sold"] == info["initial_stock"]
        assert summary[name]["unfulfilled"] == 10
        assert summary[name]["ending_stock"] == 0
        assert summary[name]["stockout_days"] == 1

    # Test 3: Inventory conservation
    for i in range(100):
        daily, summary = simulate_week()

        for name, info in PRODUCTS.items():
            data = summary[name]

            assert data["sold"] + data["unfulfilled"] == data["demand"]

            assert data["sold"] + data["ending_stock"] == info["initial_stock"]

            assert data["ending_stock"] >= 0
            assert 0 <= data["stockout_days"] <= 7

    print("All inventory tests passed!")


test_inventory()
