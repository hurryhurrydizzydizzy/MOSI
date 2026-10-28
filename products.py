
# initial_stock — quantity available immediately after the starting restock.
# normal_demand — estimated daily demand range on normal days.
# busy_demand — estimated daily demand range on busy days.
# cost — purchasing cost per unit.
# price — selling price per unit.

PRODUCTS = {
    "Bottled Water": {
        "initial_stock": 120,
        "normal_demand": (8, 12),
        "busy_demand": (15, 20),
        "cost": 15,
        "price": 20,
    },
    "Soft Drinks": {
        "initial_stock": 144,
        "normal_demand": (8, 12),
        "busy_demand": (15, 20),
        "cost": 18,
        "price": 25,
    },
    "Pancit Canton": {
        "initial_stock": 120,
        "normal_demand": (12, 20),
        "busy_demand": (12, 20),
        "cost": 17,
        "price": 20,
    },
    "Magic Sarap": {
        "initial_stock": 100,
        "normal_demand": (10, 15),
        "busy_demand": (15, 25),
        "cost": 6,
        "price": 8,
    },
    "Candy": {
        "initial_stock": 300,
        "normal_demand": (25, 50),
        "busy_demand": (40, 70),
        "cost": 0.5,
        "price": 1,
    },
}
