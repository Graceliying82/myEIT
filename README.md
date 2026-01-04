# myEIT 3D Simulator

A 3D Electrical Impedance Tomography (EIT) simulator for visualizing electric field interactions with a moving catheter.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- **Real-time EIT simulation** using pyEIT's FEM solver
- **Interactive 3D visualization** with vispy
- **3D Catheter Tracking** - Move up/down, twist, and tilt the catheter
- **Heart Shell** - Visualize the catheter inside a transparent heart organ (with impedance simulation)
- **Recording & Replay** - Record your sessions to CSV and replay them at original speed
- **Synthetic Database** - Generate standardized datasets for testing

## Installation

```bash
# Clone the repository
git clone https://github.com/Graceliying82/myEIT.git
cd myEIT

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Interactive Mode
```bash
source .venv/bin/activate
python3 main.py
```

### Recording a Session
Save your movements and voltage data to a CSV file:
```bash
python3 main.py --record my_session.csv
```

### Replaying a Session
Play back a recorded session or synthetic dataset:
```bash
python3 main.py --replay my_session.csv
```

### Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** | Move catheter in X/Y plane |
| **W / S** | Move catheter **Up / Down** (Z-axis) |
| **Q / E** | **Twist** catheter (Roll) |
| **A / D** | **Tilt** catheter (Pitch) |
| **Mouse Drag** | Rotate 3D View |
| **Scroll** | Zoom In/Out |
| **ESC** | Quit |

## Documentation

- [**pyEIT User Guide**](pyEIT_Guide.md) - Detailed guide on the underlying EIT library.
- [**Design Document**](DESIGN.md) - Technical architecture and physics model.

## Project Structure

```
myEIT/
├── main.py           # Entry point & App logic
├── simulator.py      # EIT physics engine (pyEIT)
├── visualization.py  # 3D rendering (vispy)
├── generate_data.py  # Synthetic data generator
├── pyEIT_Guide.md    # Library documentation
├── DESIGN.md         # Architecture docs
└── requirements.txt  # Dependencies
```

## Dependencies

- [pyEIT](https://github.com/eitcom/pyEIT) - EIT simulation toolkit
- [vispy](https://vispy.org/) - High-performance 3D visualization
- PyQt6 - GUI backend

## License

MIT License
