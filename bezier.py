import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def lerp(t, A, B):
    return (1 - t) * A + t * B

# Control points
P0 = np.array([0.0, 0.0])
P1 = np.array([2.0, 4.0])
P2 = np.array([6.0, 3.0])
P3 = np.array([8.0, 0.0])
# P0 = np.array([0.0, 0.0])
# P1 = np.array([2.0, 2.0])
# P2 = np.array([6.0, 0.0])
# P3 = np.array([8.0, 3.0])
# P0 = np.array([0.0, 1.0])
# P1 = np.array([8.0, 0.0])
# P2 = np.array([8.0, 4.0])
# P3 = np.array([0.0, 3.0])

fig, ax = plt.subplots(figsize=(7, 5))

ax.plot(
    [P0[0], P1[0], P2[0], P3[0]],
    [P0[1], P1[1], P2[1], P3[1]],
    'ro--',
    alpha=0.3,
    label='Control Polygon'
)

line1, = ax.plot([], [], 'g--', linewidth=1.5, alpha=0.8, label='Level 1 Lerp')
points1, = ax.plot([], [], 'go', markersize=5)

quad1, = ax.plot([], [], 'm-', linewidth=2, alpha=0.6, label='Quadratic Bézier')
quad2, = ax.plot([], [], 'm-', linewidth=2, alpha=0.6)

line2, = ax.plot([], [], 'm--', linewidth=2, alpha=0.8, label='Level 2 Lerp')
points2, = ax.plot([], [], 'mo', markersize=6)

cubic_bezier, = ax.plot([], [], 'b-', linewidth=2.5, alpha=0.8, label='Cubic Bézier')
curve_point, = ax.plot([], [], 'ko', markersize=9, label='Cubic Point')

text = ax.text(0.05, 0.92, '', transform=ax.transAxes)

ax.text(P0[0] - 0.2, P0[1] - 0.3, 'P0')
ax.text(P1[0] - 0.2, P1[1] + 0.2, 'P1')
ax.text(P2[0] + 0.1, P2[1] + 0.2, 'P2')
ax.text(P3[0] + 0.1, P3[1] - 0.3, 'P3')

ax.set_title("Cubic Bézier Construction (Nested Lerps)")
ax.set_xlim(-1, 9)
ax.set_ylim(-1, 5)
ax.grid(True)

q1_x, q1_y = [], []
q2_x, q2_y = [], []
cubic_x, cubic_y = [], []

total_frames = 260

def update(frame):
    global q1_x, q1_y, q2_x, q2_y, cubic_x, cubic_y

    # Stage 1: draw the two quadratic Bézier curves
    if frame <= 100:
        t = frame / 100

        # 1st level lerps
        L1 = lerp(t, P0, P1)
        L2 = lerp(t, P1, P2)
        L3 = lerp(t, P2, P3)

        # 2nd level lerps
        Q1 = lerp(t, L1, L2)
        Q2 = lerp(t, L2, L3)

        q1_x.append(Q1[0])
        q1_y.append(Q1[1])
        q2_x.append(Q2[0])
        q2_y.append(Q2[1])

        quad1.set_data(q1_x, q1_y)
        quad2.set_data(q2_x, q2_y)

        line1.set_data(
            [L1[0], L2[0], L3[0]],
            [L1[1], L2[1], L3[1]]
        )
        points1.set_data(
            [L1[0], L2[0], L3[0]],
            [L1[1], L2[1], L3[1]]
        )

        line2.set_data([Q1[0], Q2[0]], [Q1[1], Q2[1]])
        points2.set_data([Q1[0], Q2[0]], [Q1[1], Q2[1]])

        curve_point.set_data([], [])
        text.set_text(f'Stage 1: build quadratic curves, t = {t:.2f}')

    # Pause for a while
    elif frame <= 120:
        t = 1.0

        L1 = lerp(t, P0, P1)
        L2 = lerp(t, P1, P2)
        L3 = lerp(t, P2, P3)

        Q1 = lerp(t, L1, L2)
        Q2 = lerp(t, L2, L3)

        quad1.set_data(q1_x, q1_y)
        quad2.set_data(q2_x, q2_y)

        line1.set_data(
            [L1[0], L2[0], L3[0]],
            [L1[1], L2[1], L3[1]]
        )
        points1.set_data(
            [L1[0], L2[0], L3[0]],
            [L1[1], L2[1], L3[1]]
        )

        line2.set_data([Q1[0], Q2[0]], [Q1[1], Q2[1]])
        points2.set_data([Q1[0], Q2[0]], [Q1[1], Q2[1]])

        curve_point.set_data([], [])

        text.set_text("Stage 1: build quadratic curves, t = 1.00")

    # Stage 2: draw the cubic Bézier curve
    elif frame <= 220:
        t = (frame - 120) / 100

        L1 = lerp(t, P0, P1)
        L2 = lerp(t, P1, P2)
        L3 = lerp(t, P2, P3)

        Q1 = lerp(t, L1, L2)
        Q2 = lerp(t, L2, L3)

        current_pt = lerp(t, Q1, Q2)

        cubic_x.append(current_pt[0])
        cubic_y.append(current_pt[1])

        cubic_bezier.set_data(cubic_x, cubic_y)

        # -------- Hide green level-1 visuals --------
        line1.set_data([], [])
        points1.set_data([], [])

        line2.set_data([Q1[0], Q2[0]], [Q1[1], Q2[1]])
        points2.set_data([Q1[0], Q2[0]], [Q1[1], Q2[1]])

        curve_point.set_data([current_pt[0]], [current_pt[1]])
        text.set_text(f'Stage 2: build cubic curve, t = {t:.2f}')

    # Pause for a while
    else:
        t = 1.0

        L1 = lerp(t, P0, P1)
        L2 = lerp(t, P1, P2)
        L3 = lerp(t, P2, P3)

        Q1 = lerp(t, L1, L2)
        Q2 = lerp(t, L2, L3)

        current_pt = lerp(t, Q1, Q2)

        cubic_bezier.set_data(cubic_x, cubic_y)

        line1.set_data([], [])
        points1.set_data([], [])

        line2.set_data(
            [Q1[0], Q2[0]],
            [Q1[1], Q2[1]]
        )
        points2.set_data(
            [Q1[0], Q2[0]],
            [Q1[1], Q2[1]]
        )

        # keep final black point
        curve_point.set_data(
            [current_pt[0]],
            [current_pt[1]]
        )

        text.set_text("Stage 2: build cubic curve, t = 1.00")

    return (
        line1,
        points1,
        quad1,
        quad2,
        line2,
        points2,
        cubic_bezier,
        curve_point,
        text
    )

ani = FuncAnimation(
    fig,
    update,
    frames=total_frames,
    interval=40,
    blit=True,
    repeat=False
)

ani.save("cubic_bezier_nested.gif", writer="pillow", fps=25)
