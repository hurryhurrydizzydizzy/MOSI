import random
from products import PRODUCTS
from strategies import SUNDAY_ONLY, EMERGENCY_PERCENT

DAYS = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]


def generate_week():
    # Choose either 4 or 5 busy days
    number_of_busy_days = random.choice([4, 5])

    # Randomly select which days are busy
    busy_days = random.sample(DAYS, number_of_busy_days)

    weekly_data = []

    for day in DAYS:
        is_busy = day in busy_days

        daily_data = {
            "day": day,
            "type": "Busy" if is_busy else "Normal"
        }

        # Generate demand for every product
        for product, info in PRODUCTS.items():
            if is_busy:
                minimum, maximum = info["busy_demand"]
            else:
                minimum, maximum = info["normal_demand"]

            daily_data[product] = random.randint(
                minimum, maximum
            )

        weekly_data.append(daily_data)

    return weekly_data

def simulate_week(week=None):
    # Generate demand if none was provided
    if week is None:
        week = generate_week()

    # Copy initial stocks for all five products
    inventory = {
        name: info["initial_stock"]
        for name, info in PRODUCTS.items()
    }

    # Track weekly totals for each product
    summary = {}

    for name in PRODUCTS:
        summary[name] = {
            "demand": 0,
            "sold": 0,
            "unfulfilled": 0,
            "stockout_days": 0,
            "ending_stock": 0,
            "gross_profit": 0
        }

    daily_results = []

    # Process each day in order
    for day in week:
        daily_record = {
            "day": day["day"],
            "type": day["type"],
            "products": {}
        }

        for name, info in PRODUCTS.items():
            available = inventory[name]
            demand = day[name]

            sold = min(available, demand)
            unfulfilled = demand - sold
            remaining = available - sold

            # Save the updated inventory
            inventory[name] = remaining

            # Update weekly totals
            summary[name]["demand"] += demand
            summary[name]["sold"] += sold
            summary[name]["unfulfilled"] += unfulfilled
            summary[name]["gross_profit"] += (
                sold * (info["price"] - info["cost"])
            )

            if unfulfilled > 0:
                summary[name]["stockout_days"] += 1

            # Save daily results
            daily_record["products"][name] = {
                "starting_stock": available,
                "demand": demand,
                "sold": sold,
                "unfulfilled": unfulfilled,
                "remaining_stock": remaining
            }

        daily_results.append(daily_record)

    # Save ending inventory for all products
    for name in PRODUCTS:
        summary[name]["ending_stock"] = inventory[name]

    return daily_results, summary

def simulate_four_weeks(
    targets=None,
    emergency=False,
    weeks=None
):
    # Default to the original Sunday policy
    if targets is None:
        targets = SUNDAY_ONLY

    # Generate demand unless it was provided
    if weeks is None:
        weeks = [generate_week() for _ in range(4)]

    # Copy starting inventory
    inventory = {
        name: info["initial_stock"]
        for name, info in PRODUCTS.items()
    }

    daily_results = []
    summary = {}

    for name in PRODUCTS:
        summary[name] = {
            "demand": 0,
            "sold": 0,
            "unfulfilled": 0,
            "stockout_days": 0,
            "purchased": 0,
            "ending_stock": 0,
            "gross_profit": 0
        }

    sunday_trips = 0
    emergency_trips = 0

    for week_number, week in enumerate(weeks, start=1):
        for day in week:
            daily_record = {
                "week": week_number,
                "day": day["day"],
                "type": day["type"],
                "products": {}
            }

            # STEP 1: Process customer demand
            for name, info in PRODUCTS.items():
                available = inventory[name]
                demand = day[name]

                sold = min(available, demand)
                unfulfilled = demand - sold

                inventory[name] -= sold

                summary[name]["demand"] += demand
                summary[name]["sold"] += sold
                summary[name]["unfulfilled"] += unfulfilled

                summary[name]["gross_profit"] += (
                    sold * (info["price"] - info["cost"])
                )

                if unfulfilled > 0:
                    summary[name]["stockout_days"] += 1

                daily_record["products"][name] = {
                    "starting_stock": available,
                    "demand": demand,
                    "sold": sold,
                    "unfulfilled": unfulfilled,
                    "remaining_stock": inventory[name],
                    "restocked": 0
                }

            # STEP 2: Determine whether to restock
            is_sunday = day["day"] == "Sunday"
            is_emergency = False

            if emergency and not is_sunday:
                for name in PRODUCTS:
                    threshold = (
                        targets[name] * EMERGENCY_PERCENT
                    )

                    if inventory[name] <= threshold:
                        is_emergency = True
                        break

            # STEP 3: Replenish qualifying products
            if is_sunday or is_emergency:

                if is_sunday:
                    sunday_trips += 1
                    daily_record["trip"] = "Sunday"
                else:
                    emergency_trips += 1
                    daily_record["trip"] = "Emergency"

                for name in PRODUCTS:

                    # On Sunday, check every product.
                    # On emergency trips, only low-stock items.
                    should_buy = is_sunday or (
                        inventory[name]
                        <= targets[name] * EMERGENCY_PERCENT
                    )

                    quantity = 0

                    if should_buy:
                        quantity = max(
                            0,
                            targets[name] - inventory[name]
                        )

                    inventory[name] += quantity
                    summary[name]["purchased"] += quantity

                    daily_record["products"][name][
                        "restocked"
                    ] = quantity

                    daily_record["products"][name][
                        "remaining_stock"
                    ] = inventory[name]

            daily_results.append(daily_record)

    # STEP 4: Record final inventory
    for name in PRODUCTS:
        summary[name]["ending_stock"] = inventory[name]

    # Store trip counts without changing the return format
    if daily_results:
        daily_results[-1]["total_sunday_trips"] = sunday_trips
        daily_results[-1]["total_emergency_trips"] = emergency_trips

    return daily_results, summary

