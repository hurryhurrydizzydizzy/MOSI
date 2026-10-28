from products import PRODUCTS

# Strategy A: Original stock targets
SUNDAY_ONLY = {
    name: info["initial_stock"]
    for name, info in PRODUCTS.items()
}

# Strategy B: Preliminary risk-based targets
RISK_BASED = {
    "Bottled Water": 113,
    "Soft Drinks": 113,
    "Pancit Canton": 123,
    "Magic Sarap": 135,
    "Candy": 381
}

# Emergency trigger: 20% of the target
EMERGENCY_PERCENT = 0.20
