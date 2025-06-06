# 3D Snake Game

This repository contains a small example of a 3D snake game written in Python using `pygame` and `PyOpenGL`. The snake is controlled by a simple autoplayer that searches for the food.

## Requirements

* Python 3.12 or compatible
* `pygame`
* `PyOpenGL`

These dependencies can be installed using pip:

```bash
pip install pygame PyOpenGL PyOpenGL_accelerate
```

## Running the Game

Execute the following command from the repository root:

```bash
python snake3d.py
```

A window will open displaying the snake moving in a 3D grid. The game ends if the snake collides with itself or a wall. The autoplayer automatically steers the snake toward the food.
