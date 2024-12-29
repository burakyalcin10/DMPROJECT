import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class Grid3DVisualizer:
    def __init__(self, size=10):
        self.size = size
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(15, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.setup_style()
        
    def setup_style(self):
        self.ax.set_facecolor('black')
        self.fig.patch.set_facecolor('black')
        self.ax.grid(True, linestyle='--', alpha=0.3)
        
        self.ax.xaxis._axinfo["grid"]['color'] = (1, 1, 1, 0.3)
        self.ax.yaxis._axinfo["grid"]['color'] = (1, 1, 1, 0.3)
        self.ax.zaxis._axinfo["grid"]['color'] = (1, 1, 1, 0.3)
        
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.tick_params(axis='z', colors='white')
            
    def plot_grid(self):
        for i in range(self.size + 1):
            self.ax.plot([0, self.size], [i, i], [0], 'w-', alpha=0.1)
            self.ax.plot([i, i], [0, self.size], [0], 'w-', alpha=0.1)
            
            self.ax.plot([0], [0, self.size], [i, i], 'w-', alpha=0.1)
            self.ax.plot([0], [i, i], [0, self.size], 'w-', alpha=0.1)
            
            self.ax.plot([0, self.size], [0], [i, i], 'w-', alpha=0.1)
            self.ax.plot([i, i], [0], [0, self.size], 'w-', alpha=0.1)
            
    def plot_planes(self):
       
        x = np.linspace(0, self.size, 50)
        y = np.linspace(0, self.size, 50)
        X, Y = np.meshgrid(x, y)
        
        Z = np.zeros_like(X)
        self.ax.plot_surface(X, Y, Z, alpha=0.2, color='blue', shade=True)
        
        self.ax.plot_surface(np.zeros_like(X), X, Y, alpha=0.2, color='red', shade=True)
        
        self.ax.plot_surface(X, np.zeros_like(X), Y, alpha=0.2, color='green', shade=True)
        
    def generate_path(self, steps=20):
        """
        3D yol oluşturur.
        Kurallar:
        1. Aynı nokta tekrar ziyaret edilemez
        2. Yol ızgara sınırları içinde kalmalı
        3. Her adımda sadece bir birim hareket edilebilir
        """
        path = [(0, 0, 0)]
        visited = {(0, 0, 0)}
        
        directions = [
            (1, 0, 0),   
            (0, 1, 0),   
            (0, 0, 1),   
        ]
        
        current = (0, 0, 0)
        for _ in range(steps):
            possible_moves = []
            
            for dx, dy, dz in directions:
                new_pos = (current[0] + dx, current[1] + dy, current[2] + dz)
                
                if (0 <= new_pos[0] <= self.size and 
                    0 <= new_pos[1] <= self.size and 
                    0 <= new_pos[2] <= self.size and 
                    new_pos not in visited):
                    possible_moves.append(new_pos)
            
            if not possible_moves:
                break
                
            current = possible_moves[np.random.randint(len(possible_moves))]
            path.append(current)
            visited.add(current)
        
        return np.array(path)
        
    def plot_path(self, path, animate=True):
        """Yolu çizer ve animasyon yapar"""
        if animate:
            line, = self.ax.plot([], [], [], 'w-', linewidth=2)
            scatter = self.ax.scatter([], [], [], c='yellow', s=100)
            
            def init():
                line.set_data([], [])
                line.set_3d_properties([])
                return line, scatter
            
            def animate(frame):
                line.set_data(path[:frame+1, 0], path[:frame+1, 1])
                line.set_3d_properties(path[:frame+1, 2])
                scatter._offsets3d = (path[frame:frame+1, 0], 
                                    path[frame:frame+1, 1],
                                    path[frame:frame+1, 2])
                return line, scatter
            
            anim = FuncAnimation(self.fig, animate, init_func=init,
                               frames=len(path), interval=200, 
                               blit=True, repeat=True)
            return anim
        else:
            self.ax.plot(path[:, 0], path[:, 1], path[:, 2], 
                        'w-', linewidth=2)
            
    def calculate_areas(self, path):
        """Yolun her düzlemdeki alanını hesaplar"""
        Axy = np.sum(np.abs(np.diff(path[:, [0, 1]], axis=0)))
        Ayz = np.sum(np.abs(np.diff(path[:, [1, 2]], axis=0)))
        Axz = np.sum(np.abs(np.diff(path[:, [0, 2]], axis=0)))
        return Axy, Ayz, Axz
        
    def plot_volume_distribution(self, areas):
        """Hacim dağılımını pasta grafiği olarak gösterir"""
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111)
        
        labels = ['XY Düzlemi', 'YZ Düzlemi', 'XZ Düzlemi']
        colors = ['blue', 'red', 'green']
        
        wedges, texts, autotexts = ax.pie(areas, labels=labels, colors=colors, 
                                         autopct='%1.1f%%', startangle=90)
        
        plt.setp(autotexts, size=8, weight="bold")
        plt.setp(texts, size=10)
        plt.title('Düzlem Alanları Dağılımı', color='white', pad=20)
        
    def add_title_and_labels(self):
        """Başlık ve etiketleri ekler"""
        self.ax.set_xlabel('X', color='white', labelpad=10)
        self.ax.set_ylabel('Y', color='white', labelpad=10)
        self.ax.set_zlabel('Z', color='white', labelpad=10)
        self.ax.set_title('3D Izgara Yolu Analizi', color='white', pad=20, size=16)
        
    def show(self):
        """Görselleştirmeyi gösterir"""
        plt.show()

def main():
    visualizer = Grid3DVisualizer(size=10)
    
    visualizer.plot_grid()
    visualizer.plot_planes()
    
    path = visualizer.generate_path(steps=30)
    
    anim = visualizer.plot_path(path, animate=True)
    
    areas = visualizer.calculate_areas(path)
    print("\nDüzlem Alanları:")
    print(f"XY Düzlemi: {areas[0]:.2f}")
    print(f"YZ Düzlemi: {areas[1]:.2f}")
    print(f"XZ Düzlemi: {areas[2]:.2f}")
    
    visualizer.add_title_and_labels()
    
    visualizer.plot_volume_distribution(areas)
    
    visualizer.show()

if __name__ == "__main__":
    main() 