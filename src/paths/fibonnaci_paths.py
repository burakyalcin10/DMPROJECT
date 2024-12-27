import matplotlib.pyplot as plt
import random

def draw_custom_wall_tiling_with_path(rows, cols, path):
    """
    Draw a custom wall tiling with E1, E2 and visualize a path.
    Args:
    - rows (int): Number of rows in the grid.
    - cols (int): Number of columns in the grid.
    - path (list of tuples): The path to visualize.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Draw the custom wall tiling
    for i in range(rows):
        for j in range(cols):
            x_start = 2 * j if i % 2 == 0 else 2 * j + 1
            rect = plt.Rectangle((x_start, i), 2, 1, edgecolor='black', facecolor='none')
            ax.add_patch(rect)
    
    # Draw the path
    if path:
        x, y = zip(*path)
        ax.plot(x, y, color='red', linewidth=2, marker='o', label="Path")

    # Set limits and aspect ratio
    ax.set_xlim(-1, cols * 2 + 1)
    ax.set_ylim(-1, rows + 1)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Fibonacci Paths on Wall of $N^2$")
    ax.legend()
    plt.show()

def is_valid_move(x, y, direction, visited, rows, cols, last_move=None):
    """
    Check if a move in a given direction is valid.
    Args:
    - x, y (int): Current position.
    - direction (str): Direction of the move ('N', 'S', 'E1', 'E2').
    - visited (set): Set of visited points.
    - rows, cols (int): Grid dimensions.
    - last_move (str): The last move made (None if this is the first move).
    Returns:
    - bool: True if the move is valid, False otherwise.
    """
    directions = {'N': (0, 1), 'S': (0, -1), 'E1': (1, 0), 'E2': (2, 0)}
    dx, dy = directions[direction]
    new_x, new_y = x + dx, y + dy

    # Check grid boundaries
    if new_y < 0 or new_y >= rows or new_x < 0 or new_x >= cols * 2:
        return False
    
    # Check if the cell has already been visited
    if (new_x, new_y) in visited:
        return False
    
    # Fibonacci path rules:
    # 1. N can only come after E1 or E2
    if direction == 'N' and last_move not in ['E1', 'E2']:
        return False
        
    # 2. Cannot have N followed by S (YS sequence)
    if direction == 'S' and last_move == 'N':
        return False
    
    return True

def generate_validated_path(rows, cols):
    """
    Generate a path with validated movements for N, S, E1, E2.
    Args:
    - rows (int): Number of rows in the grid.
    - cols (int): Number of columns in the grid.
    Returns:
    - path (list of tuples): The generated path.
    - moves (list of str): The sequence of moves made.
    """
    length = random.randint(5, 15)  # Random length between 5 and 15
    path = [(0, 0)]  # Start from the bottom-left corner
    moves = []  # Track the sequence of moves
    directions = ['N', 'S', 'E1', 'E2']  # Possible directions
    visited = set(path)  # Track visited cells
    total_length = 1

    while total_length < length:
        x, y = path[-1]
        last_move = moves[-1] if moves else None

        # Determine valid moves from current position
        valid_moves = [direction for direction in directions 
                      if is_valid_move(x, y, direction, visited, rows, cols, last_move)]

        # If no valid moves are available, stop
        if not valid_moves:
            break

        # Choose a random valid move
        move = random.choice(valid_moves)
        dx, dy = {'N': (0, 1), 'S': (0, -1), 'E1': (1, 0), 'E2': (2, 0)}[move]
        new_point = (x + dx, y + dy)

        # Add the new point to the path
        path.append(new_point)
        moves.append(move)
        visited.add(new_point)
        total_length += 1

    return path, moves

# Example usage
rows = 6
cols = 8

# Generate the path with strict direction validation
validated_path, moves = generate_validated_path(rows, cols)

# Draw the grid with the generated path
draw_custom_wall_tiling_with_path(rows, cols, validated_path)
