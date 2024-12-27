import matplotlib.pyplot as plt

# Recursive Motzkin path transformation
def psi(P):
    """
    Recursively return to the Motzkin road.
    """
    if not P:  # Empty road
        return ["H"]  # Horizontal step for space in Motzkin
    elif P[0] == "E2":
        return ["H"] + psi(P[1:])  # Horizontal step
    elif P[0] == "N":
        if len(P) > 1 and P[1] == "E1" and "S" in P[2:]:
            S_index = P[2:].index("S") + 2  # To find the correct index
            return ["U"] + psi(P[2:S_index]) + ["D"] + psi(P[S_index+1:])
        else:
            return ["U"] + psi(P[1:])
    elif P[0] == "S":
        return ["D"] + psi(P[1:])
    elif P[0] == "E1":
        return ["H"] + psi(P[1:])  # Include E1 as horizontal step
    else:
        return psi(P[1:])  # Skip unrecognized steps

# Drawing the Motzkin path with diagonal movements and fixed ending
def draw_motzkin_path_fixed(path, ax=None):
    """
    Motzkin yolunu kare gridde eğik adımlarla ve düzgün sona kesilerek çiz.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
    
    x, y = 0, 0
    xs, ys = [x], [y]
    
    for step in path:
        if step == "U":  # Ydiagonal right-up
            x += 1
            y += 1
        elif step == "D":  # diagonal right-down
            x += 1
            y -= 1
        elif step == "H":  # Yatay
            x += 1  # Each horizontal step goes exactly to the right
        xs.append(x)
        ys.append(y)
    
    # Keep the end point fixed for truncation
    xs[-1] = xs[-2]  # Equalise the last x coordinate with the previous one
    ys[-1] = 0       # Reduce the last y coordinate to zero
    
    ax.plot(xs, ys, color='green', linewidth=2, marker='o')
    ax.set_title("Motzkin Path (Fixed Ending)")
    ax.grid(True)
    
    # Add horizontal gridlines
    for i in range(-6, 7):
        ax.axhline(i, color='gray', linewidth=0.5, linestyle='--')
    
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
    return ax

# Function for drawing the brick pattern
def draw_wall_tiling(rows, cols, ax=None):
    """
    Create a grid to match the drawn brick pattern.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
    
    # Create the brick pattern like a pathwall.pdf
    for i in range(rows):
        for j in range(cols):
            # Adjusting the horizontal position of bricks (alternative alignment)
            x_start = j * 2 if i % 2 == 0 else j * 2 + 1
            rect = plt.Rectangle((x_start, i), 2, 1, edgecolor='black', facecolor='none')
            ax.add_patch(rect)

    # Axis limits and style
    ax.set_xlim(0, cols * 2)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    return ax

# Drawing the path in a brick pattern
def draw_brick_path(path, rows, cols, ax=None):
    """
    Çizilen tuğla deseninde verilen yolu göster.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
    
    draw_wall_tiling(rows, cols, ax=ax)
    
    x, y = 0, 0  # Starting point
    xs, ys = [x], [y]
    
    for step in path:
        if step == "N":  # Up
            y += 1
        elif step == "S":  # Down
            y -= 1
        elif step == "E1":  # 1 unit to the right
            x += 1
        elif step == "E2":  # 2 unit to the right
            x += 2
        xs.append(x)
        ys.append(y)
    
    ax.plot(xs, ys, color='orange', linewidth=2, marker='o')
    ax.set_title("Brick Pattern Path")
    return ax

# Define complex brick path
def generate_complex_brick_path():
    """
    Belirli bir tuğla yolunu tanımla.
    """
    return ["E2", "N", "E2", "S", "E2", "N", "E1", "N", "E2", "E1", "N", "E1", "N", "E2", "S", "E2", "S", "E2", "S", "E2", "S"]

# Generate a complex brick path
complex_brick_path = generate_complex_brick_path()

# Create Motzkin path from the complex brick path
motzkin_path = psi(complex_brick_path)

# Plot both the brick path and Motzkin path
fig, axes = plt.subplots(1, 2, figsize=(14, 7))
draw_brick_path(complex_brick_path, rows=6, cols=10, ax=axes[0])
draw_motzkin_path_fixed(motzkin_path, ax=axes[1])

plt.tight_layout()
plt.show()
