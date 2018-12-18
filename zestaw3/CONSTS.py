import math

TIME = 10000
SIMULATIONS = 1
STEP = 0.1
AVG_STEP = 10
COUNT = 10000
lam_1 = 1.0 / 20
lam_2 = 1.0 / 15


def rev_dyst(lam, y):
    return -1 * math.log(y) / lam
