
import pyeit.mesh as mesh
import pyeit.eit.ode as ode
import matplotlib.pyplot as plt
from pyeit.mesh.wrapper import PyEITAnomaly_Circle

def test_3d_generation():
    print("Testing 3D mesh generation...")
    # Generate a simple 3D mesh (cylinder) using PyEIT
    # Note: pyEIT's 3D support might be limited or require specific parameters. 
    # Let's try standard 2D first to ensure library works, then check 3D.
    
    # 2D Mesh
    mesh_obj, el_pos = mesh.create(16, h0=0.1)
    print(f"2D Mesh generated: {len(mesh_obj['node'])} nodes, {len(mesh_obj['element'])} elements.")
    
    # Check if we can do 3D
    # Inspecting mesh.create arguments or documentation via code if possible
    # For now, let's assume 3D requires specific function or external library hook.
    # Looking at my research, pyEIT supports 3D mesh generation.
    
    try:
        # Attempt minimal 3D generation if supported straightforwardly
        # Often libraries use a separate function or argument for 3D
        # If this fails, we will stick to verifying 2D is working and plan 3D carefully.
        print("Checking for 3D specific modules...")
        import pyeit.mesh.mesh_3d as mesh3d
        print("pyeit.mesh.mesh_3d found.")
    except ImportError:
        print("pyeit.mesh.mesh_3d NOT found. Might need to use external tools or different API.")

if __name__ == "__main__":
    test_3d_generation()
