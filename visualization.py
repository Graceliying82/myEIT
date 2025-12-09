import numpy as np
from vispy import scene, app
from vispy.color import Colormap

class EITVisualizer:
    def __init__(self, mesh_nodes, mesh_elements):
        self.canvas = scene.SceneCanvas(keys='interactive', show=True, title="myEIT 3D Simulator", bgcolor='#333333')
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'
        self.view.camera.fov = 45
        self.view.camera.distance = 3.0
        
        # Store mesh data - ensure proper types upfront
        self.mesh_nodes = np.asarray(mesh_nodes, dtype=np.float32)
        self.mesh_elements = np.asarray(mesh_elements, dtype=np.uint32)
        
        # Prepare 3D Mesh Data (add Z=0 to 2D mesh nodes)
        self._setup_scene()
        
    def _setup_scene(self):
        n_2d = len(self.mesh_nodes)
        
        # Create 3D vertices from 2D mesh (add z=0)
        # Shape: (N, 3) with dtype float32
        self.vertices_3d = np.zeros((n_2d, 3), dtype=np.float32)
        self.vertices_3d[:, 0] = self.mesh_nodes[:, 0]
        self.vertices_3d[:, 1] = self.mesh_nodes[:, 1]
        self.vertices_3d[:, 2] = 0.0
        
        # Elements are triangles
        self.faces = self.mesh_elements
        
        # Create initial face colors (all blue) - RGB only, shape (N_faces, 3)
        n_faces = len(self.faces)
        initial_colors = np.full((n_faces, 3), [0.3, 0.5, 0.8], dtype=np.float32)
        
        # Create MeshVisual
        self.mesh_visual = scene.visuals.Mesh(
            vertices=self.vertices_3d,
            faces=self.faces,
            face_colors=initial_colors,
            shading=None,  # Disable shading to avoid normal computation issues
            parent=self.view.scene
        )
        
        # Add Catheter Marker (Sphere)
        self.catheter_marker = scene.visuals.Sphere(radius=0.08, color='red', parent=self.view.scene)
        self.catheter_marker.transform = scene.transforms.MatrixTransform()
        
        # Add coordinate axes for reference
        scene.visuals.XYZAxis(parent=self.view.scene)
        
        # Set camera range
        self.view.camera.set_range(x=(-1.5, 1.5), y=(-1.5, 1.5), z=(-0.5, 0.5))

    def update_plot(self, perm, catheter_pos):
        # Normalize perm to [0, 1] for colormap
        p_min, p_max = perm.min(), perm.max()
        if p_max - p_min < 1e-6:
            norm_perm = np.zeros(len(perm), dtype=np.float32)
        else:
            norm_perm = ((perm - p_min) / (p_max - p_min)).astype(np.float32)
        
        # Create colormap and get face colors
        cmap = Colormap(['#0066CC', '#00CCCC', '#FFCC00', '#FF3300'])
        face_colors_rgba = cmap.map(norm_perm)
        
        # Use only RGB (first 3 channels), ensure float32
        face_colors = np.ascontiguousarray(face_colors_rgba[:, :3], dtype=np.float32)
        
        # Update mesh with new colors
        self.mesh_visual.set_data(
            vertices=self.vertices_3d,
            faces=self.faces,
            face_colors=face_colors
        )
        
        # Update Catheter Marker position
        self.catheter_marker.transform.reset()
        self.catheter_marker.transform.translate((float(catheter_pos[0]), float(catheter_pos[1]), 0.1))
        
        # Force canvas update
        self.canvas.update()

    def run(self):
        app.run()

if __name__ == "__main__":
    # Test Visualizer with simple triangle
    nodes = np.array([[0, 0], [1, 0], [0.5, 1]], dtype=np.float32)
    elements = np.array([[0, 1, 2]], dtype=np.uint32)
    viz = EITVisualizer(nodes, elements)
    viz.run()
