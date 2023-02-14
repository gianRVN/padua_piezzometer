from typing import List, Dict, Callable
from constant import np, date, plt, color, MAX_STATION, timedelta, pd, math

# polynomial of degree n
def polynomial_of_degree_n(input: int, degree:int) -> List:
  f = []
  for i in range(degree):
    f.append(input ** i)
  return f

# lagrange
def lagrange(input: int, obs_data: Dict) -> float:
  yp = 0

  for i in sorted(obs_data):      
    p=1
    for j in sorted(obs_data):
      if i != j:
        p = p * (input - j)/(i - j) 

    yp += p * obs_data[i]
  return round(yp, 2)

