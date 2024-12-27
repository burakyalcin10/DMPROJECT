import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull

def calculate_path_metrics(path_x, path_y, path_z):
    """Calculate various metrics for the path"""
    points = np.column_stack((path_x, path_y, path_z))
    
    # Path length (number of steps)
    path_length = len(path_x) - 1
    
    # Total distance traveled (in grid units)
    total_distance = path_length  # Since each step is 1 unit
    
    # Average segment length (always 1 in grid movement)
    avg_segment_length = 1.0
    
    # Calculate area under the path (using convex hull)
    try:
        hull = ConvexHull(points)
        volume = hull.volume
        area = hull.area
    except:
        volume = 0
        area = 0
    
    # Path complexity (changes in direction)
    direction_changes = 0
    if len(points) > 2:
        for i in range(1, len(points)-1):
            v1 = tuple(points[i] - points[i-1])
            v2 = tuple(points[i+1] - points[i])
            if v1 != v2:
                direction_changes += 1
    
    # Estimate reachable paths (more realistic than 6^n)
    # Using a simplified estimation based on grid size and path length
    grid_points = len(visited)  # Using the visited set from generate_3d_path
    reachable_paths = min(grid_points * 6, 6 ** path_length)
    
    return {
        'steps': path_length,
        'total_distance': total_distance,
        'avg_segment_length': avg_segment_length,
        'possible_paths': reachable_paths,
        'convex_hull_volume': volume,
        'surface_area': area,
        'direction_changes': direction_changes,
        'complexity_score': direction_changes / path_length if path_length > 0 else 0
    }

def generate_3d_path(grid_size=20, path_length=50):
    global visited  # Make visited accessible to calculate_path_metrics
    
    # Seed for randomness
    np.random.seed(None)  # Different random path in each run
    
    # Starting point 0,0,0
    path_x = [0]
    path_y = [0]
    path_z = [0]
    
    # Track visited points
    visited = set([(0,0,0)])
    
    for _ in range(path_length):
        # Calculate neighbor coordinates (direct neighbors only)
        candidates = [
            (path_x[-1]+1, path_y[-1], path_z[-1]),   # Right
            (path_x[-1]-1, path_y[-1], path_z[-1]),   # Left
            (path_x[-1], path_y[-1]+1, path_z[-1]),   # Up
            (path_x[-1], path_y[-1]-1, path_z[-1]),   # Down
            (path_x[-1], path_y[-1], path_z[-1]+1),   # Forward
            (path_x[-1], path_y[-1], path_z[-1]-1)    # Backward
        ]
        
        # Find points within grid boundaries and unvisited points
        valid_moves = [
            (x,y,z) for x,y,z in candidates 
            if (0 <= x < grid_size and 
                0 <= y < grid_size and 
                0 <= z < grid_size and 
                (x,y,z) not in visited)
        ]
        
        # If there is nowhere to move, stop
        if not valid_moves:
            break
        
        # Randomly select the next point
        next_x, next_y, next_z = valid_moves[np.random.randint(len(valid_moves))]
        
        # Add to path
        path_x.append(next_x)
        path_y.append(next_y)
        path_z.append(next_z)
        visited.add((next_x, next_y, next_z))
    
    # Calculate metrics
    metrics = calculate_path_metrics(path_x, path_y, path_z)
    
    # Create figure with a specific size
    fig = plt.figure(figsize=(15, 8))
    
    # Create grid layout
    gs = plt.GridSpec(1, 2, width_ratios=[2, 1], figure=fig)
    
    # 3D plot on the left
    ax = fig.add_subplot(gs[0], projection='3d')
    
    # Draw path
    ax.plot3D(path_x, path_y, path_z, color='black', marker='o', linewidth=2)
    
    # Start and end points
    ax.scatter(path_x[0], path_y[0], path_z[0], color='green', s=200, label='Start')
    ax.scatter(path_x[-1], path_y[-1], path_z[-1], color='red', s=200, label='End')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Grid Path')
    ax.legend()
    
    # Set the same scale for all axes
    max_range = max(max(path_x) - min(path_x),
                   max(path_y) - min(path_y),
                   max(path_z) - min(path_z))
    mid_x = (max(path_x) + min(path_x)) / 2
    mid_y = (max(path_y) + min(path_y)) / 2
    mid_z = (max(path_z) + min(path_z)) / 2
    ax.set_xlim(mid_x - max_range/2, mid_x + max_range/2)
    ax.set_ylim(mid_y - max_range/2, mid_y + max_range/2)
    ax.set_zlim(mid_z - max_range/2, mid_z + max_range/2)
    
    # Metrics text on the right
    ax_text = fig.add_subplot(gs[1])
    ax_text.axis('off')
    
    # Create metrics text with sections
    metrics_text = "PATH METRICS\n"
    metrics_text += "═" * 40 + "\n\n"
    
    metrics_text += "Basic Metrics:\n"
    metrics_text += "─" * 20 + "\n"
    metrics_text += f"• Steps: {metrics['steps']}\n"
    metrics_text += f"• Total Distance: {metrics['total_distance']} units\n"
    metrics_text += f"• Step Length: {metrics['avg_segment_length']:.2f} units\n\n"
    
    metrics_text += "Geometric Properties:\n"
    metrics_text += "─" * 20 + "\n"
    metrics_text += f"• Surface Area: {metrics['surface_area']:.2f}\n"
    metrics_text += f"• Volume: {metrics['convex_hull_volume']:.2f}\n\n"
    
    metrics_text += "Complexity Analysis:\n"
    metrics_text += "─" * 20 + "\n"
    metrics_text += f"• Direction Changes: {metrics['direction_changes']}\n"
    metrics_text += f"• Complexity Score: {metrics['complexity_score']:.2f}\n"
    metrics_text += f"• Possible Paths: {metrics['possible_paths']:,}\n"
    
    # Add text box with metrics
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
    ax_text.text(0.05, 0.95, metrics_text, transform=ax_text.transAxes,
                fontsize=10, verticalalignment='top', bbox=props,
                family='monospace')
    
    plt.tight_layout()
    plt.show()
    
    return metrics

if __name__ == "__main__":
    metrics = generate_3d_path()
    print("\nDetailed Path Analysis:")
    print(f"Number of steps: {metrics['steps']}")
    print(f"Total distance: {metrics['total_distance']} units")
    print(f"Length per step: {metrics['avg_segment_length']:.2f} units")
    print(f"Estimated reachable paths: {metrics['possible_paths']:,}")
    print(f"Surface area (convex hull): {metrics['surface_area']:.2f}")
    print(f"Volume (convex hull): {metrics['convex_hull_volume']:.2f}")
    print(f"Direction changes: {metrics['direction_changes']}")
    print(f"Path complexity score: {metrics['complexity_score']:.2f}")
