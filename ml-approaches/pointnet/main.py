import open3d as o3d
import numpy as np

mn40_airplane_0001 = "datasets/modelnet40/ModelNet40/airplane/train/airplane_0001.off"
toilet_0001 = "datasets/modelnet40/ModelNet40/toilet/train/toilet_0001.off"

def read_off(file_path):
    with open(file_path, 'r') as f:
        if 'OFF' != f.readline().strip():
            raise ValueError('Not a valid OFF header')
        n_verts, n_faces, n_edges = tuple(map(int, f.readline().strip().split(' ')))
        
        verts = []
        for i in range(n_verts):
            verts.append(list(map(float, f.readline().strip().split(' '))))

        faces = []
        for i in range(n_faces):
            faces.append(list(map(int, f.readline().strip().split(' ')))[1:])
        return np.array(verts)


points = read_off(mn40_airplane_0001)
point_cloud = o3d.geometry.PointCloud()
point_cloud.points = o3d.utility.Vector3dVector(points)

colors = np.tile([0, 0, 1], (points.shape[0], 1)).astype(np.float64)
point_cloud.colors = o3d.utility.Vector3dVector(colors)


# o3d.visualization.draw_geometries([point_cloud])


# Classes
import os
dataset_path = "datasets/modelnet40/ModelNet40"
folders = [dir for dir in sorted(os.listdir(dataset_path)) if os.path.isdir(dataset_path)]
classes = {folder: i for i, folder in enumerate(folders)};
print(classes)
# ***

def read_off(file):
    off_header = file.readline().strip()
    if 'OFF' == off_header:
        n_verts, n_faces, __ = tuple([int(s) for s in file.readline().strip().split(' ')])
    else:
        n_verts, n_faces, __ = tuple([int(s) for s in off_header[3:].split(' ')])

    print(n_verts)
    print(n_faces)
    verts = [[float(s) for s in file.readline().strip().split(' ')] for i_vert in range(n_verts)]
    faces = [[int(s) for s in file.readline().strip().split(' ')][1:] for i_face in range(n_faces)]
    return verts, faces


def visualize_rotate(data):
    x_eye, y_eye, z_eye = 1.25, 1.25, 0.8
    frames=[]

    def rotate_z(x, y, z, theta):
        w = x+1j*y
        return np.real(np.exp(1j*theta)*w), np.imag(np.exp(1j*theta)*w), z

    for t in np.arange(0, 10.26, 0.1):
        xe, ye, ze = rotate_z(x_eye, y_eye, z_eye, -t)
        frames.append(dict(layout=dict(scene=dict(camera=dict(eye=dict(x=xe, y=ye, z=ze))))))
    fig = go.Figure(data=data,
        layout=go.Layout(
            updatemenus=[dict(type='buttons',
                showactive=False,
                y=1,
                x=0.8,
                xanchor='left',
                yanchor='bottom',
                pad=dict(t=45, r=10),
                buttons=[dict(label='Play',
                    method='animate',
                    args=[None, dict(frame=dict(duration=50, redraw=True),
                        transition=dict(duration=0),
                        fromcurrent=True,
                        mode='immediate'
                        )]
                    )
                ])]
        ),
        frames=frames
    )

    return fig


def pcshow(xs,ys,zs):
    data=[go.Scatter3d(x=xs, y=ys, z=zs,
                                   mode='markers')]
    fig = visualize_rotate(data)
    fig.update_traces(marker=dict(size=2,
                      line=dict(width=2,
                      color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    fig.show()

with open(mn40_airplane_0001, 'r') as f:
    verts, faces = read_off(f)
    
i,j,k = np.array(faces).T
x,y,z = np.array(verts).T
import plotly.graph_objects as go

# visualize_rotate([go.Mesh3d(x=x, y=y, z=z, color='yellowgreen', opacity=0.50, i=i,j=j,k=k)]).show()
# visualize_rotate([go.Scatter3d(x=x, y=y, z=z, mode='markers')]).show()
pcshow(x,y,z)

