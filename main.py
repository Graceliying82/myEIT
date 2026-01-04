
import sys
import argparse
import csv
import numpy as np
from simulator import EITSimulator
from visualization import EITVisualizer
from vispy import app

class MyEITApp:
    def __init__(self, replay_file=None):
        print("Initializing myEIT Simulator...")
        self.sim = EITSimulator()
        
        # Get initial mesh data for visualization
        nodes, elements = self.sim.get_mesh_data()
        self.viz = EITVisualizer(nodes, elements)
        
        # Application State
        self.replay_mode = False
        self.replay_data = []
        self.replay_index = 0
        
        if replay_file:
            self.setup_replay(replay_file)
        else:
            self.setup_interactive()
            
    def setup_interactive(self):
        # Initial Catheter Position (X, Y, Z)
        self.cx, self.cy, self.cz = 0.2, 0.2, 0.0
        # Catheter rotation angles (pitch, yaw, twist) in degrees
        self.rx, self.ry, self.rz = 0.0, 0.0, 0.0
        
        self.update_simulation()
        
        # Bind keys
        self.viz.canvas.events.key_press.connect(self.on_key_press)
        
        print("Simulator Ready. MODE: INTERACTIVE")
        print("Controls:")
        print("  Arrow keys: Move catheter in X/Y plane")
        print("  W/S keys: Move catheter up/down (Z axis)")
        print("  Q/E keys: Twist catheter (roll)")
        print("  A/D keys: Tilt catheter (pitch)")
        print("  Esc: Quit")

    def setup_replay(self, filename):
        print(f"Loading replay data from {filename}...")
        self.replay_mode = True
        
        try:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                header = next(reader) # Skip header
                # Expected format: index, x, y, z, v...
                for row in reader:
                    if not row: continue
                    # Parse position (x, y, z) - columns 1, 2, 3
                    x, y, z = float(row[1]), float(row[2]), float(row[3])
                    self.replay_data.append((x, y, z))
        except Exception as e:
            print(f"Error loading file: {e}")
            sys.exit(1)
            
        print(f"Loaded {len(self.replay_data)} frames. MODE: REPLAY")
        print("Press Esc to Quit.")
        
        # Setup Animation Timer (20 FPS)
        self.timer = app.Timer(interval=0.05, connect=self.on_timer, start=True)

    def on_timer(self, event):
        if not self.replay_data: return
        
        # Get current frame data
        x, y, z = self.replay_data[self.replay_index]
        
        # Run physics update with recorded position
        # Note: In a real replay, we might assume 'perm' is reconstructed from voltages.
        # Here we simulate the effect by moving the catheter to the recorded position.
        v, perm = self.sim.update_catheter(x, y, z)
        
        # Update Visualization
        # Use 0 rotation for replay (or save rotation in CSV if needed later)
        self.viz.update_plot(perm, [x, y, z], rotation=(0, 0, 0))
        
        # Loop playback
        self.replay_index = (self.replay_index + 1) % len(self.replay_data)

    def on_key_press(self, event):
        # Global keys
        if event.key == 'Escape':
            sys.exit(0)
            
        if self.replay_mode:
            return # Ignore movement keys in replay mode

        step = 0.05
        rot_step = 10  # degrees
        if event.key == 'Left':
            self.cx -= step
        elif event.key == 'Right':
            self.cx += step
        elif event.key == 'Up':
            self.cy += step
        elif event.key == 'Down':
            self.cy -= step
        elif event.key == 'W' or event.key == 'w':
            self.cz += step  # Move up
        elif event.key == 'S' or event.key == 's':
            self.cz -= step  # Move down
        elif event.key == 'Q' or event.key == 'q':
            self.rz += rot_step  # Twist left
        elif event.key == 'E' or event.key == 'e':
            self.rz -= rot_step  # Twist right
        elif event.key == 'A' or event.key == 'a':
            self.rx += rot_step  # Tilt forward
        elif event.key == 'D' or event.key == 'd':
            self.rx -= rot_step  # Tilt backward
            
        self.update_simulation()
    
    def update_simulation(self):
        # Run physics
        v, perm = self.sim.update_catheter(self.cx, self.cy, self.cz)
        
        # Update visualization with 3D position and rotation
        self.viz.update_plot(perm, [self.cx, self.cy, self.cz], rotation=(self.rx, self.ry, self.rz))

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='myEIT 3D Simulator')
    parser.add_argument('--replay', type=str, help='Path to CSV file for data replay')
    args = parser.parse_args()

    # Start App
    eit_app = MyEITApp(replay_file=args.replay)
    eit_app.viz.run()
