import matplotlib.pyplot as plt

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

# Recursive Dyck path transformation
def phi(P):
    """
    Rekürsif olarak Dyck yoluna dönüştür.
    """
    if not P:  # Empty road
        return ["U", "D"]
    elif P[0] == "E2":
        return phi(P[1:])  # Horizontal steps are skipped Dyck way
    elif P[0] == "N":
        return ["U"] + phi(P[1:])
    elif P[0] == "S":
        return ["D"] + phi(P[1:])
    else:
        return phi(P[1:])  # Skip steps that are not valid

# Don't draw the Dyck way
def draw_dyck_path(path, ax=None):
    """
    Dyck yolunu kare gridde çiz.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
    
    x, y = 0, 0
    xs, ys = [x], [y]
    
    for step in path:
        if step == "U":  # Yukarı
            y += 1
        elif step == "D":  # Aşağı
            y -= 1
        x += 1
        xs.append(x)
        ys.append(y)
    
    ax.plot(xs, ys, color='blue', linewidth=2, marker='o')
    ax.set_title("Dyck Path")
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
    return ax

# Creating a more complicated brick path
def generate_complex_brick_path():
    """
    Belirli bir tuğla yolunu tanımla.
    """
    return ["E2", "N", "E2", "S", "E2", "N", "E1", "N", "E2", "E1", "N", "E1", "N", "E2", "S", "E2", "S", "E2", "S","E2","S"]

# Create complex brick path and Dyck path
complex_brick_path = generate_complex_brick_path()
dyck_path = phi(complex_brick_path)

# for chart area
fig, axes = plt.subplots(1, 2, figsize=(14, 7))

# Draw the brick path
draw_brick_path(complex_brick_path, rows=6, cols=10, ax=axes[0])

# draw the dyck path
draw_dyck_path(dyck_path, ax=axes[1])

plt.tight_layout()
plt.show()
