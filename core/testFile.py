import random as rd

mass = [rd.randint(0, 3) for i in range(1, 15)]
print(*mass)
# cc = mass.count(0)
# # if cc != 0:
# for i in range(cc):
#     mass.remove(0)
# mass = mass + [0] * cc

print(*sorted(mass, key=lambda x: x == 0))
