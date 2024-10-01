import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

alpha = -1
beta = 1
t_values = np.linspace(alpha, beta, 100)

# Grid
a0_values = np.linspace(-1, 1, 50)
a1_values = np.linspace(-1, 1, 50)
a2_values = np.linspace(-1, 1, 50)
a0, a1, a2 = np.meshgrid(a0_values, a1_values, a2_values)

# Polynomial p(t) = a0 + a1 * t + a2 * t^2
def p(t, a0, a1, a2):
    return a0 + a1 * t + a2 * t**2

# |p(t)| <= 1 for all t in [alpha, beta]
feasible = np.ones(a0.shape, dtype=bool)

for t in t_values:
    feasible &= (np.abs(p(t, a0, a1, a2)) <= 1)

# Plot the feasible region
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot settings
ax.scatter(a0[feasible], a1[feasible], a2[feasible], c='blue', alpha=0.3)

ax.set_xlabel('$a_0$')
ax.set_ylabel('$a_1$')
ax.set_zlabel('$a_2$')
ax.set_title('Visualization of Set S for $k=2$')

plt.show()

# Now only visualize a_0 and a_2 in 2D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)

# Plot settings
ax.scatter(a0[feasible], a2[feasible], c='blue', alpha=0.3)

ax.set_xlabel('$a_0$')
ax.set_ylabel('$a_2$')
ax.set_title('Visualization of Set S for $k=2$')

plt.show()
