from MOSI.analysis import (
    confidence_interval,
    run_monte_carlo
)
from MOSI.products import PRODUCTS


def test_confidence_interval():
    # Identical results should have zero uncertainty
    lower, upper = confidence_interval([10, 10, 10])

    assert lower == 10
    assert upper == 10

    # The average must lie inside the interval
    lower, upper = confidence_interval([5, 10, 15])

    assert lower <= 10 <= upper


def test_monte_carlo():
    # Use 100 trials for quick testing
    results = run_monte_carlo(100)

    assert len(results) == 5

    for name in PRODUCTS:
        data = results[name]

        assert 0 <= data[
            "weekly_stockout_probability"
        ] <= 1

        assert 0 <= data[
            "monthly_stockout_probability"
        ] <= 1

        assert 0 <= data["fulfillment_rate"] <= 1

        assert data["average_unfulfilled"] >= 0
        assert data["average_ending_stock"] >= 0
        assert data["average_purchased"] >= 0

        # Any four-week stockout includes
        # at least one weekly stockout
        assert (
            data["monthly_stockout_probability"]
            >= data["weekly_stockout_probability"]
        )


test_confidence_interval()
test_monte_carlo()

print("All Monte Carlo tests passed!")
