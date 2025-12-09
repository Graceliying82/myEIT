
import numpy as np
import pyeit.mesh as mesh
from pyeit.eit.fem import EITForward
from pyeit.eit.utils import eit_scan_lines
import pyeit.eit.protocol as protocol
from pyeit.mesh.wrapper import PyEITAnomaly_Circle

class EITSimulator:
    def __init__(self, n_el=16, n_nodes=1024):
        self.n_el = n_el
        self.n_nodes = n_nodes
        self.catheter_pos = [0.0, 0.0] # x, y (z ignored for 2D simplified core first)
        self.catheter_radius = 0.1
        self.conductivity_bg = 1.0
        self.conductivity_catheter = 2.0 # Higher conductivity for catheter tip or lower depending on material
        
        # Initialize Mesh
        # Note: pyEIT core is 2D. 3D support is experimental or via external meshes.
        # We will start with a high-fidelity 2D slice for physics and visualize it in 3D (extruded)
        # to ensure stability, as requested by the plan's fallback strategy.
        # Mesh setup
        # mesh.create returns a PyEITMesh object, not a tuple
        self.mesh_obj = mesh.create(n_el, h0=0.08)
        self.el_pos = self.mesh_obj.el_pos

        
        # Setup Protocol
        self.protocol_obj = protocol.create(n_el, dist_exc=1, step_meas=1, parser_meas="std")
        
        # Setup Forward Solver
        self.fwd = EITForward(self.mesh_obj, self.protocol_obj)
        
        # Baseline (Homogeneous)
        self.f0 = self.fwd.solve_eit(perm=self.conductivity_bg)
        # Handle different return types of solve_eit (object with .v or direct array)
        if hasattr(self.f0, 'v'):
            self.v0 = self.f0.v
        else:
            self.v0 = self.f0
        
    def update_catheter(self, x, y, z=0):
        """ Update catheter position and recalculate fields """
        self.catheter_pos = [x, y]
        
        # Generate anomaly
        anomaly = PyEITAnomaly_Circle(center=[x, y], r=self.catheter_radius, perm=self.conductivity_catheter)
        
        # Calculate new permittivity mapping on mesh
        # We start with background
        perm = np.full(self.mesh_obj.element.shape[0], self.conductivity_bg)
        
        # Apply anomaly
        # PyEIT mesh coordinates are in mesh_obj.node
        # Elements are defined by indices in mesh_obj.element
        # We need to find elements inside the anomaly
        
        pts = self.mesh_obj.node
        tri = self.mesh_obj.element
        
        # Calculate centroids of triangles to determine if they are inside the anomaly
        # shape (N_el, 3, 2) -> mean -> (N_el, 2)
        centroids = np.mean(pts[tri], axis=1)
        
        # Check distance
        dist = np.sqrt((centroids[:, 0] - x)**2 + (centroids[:, 1] - y)**2)
        mask = dist <= self.catheter_radius
        perm[mask] = self.conductivity_catheter
        
        self.current_perm = perm
        
        # Solve Forward
        # solve_eit returns a dictionary or similar structure in some versions, but error said ndarray
        # If it returns ndarray, that is the voltage.
        self.f1 = self.fwd.solve_eit(perm=perm)
        
        return self.f1.v if hasattr(self.f1, 'v') else self.f1, perm

    def get_mesh_data(self):
        return self.mesh_obj.node, self.mesh_obj.element

if __name__ == "__main__":
    sim = EITSimulator()
    v, perm = sim.update_catheter(0.2, 0.2)
    print(f"Simulation test: Voltage vector shape {v.shape}")
