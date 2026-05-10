import numpy as np
import pyvista as pv

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

points = []

for face in faces:
    control_patch = make_cube_face_control_patch(face, radius=1.0)
    points.append(control_patch.reshape(-1, 3))

points = np.vstack(points)
points = np.unique(np.round(points, decimals=8), axis=0)
points = points / np.linalg.norm(points, axis=1, keepdims=True)

cloud = pv.PolyData(points)

volume = cloud.delaunay_3d(alpha=1.5)
surface = volume.extract_geometry()
surface = surface.triangulate()

plotter = pv.Plotter()

plotter.add_mesh(
    surface,
    color="lightblue",
    opacity=0.55,
    show_edges=True,
)

plotter.add_points(
    cloud,
    color="yellow",
    point_size=10,
    render_points_as_spheres=True,
    show_scalar_bar=False
)
plotter.background_color = pv.Color('black')

plotter.show()
