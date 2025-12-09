
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
        
        # Initial Catheter Position
        self.cx, self.cy = 0.2, 0.2
        self.update_simulation()
        
        # Bind keys
        self.viz.canvas.events.key_press.connect(self.on_key_press)
        
        print("Simulator Ready. Controls: Arrow keys to move catheter. Esc to quit.")

    def on_key_press(self, event):
        step = 0.05
        if event.key == 'Left':
            self.cx -= step
        elif event.key == 'Right':
            self.cx += step
        elif event.key == 'Up':
            self.cy += step
        elif event.key == 'Down':
            self.cy -= step
        elif event.key == 'Escape':
            sys.exit(0)
            
        self.update_simulation()

    def update_simulation(self):
        # Run physics
        v, perm = self.sim.update_catheter(self.cx, self.cy)
        
        # Update visualization
        self.viz.update_plot(perm, [self.cx, self.cy])

if __name__ == '__main__':
    eit_app = MyEITApp()
    eit_app.viz.run()
