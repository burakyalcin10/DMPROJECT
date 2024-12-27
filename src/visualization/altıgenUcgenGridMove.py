import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np

def draw_hexagonal_grid(rows, cols, paths=None, radius=1):
    """
    Draw a hexagonal grid and overlay paths if provided.
    Args:
    - rows: Number of rows in the grid.
    - cols: Number of columns in the grid.
    - paths: List of paths (each path is a list of coordinates).
    - radius: Radius of the hexagons.
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    hex_height = np.sqrt(3) * radius  # Height of a hexagon
    for row in range(rows):
        for col in range(cols):
            # Calculate hexagon center
            x = col * 1.5 * radius
            y = row * hex_height
            if col % 2 == 1:  # Offset for odd columns
                y += hex_height / 2
            # Draw hexagon
            hexagon = RegularPolygon((x, y), numVertices=6, radius=radius, edgecolor='black', facecolor='none')
            ax.add_patch(hexagon)
    
    # Overlay paths if provided
    if paths:
        for path in paths:
            xs, ys = zip(*path)
            ax.plot(xs, ys, color='blue', marker='o', linewidth=2)

    ax.set_xlim(-radius, cols * 1.5 * radius)
    ax.set_ylim(-radius, rows * hex_height)
    ax.set_aspect('equal')
    plt.xticks([])
    plt.yticks([])
    plt.title("Hexagonal Grid with Paths")
    plt.show()

def generate_hexagonal_paths(start, length, rows, cols):
    """
    Generate paths on a hexagonal grid.
    Args:
    - start: Starting point (x, y).
    - length: Total number of steps in the path.
    - rows: Number of rows in the grid.
    - cols: Number of columns in the grid.
    Returns:
    - List of paths.
    """
    moves = [
        (1, 0),   # Right
        (-1, 0),  # Left
        (1, -1),  # Right down
        (-1, -1), # Left down
        (1, 1),   # Right up
        (-1, 1)   # Left up
    ]
    paths = []

    def is_valid_move(current, move):
        """Check if the move is valid on the grid."""
        x, y = current
        dx, dy = move
        nx, ny = x + dx, y + dy
        
        # Check boundaries
        if nx < 0 or ny < 0 or nx >= cols or ny >= rows:
            return False
        
        return True

    def backtrack(path):
        """Recursive backtracking to generate paths."""
        if len(path) == length + 1:  # Path is complete
            paths.append(path[:])
            return
        
        for move in moves:
            if is_valid_move(path[-1], move):
                nx, ny = path[-1][0] + move[0], path[-1][1] + move[1]
                path.append((nx, ny))
                backtrack(path)
                path.pop()

    backtrack([start])
    return paths

# Parameters
rows, cols = 6, 6
start = (0, 0)  # Starting at the corner of the first hexagon
length = 4  # Path length

# Generate paths and draw
paths = generate_hexagonal_paths(start, length, rows, cols)
draw_hexagonal_grid(rows, cols, paths)
