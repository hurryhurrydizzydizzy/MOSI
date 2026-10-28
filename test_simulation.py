
from simulation import generate_week
from products import PRODUCTS


def test_week():
    week = generate_week()

    # Test 1: Exactly 7 days
    assert len(week) == 7

    # Test 2: Exactly 4 or 5 busy days
    busy_count = sum(
        day["type"] == "Busy" for day in week
    )
    assert busy_count in [4, 5]

    # Test 3: Demand stays within expected ranges
    for day in week:
        for product, info in PRODUCTS.items():
            if day["type"] == "Busy":
                minimum, maximum = info["busy_demand"]
            else:
                minimum, maximum = info["normal_demand"]

            demand = day[product]

            assert minimum <= demand <= maximum
            assert isinstance(demand, int)

    print("All tests passed!")


# Test n randomly generated weeks
n = 10000
for i in range(n):
    test_week()

print(f"Successfully tested {n} simulated weeks.")
