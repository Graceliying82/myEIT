
import sys
import numpy as np
from simulator import EITSimulator
from visualization import EITVisualizer
from vispy import app

class MyEITApp:
    def __init__(self):
        print("Initializing myEIT Simulator...")
        self.sim = EITSimulator()
        
        # Get initial mesh data for visualization
        nodes, elements = self.sim.get_mesh_data()
        
        self.viz = EITVisualizer(nodes, elements)
        
        # Initial Catheter Position (X, Y, Z)
        self.cx, self.cy, self.cz = 0.2, 0.2, 0.0
        # Catheter rotation angles (pitch, yaw, twist) in degrees
        self.rx, self.ry, self.rz = 0.0, 0.0, 0.0
        self.update_simulation()
        
        # Bind keys
        self.viz.canvas.events.key_press.connect(self.on_key_press)
        
        print("Simulator Ready. Controls:")
        print("  Arrow keys: Move catheter in X/Y plane")
        print("  W/S keys: Move catheter up/down (Z axis)")
        print("  Q/E keys: Twist catheter (roll)")
        print("  A/D keys: Tilt catheter (pitch)")
        print("  Esc: Quit")

    def on_key_press(self, event):
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
        elif event.key == 'Escape':
            sys.exit(0)
            
        self.update_simulation()

    def update_simulation(self):
        # Run physics
        v, perm = self.sim.update_catheter(self.cx, self.cy, self.cz)
        
        # Update visualization with 3D position and rotation
        self.viz.update_plot(perm, [self.cx, self.cy, self.cz], rotation=(self.rx, self.ry, self.rz))

if __name__ == '__main__':
    eit_app = MyEITApp()
    eit_app.viz.run()
