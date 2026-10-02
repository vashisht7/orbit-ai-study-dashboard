small_cost, large_cost = 1.0, 5.0
fraction_large = 0.30
direct = ((1-fraction_large) * small_cost
          + fraction_large * large_cost)
fallback = small_cost + fraction_large * large_cost
print(direct, fallback)  # 2.2, 2.5
