import matplotlib.pyplot as plt

def draw_wall_tiling(rows, cols):
    """
    Draw a wall tiling where the leftmost edge has a dashed line without extra space.
    Args:
    - rows (int): Number of rows in the wall tiling.
    - cols (int): Number of columns in the wall tiling.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Loop through each row to draw bricks
    for i in range(rows):
        for j in range(cols):
            # Adjust x_start to ensure bricks alternate properly
            x_start = j * 2 if i % 2 == 0 else j * 2 + 1
            rect = plt.Rectangle((x_start, i), 2, 1, edgecolor='black', facecolor='none')
            ax.add_patch(rect)
            
            # Add dashed line on the very left of the grid
            if j == 0:  # For the first column, add a dashed line
                ax.plot(
                    [0, 0],  # x-coordinates for the dashed line
                    [0, rows],  # y-coordinates spanning the entire grid
                    linestyle='--', color='black'
                )

    # Set limits and aspect ratio
    ax.set_xlim(0, cols * 2)  # Remove extra space on the left
    ax.set_ylim(0, rows)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Wall Tiling N² ")
    plt.show()

# Draw the wall tiling without left gap
draw_wall_tiling(rows=6, cols=8)
