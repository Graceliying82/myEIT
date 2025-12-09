
import unittest
import numpy as np
from simulator import EITSimulator

class TestEITSimulator(unittest.TestCase):
    def setUp(self):
        print("Setting up EIT Simulator for testing...")
        self.sim = EITSimulator(n_el=16, n_nodes=512) # Use fewer nodes for faster testing

    def test_initialization(self):
        """ Test if simulator initializes mesh and forward solver """
        self.assertIsNotNone(self.sim.mesh_obj)
        self.assertIsNotNone(self.sim.fwd)
        self.assertIsNotNone(self.sim.v0)
        # Check baseline voltage
        self.assertTrue(len(self.sim.v0) > 0)

    def test_catheter_update(self):
        """ Test catheter movement and anomaly generation """
        # Move catheter to (0.1, 0.1)
        v, perm = self.sim.update_catheter(0.1, 0.1)
        
        # Check output shapes
        self.assertEqual(len(v), len(self.sim.v0))
        self.assertEqual(len(perm), len(self.sim.mesh_obj.element))
        
        # Check if conductivity changed (anomaly present)
        # Background is 1.0, Catheter is 2.0
        self.assertTrue(np.any(perm > 1.1), "Conductivity should be perturbed by catheter")
        
        # Check voltage difference
        diff_v = np.linalg.norm(v - self.sim.v0)
        print(f"Voltage difference magnitude: {diff_v}")
        self.assertTrue(diff_v > 1e-6, "Voltage should change when catheter is introduced")

if __name__ == '__main__':
    unittest.main()
