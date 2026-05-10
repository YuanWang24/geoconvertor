import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Control points
P0 = np.array([0.0, 0.0])
P1 = np.array([2.0, 4.0])
P2 = np.array([6.0, 3.0])
P3 = np.array([8.0, 0.0])

fig, ax = plt.subplots(figsize=(7, 5))

ax.plot(
    [P0[0], P1[0], P2[0], P3[0]],
    [P0[1], P1[1], P2[1], P3[1]],
    'ro',
    alpha=0.8,
)

ax.set_title("Points")
ax.set_xlim(-1, 9)
ax.set_ylim(-1, 5)
ax.grid(True)
ax.legend()

plt.show()
