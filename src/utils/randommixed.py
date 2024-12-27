import matplotlib.pyplot as plt
from math import comb

# Catalan sayılarının hesaplanması
def catalan_number(n):
    return comb(2 * n, n) // (n + 1)

# Catalan yolları oluşturma
def generate_catalan_path(n):
    path = []
    x, y = 0, 0  # Başlangıç noktası
    balance = 0  # Yukarı ve aşağı adımların dengesi
    for _ in range(2 * n):
        if balance == 0:
            path.append("U")  # Yalnızca yukarı çıkabilir
            balance += 1
        elif len(path) == 2 * n - 1 or balance == n:
            path.append("D")  # Yalnızca aşağı inebilir
            balance -= 1
        else:
            # Rastgele yukarı veya aşağı seçimi, ancak dengeyi koruyarak
            step = "U" if balance < n else "D"
            path.append(step)
            balance += 1 if step == "U" else -1
    return path

# Catalan yolunu grid üzerinde çizme
def draw_catalan_path(path, ax, color='blue', label=''):
    x, y = 0, 0
    xs, ys = [x], [y]
    for step in path:
        if step == "U":
            y += 1
        elif step == "D":
            y -= 1
        x += 1
        xs.append(x)
        ys.append(y)
    ax.plot(xs, ys, color=color, label=label)
    ax.scatter(xs, ys, color='red', s=10)

# Catalan yollarını analiz ve görselleştirme
def visualize_catalan_paths(n_paths, n_steps):
    fig, ax = plt.subplots(figsize=(8, 8))
    for i in range(n_paths):
        path = generate_catalan_path(n_steps)
        draw_catalan_path(path, ax, label=f"Path {i+1}")
    ax.legend()
    ax.grid(True)
    ax.set_title(f"Catalan Paths ({n_paths} Paths, {n_steps} Steps)")
    plt.show()

# Analiz: Catalan sayıları ve yolların dağılımı
def analyze_catalan_numbers(max_n):
    numbers = [catalan_number(n) for n in range(max_n)]
    plt.figure(figsize=(10, 6))
    plt.bar(range(max_n), numbers, color='skyblue', edgecolor='black')
    plt.title("Catalan Numbers")
    plt.xlabel("n")
    plt.ylabel("C(n)")
    plt.show()

# Parametreler
n_steps = 10  # Adım sayısı
n_paths = 5   # Üretilecek yol sayısı

# Catalan yollarını görselleştir
visualize_catalan_paths(n_paths, n_steps)

# Catalan sayılarını analiz et
analyze_catalan_numbers(10)
