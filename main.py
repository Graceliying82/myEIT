
import sys
import argparse
import csv
import numpy as np
from simulator import EITSimulator
from visualization import EITVisualizer
from vispy import app

class MyEITApp:
    def __init__(self, replay_file=None, record_file=None):
        print("Initializing myEIT Simulator...")
        self.sim = EITSimulator()
        
        # Get initial mesh data for visualization
        nodes, elements = self.sim.get_mesh_data()
        self.viz = EITVisualizer(nodes, elements)
        
        # Application State
        self.replay_mode = False
        self.replay_data = []
        self.replay_index = 0
        
        self.record_mode = False
        self.record_file = None
        self.record_writer = None
        self.record_frame_index = 0
        
        if replay_file:
            self.setup_replay(replay_file)
        elif record_file:
            self.setup_recording(record_file)
            self.setup_interactive() # Record mode is interactive + saving
        else:
            self.setup_interactive()
            
    def setup_recording(self, filename):
        print(f"Recording data to {filename}...")
        self.record_mode = True
        try:
            self.record_file = open(filename, 'w', newline='')
            self.record_writer = csv.writer(self.record_file)
            # Write Header (same format as generate_data.py)
            # Need to know voltage size. Get simulated voltage size first.
            v_init, _ = self.sim.update_catheter(0, 0, 0)
            header = ['index', 'x', 'y', 'z'] + [f'v_{i}' for i in range(len(v_init))]
            self.record_writer.writerow(header)
            
        except Exception as e:
            print(f"Error opening file for recording: {e}")
            sys.exit(1)
            
    def setup_interactive(self):
        # Initial Catheter Position (X, Y, Z)
        self.cx, self.cy, self.cz = 0.2, 0.2, 0.0
        # Catheter rotation angles (pitch, yaw, twist) in degrees
        self.rx, self.ry, self.rz = 0.0, 0.0, 0.0
        
        self.update_simulation()
        
        # Bind keys
        self.viz.canvas.events.key_press.connect(self.on_key_press)
        
        print("Simulator Ready. MODE: INTERACTIVE")
        if self.record_mode:
            print("  [RECORDING ACTIVE]")
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
        v, perm = self.sim.update_catheter(x, y, z)
        
        # Update Visualization
        self.viz.update_plot(perm, [x, y, z], rotation=(0, 0, 0))
        
        # Loop playback
        self.replay_index = (self.replay_index + 1) % len(self.replay_data)

    def on_key_press(self, event):
        # Global keys
        if event.key == 'Escape':
            if self.record_file:
                print("Closing recording file...")
                self.record_file.close()
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
        
        # Determine if voltages are complex and get magnitude if necessary
        is_complex = np.iscomplexobj(v)
        if is_complex:
            v_data = np.abs(v)
        else:
            v_data = v

        # If recording, save frame
        if self.record_mode and self.record_writer:
            row = [self.record_frame_index, self.cx, self.cy, self.cz] + list(v_data)
            self.record_writer.writerow(row)
            self.record_frame_index += 1
        
        # Update visualization with 3D position and rotation
        self.viz.update_plot(perm, [self.cx, self.cy, self.cz], rotation=(self.rx, self.ry, self.rz))

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='myEIT 3D Simulator')
    parser.add_argument('--replay', type=str, help='Path to CSV file for data replay')
    parser.add_argument('--record', type=str, help='Path to CSV file for data recording')
    args = parser.parse_args()

    # Start App
    eit_app = MyEITApp(replay_file=args.replay, record_file=args.record)
    eit_app.viz.run()
