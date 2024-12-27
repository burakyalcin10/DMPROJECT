import matplotlib.pyplot as plt
import numpy as np

# Hareket fonksiyonları
sqrt8 = np.sqrt(8)
def move_E(x, y):
    return x + 3, y

def move_N(x, y):
    return x + 1, y + sqrt8

def move_S(x, y):
    return x - 1, y - sqrt8

# Grid boyutu
steps = 10  # Paralel kenar kenar uzunluğu artırıldı

# Gridin çizimi
for i in range(steps + 1):
    # Paralel çizgiler (yukarı ve aşağı doğru)
    x_start, y_start = 0, i * sqrt8
    for j in range(steps + 1):
        x_end, y_end = move_E(x_start, y_start)
        plt.plot([x_start, x_end], [y_start, y_end], color="gray", linewidth=0.5)
        x_start, y_start = x_end, y_end

for i in range(steps + 1):
    # Diyagonal yukarı (N) ve aşağı (S) çizgiler
    x_start, y_start = i * 3, 0
    for j in range(steps + 1 - i):
        x_end, y_end = move_N(x_start, y_start)
        plt.plot([x_start, x_end], [y_start, y_end], color="gray", linewidth=0.5)
        x_start, y_start = x_end, y_end

path = [(0, 0)]
directions = ["E", "E", "N", "E", "N", "N", "E", "E", "S", "S", "E", "N","E"]

for direction in directions:
    x, y = path[-1]  # Mevcut yolun son noktasını başlangıç olarak al
    if direction == "E":
        path.append(move_E(x, y))
    elif direction == "N":
        path.append(move_N(x, y))
    elif direction == "S":
        path.append(move_S(x, y))

# Güncellenen yolun çizimi
path_x = [x for x, y in path]
path_y = [y for x, y in path]
plt.plot(path_x, path_y, color="blue", linewidth=2, marker="o")

# Grid ve gösterim ayarları
plt.gca().set_aspect("equal", adjustable="box")
plt.grid(False)
plt.show()
