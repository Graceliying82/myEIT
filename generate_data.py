
import csv
import time
import numpy as np
from simulator import EITSimulator

def generate_synthetic_data(filename="eit_data.csv", steps=100):
    print(f"Generating synthetic data to {filename}...")
    
    sim = EITSimulator()
    
    # Define a trajectory (e.g., a spiral)
    # spiral parameters
    n_points = steps
    t = np.linspace(0, 4*np.pi, n_points)
    
    # x, y positions (spiral out)
    # Center is 0,0. Max radius 0.8
    r = np.linspace(0, 0.8, n_points)
    x_traj = r * np.cos(t)
    y_traj = r * np.sin(t)
    z_traj = np.linspace(-0.5, 0.5, n_points) # Moving up
    
    # Prepare CSV file
    # We will save: index, x, y, z, v0, v1, ... vN
    # We need to know N (number of measurements)
    # Run one update to get voltage size
    v_init, _ = sim.update_catheter(0, 0, 0)
    
    # EITForward.solve_eit returns complex data usually. 
    # For CSV we might want to save real or abs. 
    # For visualization/reconstruction mostly absolute change or real part is used.
    # Let's save the Real part for simplicity, or Magnitude. 
    # Let's check type. If complex, taking absolute value (magnitude) is standard for simple dynamic imaging.
    is_complex = np.iscomplexobj(v_init)
    
    header = ['index', 'x', 'y', 'z'] + [f'v_{i}' for i in range(len(v_init))]
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        for i in range(n_points):
            cx = x_traj[i]
            cy = y_traj[i]
            cz = z_traj[i]
            
            v, _ = sim.update_catheter(cx, cy, cz)
            
            # Process voltage
            if is_complex:
                v_data = np.abs(v) # Use magnitude
            else:
                v_data = v
                
            row = [i, cx, cy, cz] + list(v_data)
            writer.writerow(row)
            
            if i % 10 == 0:
                print(f"Processed step {i}/{n_points}")

    print(f"Data generation complete. Saved {n_points} frames to {filename}")

if __name__ == "__main__":
    generate_synthetic_data()
