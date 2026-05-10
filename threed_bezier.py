import numpy as np
import pyvista as pv
from math import comb

def bernstein(i, n, t):
    return comb(n, i) * (1 - t)**(n - i) * t**i

def bezier_patch(control_points, res_u=40, res_v=40):
    m = control_points.shape[0] - 1
    n = control_points.shape[1] - 1

    u_values = np.linspace(0, 1, res_u)
    v_values = np.linspace(0, 1, res_v)

    surface_points = np.zeros((res_u, res_v, 3))

    for ui, u in enumerate(u_values):
        for vi, v in enumerate(v_values):
            p = np.zeros(3)

            for i in range(m + 1):
                Bu = bernstein(i, m, u)
                for j in range(n + 1):
                    Bv = bernstein(j, n, v)
                    p += Bu * Bv * control_points[i, j]

            surface_points[ui, vi] = p

    return surface_points

def surface_points_to_mesh(surface_points):
    grid = pv.StructuredGrid()
    grid.points = surface_points.reshape(-1, 3)
    grid.dimensions = [
        surface_points.shape[0],
        surface_points.shape[1],
        1
    ]
    return grid.extract_surface().triangulate()

def normalize_to_sphere(points, radius=1.0):
    norm = np.linalg.norm(points, axis=-1, keepdims=True)
    return radius * points / norm

def make_cube_face_control_patch(face="z+", radius=1.0):
    vals = np.linspace(-1, 1, 4)
    control = np.zeros((4, 4, 3))

    for i, a in enumerate(vals):
        for j, b in enumerate(vals):

            if face == "z+":
                p = np.array([a, b, 1.0])
            elif face == "z-":
                p = np.array([a, b, -1.0])
            elif face == "x+":
                p = np.array([1.0, a, b])
            elif face == "x-":
                p = np.array([-1.0, a, b])
            elif face == "y+":
                p = np.array([a, 1.0, b])
            elif face == "y-":
                p = np.array([a, -1.0, b])

            control[i, j] = p

    control = normalize_to_sphere(control, radius=radius)
    return control

faces = ["x+", "x-", "y+", "y-", "z+", "z-"]

patch_meshes = []
control_patches = []

for face in faces:
    control = make_cube_face_control_patch(face, radius=1.0)
    control_patches.append(control)

    surface_points = bezier_patch(
        control,
        res_u=45,
        res_v=45
    )

    mesh = surface_points_to_mesh(surface_points)
    patch_meshes.append(mesh)

plotter = pv.Plotter()
plotter.set_background("black")

for mesh in patch_meshes:
    plotter.add_mesh(
        mesh,
        color="lightblue",
        opacity=0.85,
        show_edges=True,
        edge_color="black"
    )

for control in control_patches:
    control_points = control.reshape(-1, 3)
    control_cloud = pv.PolyData(control_points)

    lines = []
    rows, cols = control.shape[:2]

    # row lines
    for i in range(rows):
        for j in range(cols - 1):
            p0 = i * cols + j
            p1 = i * cols + j + 1
            lines.append([2, p0, p1])

    # column lines
    for j in range(cols):
        for i in range(rows - 1):
            p0 = i * cols + j
            p1 = (i + 1) * cols + j
            lines.append([2, p0, p1])

    control_net = pv.PolyData()
    control_net.points = control_points
    control_net.lines = np.hstack(lines)

    plotter.add_mesh(
        control_net,
        color="white",
        line_width=2
    )

    plotter.add_points(
        control_cloud,
        color="yellow",
        point_size=10,
        render_points_as_spheres=True
    )

plotter.show()
