import random
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==============================================================================
# DATA KASUS KNAPSACK (Dapat disesuaikan saat praktikum)
# ==============================================================================
ITEMS = [
    {"name": "Barang1", "profit": 10, "weight": 5},
    {"name": "Barang2", "profit": 40, "weight": 4},
    {"name": "Barang3", "profit": 30, "weight": 6},
    {"name": "Barang4", "profit": 50, "weight": 3},
    {"name": "Barang5", "profit": 35, "weight": 7},
]
MAX_WEIGHT = 15

# ==============================================================================
# OUTPUT TERMINAL (Sesuai Format yang Diminta)
# ==============================================================================
print(f"{'Barang':<10}{'Keuntungan':<14}{'Ukuran'}")
for item in ITEMS:
    print(f"{item['name']:<10}{item['profit']:<14}{item['weight']}")

print(f"\nUkuran Maksimal Gudang: {MAX_WEIGHT}\n")
print("-" * 40) # Pembatas di terminal biar rapi

# ==============================================================================
# FUNGSI-FUNGSI ALGORITMA GENETIKA (NIM: H1D024064)
# ==============================================================================

def fitness(chromosome):
    """Menghitung total profit. Jika melebihi kapasitas, fitness = 0."""
    total_weight = 0
    total_profit = 0
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_weight += ITEMS[i]["weight"]
            total_profit += ITEMS[i]["profit"]
    if total_weight > MAX_WEIGHT:
        return 0  # Penalti jika melebihi ukuran maksimal gudang
    return total_profit

def create_chromosome():
    """Membuat kromosom acak sepanjang jumlah barang."""
    return [random.randint(0, 1) for _ in range(len(ITEMS))]

def selection_rws(population, fitnesses):
    """Seleksi menggunakan Roulette Wheel Selection (RWS) sesuai NIM."""
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        return random.choice(population)
    
    pick = random.uniform(0, total_fitness)
    current = 0
    for chromosome, fit_val in zip(population, fitnesses):
        current += fit_val
        if current > pick:
            return chromosome
    return population[-1]

def crossover_two_point(parent1, parent2):
    """Crossover menggunakan Two Point Crossover sesuai NIM."""
    length = len(parent1)
    pt1 = random.randint(1, length - 2)
    pt2 = random.randint(pt1 + 1, length - 1)
    
    child1 = parent1[:pt1] + parent2[pt1:pt2] + parent1[pt2:]
    child2 = parent2[:pt1] + parent1[pt1:pt2] + parent2[pt2:]
    return child1, child2

def mutation_swap(chromosome):
    """Mutasi menggunakan Swap Mutation sesuai NIM."""
    mutated = chromosome.copy()
    idx1, idx2 = random.sample(range(len(mutated)), 2)
    mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
    return mutated

# ==============================================================================
# ENGINE ALGORITMA GENETIKA
# ==============================================================================

def run_genetic_algorithm(pop_size, generations, crossover_rate, mutation_rate):
    population = [create_chromosome() for _ in range(pop_size)]
    history_best_fitness = []
    
    best_chromosome = None
    best_fitness_score = -1

    for gen in range(generations):
        fitnesses = [fitness(chrom) for chrom in population]
        
        # Cari solusi terbaik di generasi ini
        for chrom, fit in zip(population, fitnesses):
            if fit > best_fitness_score:
                best_fitness_score = fit
                best_chromosome = chrom
        
        history_best_fitness.append(best_fitness_score)
        
        # Pembentukan generasi baru
        new_population = []
        while len(new_population) < pop_size:
            # Seleksi Orang Tua (RWS)
            p1 = selection_rws(population, fitnesses)
            p2 = selection_rws(population, fitnesses)
            
            # Crossover (Two Point)
            if random.random() < crossover_rate:
                c1, c2 = crossover_two_point(p1, p2)
            else:
                c1, c2 = p1.copy(), p2.copy()
                
            # Mutasi (Swap)
            if random.random() < mutation_rate:
                c1 = mutation_swap(c1)
            if random.random() < mutation_rate:
                c2 = mutation_swap(c2)
                
            new_population.extend([c1, c2])
            
        population = new_population[:pop_size]
        
    return best_chromosome, best_fitness_score, history_best_fitness

# ==============================================================================
# ANTARMUKA GUI (TKINTER)
# ==============================================================================

class KnapsackGAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Praktikum KB - Pertemuan 10 (NIM: H1D024064)")
        self.root.geometry("900x600")
        
        # Panel Input Kontrol (Kiri)
        control_frame = ttk.LabelFrame(root, text=" Parameter GA (NIM: H1D024064) ", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Info Metode Tetap Sesuai NIM
        ttk.Label(control_frame, text="Metode Seleksi: RWS", font=('Helvetica', 9, 'bold')).pack(anchor=tk.W, pady=2)
        ttk.Label(control_frame, text="Metode Crossover: Two Point", font=('Helvetica', 9, 'bold')).pack(anchor=tk.W, pady=2)
        ttk.Label(control_frame, text="Metode Mutasi: Swap", font=('Helvetica', 9, 'bold')).pack(anchor=tk.W, pady=2)
        ttk.Separator(control_frame, orient='horizontal').pack(fill='x', pady=10)

        # Input Parameter Dinamis
        ttk.Label(control_frame, text="Ukuran Populasi:").pack(anchor=tk.W)
        self.entry_pop = ttk.Entry(control_frame)
        self.entry_pop.insert(0, "20")
        self.entry_pop.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Jumlah Generasi:").pack(anchor=tk.W)
        self.entry_gen = ttk.Entry(control_frame)
        self.entry_gen.insert(0, "50")
        self.entry_gen.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Crossover Rate (0-1):").pack(anchor=tk.W)
        self.entry_cr = ttk.Entry(control_frame)
        self.entry_cr.insert(0, "0.8")
        self.entry_cr.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Mutation Rate (0-1):").pack(anchor=tk.W)
        self.entry_mr = ttk.Entry(control_frame)
        self.entry_mr.insert(0, "0.1")
        self.entry_mr.pack(fill=tk.X, pady=5)
        
        btn_run = ttk.Button(control_frame, text="Jalankan Optimasi", command=self.on_run)
        btn_run.pack(fill=tk.X, pady=15)
        
        # Hasil Output Text
        self.txt_result = tk.Text(control_frame, width=30, height=12, font=('Consolas', 9))
        self.txt_result.pack(fill=tk.BOTH, expand=True)

        # Panel Output Grafik (Kanan)
        self.graph_frame = ttk.LabelFrame(root, text=" Grafik Konvergensi Nilai Fitness ", padding=10)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_run(self):
        try:
            pop_size = int(self.entry_pop.get())
            generations = int(self.entry_gen.get())
            cr = float(self.entry_cr.get())
            mr = float(self.entry_mr.get())
            
            # Eksekusi Algoritma Genetika
            best_chrom, best_fit, history = run_genetic_algorithm(pop_size, generations, cr, mr)
            
            # Hitung total berat akhir untuk validasi
            total_w = sum(ITEMS[i]["weight"] for i in range(len(best_chrom)) if best_chrom[i] == 1)
            
            # Tampilkan Hasil di GUI Text area
            self.txt_result.delete("1.0", tk.END)
            self.txt_result.insert(tk.END, f"=== HASIL TERBAIK ===\n")
            self.txt_result.insert(tk.END, f"Kromosom: {best_chrom}\n")
            self.txt_result.insert(tk.END, f"Total Profit: {best_fit}\n")
            self.txt_result.insert(tk.END, f"Total Ukuran: {total_w}/{MAX_WEIGHT}\n\n")
            self.txt_result.insert(tk.END, f"Barang yang dibeli:\n")
            
            for i, gene in enumerate(best_chrom):
                if gene == 1:
                    self.txt_result.insert(tk.END, f"- {ITEMS[i]['name']}\n")
                    
            # Tampilkan Plot Grafik (Sama, tidak diubah)
            self.ax.clear()
            self.ax.plot(range(1, generations + 1), history, color='blue', marker='o', markersize=3)
            self.ax.set_title("Peningkatan Profit per Generasi")
            self.ax.set_xlabel("Generasi")
            self.ax.set_ylabel("Fitness Terbaik (Profit)")
            self.ax.grid(True)
            self.canvas.draw()
            
        except ValueError:
            messagebox.showerror("Error Input", "Pastikan semua input parameter bernilai valid!")

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackGAApp(root)
    root.mainloop()