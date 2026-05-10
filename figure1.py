import numpy as np
import matplotlib.pyplot as plt
from matplotlib.textpath import TextPath
from matplotlib.path import Path
from matplotlib.transforms import Affine2D

def lerp(t, A, B):
    return (1 - t) * A + t * B

def quad_bezier(t, P0, P1, P2):
    L1 = lerp(t, P0, P1)
    L2 = lerp(t, P1, P2)
    return lerp(t, L1, L2)

def cubic_bezier(t, P0, P1, P2, P3):
    L1 = lerp(t, P0, P1)
    L2 = lerp(t, P1, P2)
    L3 = lerp(t, P2, P3)

    Q1 = lerp(t, L1, L2)
    Q2 = lerp(t, L2, L3)

    return lerp(t, Q1, Q2)

text = "CS334"

text_path = TextPath(
    (0, 0),
    text,
    size=1.0
)

transform = Affine2D().scale(1.0).translate(0, 0)
text_path = transform.transform_path(text_path)

vertices = text_path.vertices
codes = text_path.codes

points = []
line_segments = []
bezier_segments = []

current_pos = None
start_pos = None
i = 0

while i < len(vertices):
    code = codes[i]
    v = vertices[i]

    if code == Path.MOVETO:
        current_pos = v
        start_pos = v
        points.append(v)
        i += 1

    elif code == Path.LINETO:
        line_segments.append((current_pos, v))
        bezier_segments.append(("line", current_pos, v))
        points.append(v)
        current_pos = v
        i += 1

    elif code == Path.CURVE3:
        P0 = current_pos
        P1 = vertices[i]
        P2 = vertices[i + 1]

        line_segments.append((P0, P1))
        line_segments.append((P1, P2))

        bezier_segments.append(("quad", P0, P1, P2))

        points.extend([P1, P2])
        current_pos = P2
        i += 2

    elif code == Path.CURVE4:
        P0 = current_pos
        P1 = vertices[i]
        P2 = vertices[i + 1]
        P3 = vertices[i + 2]

        line_segments.append((P0, P1))
        line_segments.append((P1, P2))
        line_segments.append((P2, P3))

        bezier_segments.append(("cubic", P0, P1, P2, P3))

        points.extend([P1, P2, P3])
        current_pos = P3
        i += 3

    elif code == Path.CLOSEPOLY:
        if start_pos is not None:
            line_segments.append((current_pos, start_pos))
            bezier_segments.append(("line", current_pos, start_pos))
        current_pos = start_pos
        i += 1

    else:
        i += 1

points = np.array(points)

fig, axes = plt.subplots(3, 1, figsize=(15, 4))

for ax in axes:
    ax.set_aspect("equal")
    ax.axis("off")

axes[0].scatter(points[:, 0], points[:, 1], s=8)

for A, B in line_segments:
    axes[1].plot([A[0], B[0]], [A[1], B[1]], linewidth=1)

axes[1].scatter(points[:, 0], points[:, 1], s=6)

t_vals = np.linspace(0, 1, 40)

for seg in bezier_segments:
    if seg[0] == "line":
        _, P0, P1 = seg
        curve = np.array([lerp(t, P0, P1) for t in t_vals])

    elif seg[0] == "quad":
        _, P0, P1, P2 = seg
        curve = np.array([quad_bezier(t, P0, P1, P2) for t in t_vals])

    elif seg[0] == "cubic":
        _, P0, P1, P2, P3 = seg
        curve = np.array([cubic_bezier(t, P0, P1, P2, P3) for t in t_vals])

    axes[2].plot(curve[:, 0], curve[:, 1], linewidth=1.5)

plt.tight_layout()
plt.savefig("figure1.png", dpi=300, bbox_inches="tight")
