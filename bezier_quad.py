import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def lerp(t, A, B):
    return (1 - t) * A + t * B

# Control points
P0 = np.array([0.0, 0.0])
P1 = np.array([4.0, 4.0])
P2 = np.array([8.0, 0.0])
# P0 = np.array([0.0, 0.0])
# P1 = np.array([8.0, 2.0])
# P2 = np.array([0.0, 4.0])

fig, ax = plt.subplots(figsize=(7, 5))

ax.plot(
    [P0[0], P1[0], P2[0]],
    [P0[1], P1[1], P2[1]],
    'ro--',
    alpha=0.3,
    label='Control Polygon'
)

level1_line, = ax.plot([], [], 'g--', linewidth=1.5, alpha=0.8, label='Level 1 Lerp')
level1_points, = ax.plot([], [], 'go', markersize=5)

quad_trace_1, = ax.plot([], [], 'm-', linewidth=2, alpha=0.6, label='Quadratic Bézier')
quad_trace_2, = ax.plot([], [], 'm-', linewidth=2, alpha=0.6)

level2_line, = ax.plot([], [], 'm--', linewidth=2, alpha=0.8, label='Level 2 Lerp')
level2_points, = ax.plot([], [], 'mo', markersize=6)

t_text = ax.text(0.05, 0.92, '', transform=ax.transAxes)

ax.text(P0[0] - 0.2, P0[1] - 0.3, 'P0')
ax.text(P1[0] - 0.2, P1[1] + 0.2, 'P1')
ax.text(P2[0] + 0.1, P2[1] + 0.2, 'P2')

ax.set_title("Quadratic Bézier Construction")
ax.set_xlim(-1, 9)
ax.set_ylim(-1, 5)
ax.grid(True)

q1_x, q1_y = [], []
q2_x, q2_y = [], []

total_frames = 140

def update(frame):
    global q1_x, q1_y, q2_x, q2_y

    # Draw the two quadratic Bézier curves
    if frame <= 100:
        t = frame / 100

        L1 = lerp(t, P0, P1)
        L2 = lerp(t, P1, P2)

        Q1 = lerp(t, L1, L2)

        q1_x.append(Q1[0])
        q1_y.append(Q1[1])

        quad_trace_1.set_data(q1_x, q1_y)

        level1_line.set_data(
            [L1[0], L2[0]],
            [L1[1], L2[1]]
        )
        level1_points.set_data(
            [L1[0], L2[0]],
            [L1[1], L2[1]]
        )

        level2_line.set_data([Q1[0]], [Q1[1]])
        level2_points.set_data([Q1[0]], [Q1[1]])

    # Pause for a while
    else:
        t = 1.0

        L1 = lerp(t, P0, P1)
        L2 = lerp(t, P1, P2)

        Q1 = lerp(t, L1, L2)

        quad_trace_1.set_data(q1_x, q1_y)

        level1_line.set_data(
            [L1[0], L2[0]],
            [L1[1], L2[1]]
        )
        level1_points.set_data(
            [L1[0], L2[0]],
            [L1[1], L2[1]]
        )

    return (
        level1_line,
        level1_points,
        quad_trace_1,
        quad_trace_2,
        level2_line,
        level2_points,
        t_text
    )

ani = FuncAnimation(
    fig,
    update,
    frames=total_frames,
    interval=40,
    blit=True,
    repeat=False
)

ani.save("quad_bezier.gif", writer="pillow", fps=25)
