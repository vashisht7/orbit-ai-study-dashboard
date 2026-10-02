import math
scores = [0.0, math.log(3)]
values = [[2.0, 0.0], [0.0, 4.0]]
exp_scores = [math.exp(s) for s in scores]
weights = [s / sum(exp_scores) for s in exp_scores]
output = [sum(weights[i] * values[i][j] for i in range(2))
          for j in range(2)]
print(weights)  # [0.25, 0.75]
print(output)   # [0.5, 3.0]
