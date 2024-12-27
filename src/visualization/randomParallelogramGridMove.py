import matplotlib.pyplot as plt
import numpy as np
import random

# Hareket fonksiyonları
sqrt8 = np.sqrt(8)
def move_E(x, y):
    return x + 3, y

def move_N(x, y):
    return x + 1, y + sqrt8

def move_S(x, y, visited_paths):
    next_x, next_y = x - 1, y - sqrt8
    
    # Y koordinatı 0'dan büyük mü?
    if next_y < 0:
        return x, y
    
    # Geri dönüş kontrolü için daha detaylı kontrol
    for existing_path in visited_paths:
        # Eğer bu yeni nokta daha önce gittiğimiz bir yolun üzerinde ise
        if (next_x, next_y) in existing_path:
            return x, y
    
    return next_x, next_y

# Grid boyutu
steps = 10

# Gridin çizimi
for i in range(steps + 1):
    x_start, y_start = 0, i * sqrt8
    for j in range(steps + 1):
        x_end, y_end = move_E(x_start, y_start)
        plt.plot([x_start, x_end], [y_start, y_end], color="gray", linewidth=0.5)
        x_start, y_start = x_end, y_end

for i in range(steps + 1):
    x_start, y_start = i * 3, 0
    for j in range(steps + 1 - i):
        x_end, y_end = move_N(x_start, y_start)
        plt.plot([x_start, x_end], [y_start, y_end], color="gray", linewidth=0.5)
        x_start, y_start = x_end, y_end

# Rastgele bir yol oluşturma
possible_directions = ["E", "N", "S"]
path_length = 15

# Rastgele bir yol oluşturma
path = [(0, 0)]  # Başlangıç noktası
visited_paths = [path.copy()]  # Ziyaret edilen yolları takip et
current_x, current_y = 0, 0

for _ in range(path_length):
    direction = random.choice(possible_directions)
    if direction == "E":
        current_x, current_y = move_E(current_x, current_y)
    elif direction == "N":
        current_x, current_y = move_N(current_x, current_y)
    elif direction == "S":
        current_x, current_y = move_S(current_x, current_y, visited_paths)
    
    path.append((current_x, current_y))
    visited_paths.append(path.copy())  # Her adımda güncel yolu kaydet

# Rastgele yolun çizimi
path_x = [x for x, y in path]
path_y = [y for x, y in path]
plt.plot(path_x, path_y, color="blue", linewidth=2, marker="o")

# Grid ve gösterim ayarları
plt.gca().set_aspect("equal", adjustable="box")
plt.grid(False)
plt.show()
