# myEIT 3D Simulator

A 3D Electrical Impedance Tomography (EIT) simulator for visualizing electric field interactions with a moving catheter.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- **Real-time EIT simulation** using pyEIT's FEM solver
- **Interactive 3D visualization** with vispy
- **Dynamic catheter tracking** - move the catheter and see impedance changes
- **Configurable electric field** parameters

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/myEIT.git
cd myEIT

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
source .venv/bin/activate
python3 main.py
```

### Controls

| Key | Action |
|-----|--------|
| ↑ ↓ ← → | Move catheter |
| Mouse drag | Rotate view |
| Scroll | Zoom |
| ESC | Quit |

## Project Structure

```
myEIT/
├── main.py           # Entry point
├── simulator.py      # EIT physics engine (pyEIT)
├── visualization.py  # 3D rendering (vispy)
├── test_simulator.py # Unit tests
├── DESIGN.md         # Technical documentation
└── requirements.txt  # Dependencies
```

## Dependencies

- [pyEIT](https://github.com/eitcom/pyEIT) - EIT simulation toolkit
- [vispy](https://vispy.org/) - High-performance 3D visualization
- PyQt6 - GUI backend

## License

MIT License
