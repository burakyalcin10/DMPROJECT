import matplotlib.pyplot as plt
import numpy as np
import random

# Hareket fonksiyonları
sqrt3 = np.sqrt(3)
def move_E(x, y):
    return x + 1, y

def move_NE(x, y):
    return x + 0.5, y + sqrt3/2

def move_SW(x, y, visited_paths):
    next_x, next_y = x - 0.5, y - sqrt3/2
    
    # Sadece temel kontroller
    # 1. Y koordinatı negatif olmamalı
    if next_y < 0:
        return x, y
        
    # 2. Son noktaya geri dönmemeli
    if len(visited_paths[-1]) >= 2:
        last_point = visited_paths[-1][-2]  # Son noktadan bir önceki nokta
        if (next_x, next_y) == last_point:
            return x, y
    
    return next_x, next_y

def do_lines_intersect(p1, p2, p3, p4):
    # İki çizginin kesişip kesişmediğini kontrol eden yardımcı fonksiyon
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    # Çizgilerin kesişim kontrolü için determinant hesaplaması
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:  # Çizgiler paralel
        return False
        
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
    
    # Kesişim noktası çizgi parçaları üzerinde mi?
    return 0 <= t <= 1 and 0 <= u <= 1

# Grid boyutu
steps = 10

# Figür boyutunu ayarla
plt.figure(figsize=(8, 6))

# Gridin çizimi
for i in range(steps + 1):
    x_start, y_start = 0, i * sqrt3/2
    for j in range(steps + 1):
        x_end, y_end = move_E(x_start, y_start)
        plt.plot([x_start, x_end], [y_start, y_end], color="lightgray", linewidth=0.5)
        x_start, y_start = x_end, y_end

for i in range(steps + 1):
    x_start, y_start = i, 0
    for j in range(steps + 1 - i):
        x_end, y_end = move_NE(x_start, y_start)
        plt.plot([x_start, x_end], [y_start, y_end], color="lightgray", linewidth=0.5)
        x_start, y_start = x_end, y_end

# Rastgele bir yol oluşturma
possible_directions = ["E", "NE", "SW"]
path_length = 15

# Rastgele bir yol oluşturma
path = [(0, 0)]  # Başlangıç noktası
visited_paths = [path.copy()]  # Ziyaret edilen yolları takip et
current_x, current_y = 0, 0
selected_directions = []  # Seçilen yönleri sakla
last_direction = None  # Son hareket yönünü takip et

for step in range(path_length):
    # Mevcut duruma göre olası yönleri belirle
    available_directions = []
    
    # Her zaman E yönü mümkün
    available_directions.append("E")
    
    # NE yönü, son hareket SW değilse mümkün
    if last_direction != "SW":
        available_directions.append("NE")
    
    # SW yönü, son hareket NE değilse mümkün
    if last_direction != "NE":
        available_directions.append("SW")
    
    # Debug için yön seçimini göster
    print(f"Step {step}: Last direction: {last_direction}, Available directions: {available_directions}")
    
    # Rastgele yön seç
    direction = random.choice(available_directions)
    selected_directions.append(direction)
    print(f"Selected direction: {direction}")
    
    # Hareketi uygula
    if direction == "E":
        current_x, current_y = move_E(current_x, current_y)
        last_direction = "E"
    elif direction == "NE":
        current_x, current_y = move_NE(current_x, current_y)
        last_direction = "NE"
    elif direction == "SW":
        old_pos = (current_x, current_y)
        current_x, current_y = move_SW(current_x, current_y, visited_paths)
        if old_pos == (current_x, current_y):  # Hareket başarısız olduysa
            selected_directions[-1] = None
            last_direction = None
        else:
            last_direction = "SW"
    
    path.append((current_x, current_y))
    visited_paths.append(path.copy())

# Rastgele yolun çizimi
path_x = [x for x, y in path]
path_y = [y for x, y in path]
plt.plot(path_x, path_y, color="blue", linewidth=2, marker="o", markersize=5)

# Toplam mesafe ve yön değişikliği hesaplama
horizontal_distance = 0  # Sağa gidiş mesafesi (E)
diagonal_distance = 0    # Çapraz gidiş mesafesi (NE ve SW)
direction_changes = 0

# Her yön için mesafeleri hesapla
for direction in selected_directions:
    if direction == "E":
        horizontal_distance += 1
    elif direction in ["NE", "SW"]:
        diagonal_distance += 1

total_distance = horizontal_distance + diagonal_distance

# Yön değişikliklerini say (sadece geçerli hareketler için)
prev_direction = None
for direction in selected_directions:
    if direction is not None:  # Sadece geçerli hareketleri kontrol et
        if prev_direction is not None and direction != prev_direction:
            direction_changes += 1
        prev_direction = direction

# Bilgileri görüntüye ekleme
metrics_text = (
    "📏 METRICS\n"
    "──────────────\n"
    f"📍 Total Distance = {horizontal_distance} (→) + {diagonal_distance} (↗↙)\n"
    f"🔄 Direction Changes: {direction_changes}"
)

# Metrik kutusu özelleştirme
plt.text(0, steps * sqrt3/2 + 0.3, metrics_text,
         bbox=dict(
             facecolor='white',
             edgecolor='lightgray',
             boxstyle='round,pad=0.6',
             alpha=0.9
         ),
         family='monospace',
         size=9,
         verticalalignment='bottom'
)

# Grid ve gösterim ayarları
plt.gca().set_aspect("equal", adjustable="box")
plt.grid(False)

# Eksen etiketlerini ve değerlerini ayarla
plt.xticks(range(0, steps+1, 2))
plt.yticks(np.arange(0, (steps+1) * sqrt3/2, sqrt3), range(0, steps+1, 2))

# Eksen çizgilerini incelt
plt.gca().spines['bottom'].set_linewidth(0.5)
plt.gca().spines['left'].set_linewidth(0.5)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Kenar boşluklarını ayarla
plt.tight_layout()

plt.show()
