import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from stl import mesh

def generate_terrain(size=(10, 10), base_height=0.2, peak_scale=0.8):
    peaks = np.random.rand(*size)
    return np.where(peaks < base_height, base_height, base_height + peaks * peak_scale)

data = generate_terrain()

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x, y = np.meshgrid(range(data.shape[1]), range(data.shape[0]))
ax.plot_surface(x, y, data, cmap='terrain')
plt.show()

def create_stl(vertices, grid_rows, grid_cols, filename):
    faces = []
    
    for i in range(grid_rows - 1):
        for j in range(grid_cols - 1):
            v1 = i * grid_cols + j
            v2 = (i + 1) * grid_cols + j
            v3 = i * grid_cols + (j + 1)
            v4 = (i + 1) * grid_cols + (j + 1)
            
            faces.append([v1, v2, v3])
            faces.append([v2, v4, v3])
    
    stl_mesh = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            stl_mesh.vectors[i][j] = vertices[face[j]]
    
    stl_mesh.save(filename)

# Подготовка вершин
x_flat = x.flatten()
y_flat = y.flatten()
z_flat = data.flatten()
vertices = np.vstack((x_flat, y_flat, z_flat)).T

# Экспорт (передаем реальные размеры сетки)
create_stl(vertices, data.shape[0], data.shape[1], 'models/terrain.stl')