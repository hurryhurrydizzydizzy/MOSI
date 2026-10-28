import os
from graphs import create_graphs


def test_graphs():
    create_graphs()

    files = [
        "stockout_probability.png",
        "demand_fulfillment.png",
        "profit_comparison.png",
        "purchasing_trips.png"
    ]

    for filename in files:
        path = os.path.join("graphs", filename)

        assert os.path.exists(path)
        assert os.path.getsize(path) > 0

    print("All graph tests passed!")


test_graphs()
