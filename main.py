import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BhaskaraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Equações do 2º Grau - ax² + bx + c = 0")
        self.root.geometry("950x620")
        self.root.configure(bg="#1e1e2e")
        self.root.minsize(850, 550)

        self.setup_styles()
        self.create_widgets()
        self.calcular() # Cálculo inicial de demonstração

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e2e")
        style.configure("Card.TFrame", background="#252538")
        style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 11))
        style.configure("Card.TLabel", background="#252538", foreground="#cdd6f4", font=("Segoe UI", 11))
        style.configure("Title.TLabel", background="#1e1e2e", foreground="#89b4fa", font=("Segoe UI", 16, "bold"))
        style.configure("Formula.TLabel", background="#252538", foreground="#f9e2af", font=("Segoe UI", 13, "bold"))
        style.configure("TButton", background="#89b4fa", foreground="#11111b", font=("Segoe UI", 11, "bold"), padding=8)
        style.map("TButton", background=[("active", "#b4befe")])
        style.configure("Clear.TButton", background="#45475a", foreground="#cdd6f4", font=("Segoe UI", 11), padding=8)
        style.map("Clear.TButton", background=[("active", "#585b70")])

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Painel Esquerdo: Entradas e Passo a Passo
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 20))

        ttk.Label(left_frame, text="Equação do 2º Grau", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

        # Card da Fórmula e Inputs
        input_card = ttk.Frame(left_frame, style="Card.TFrame", padding=15)
        input_card.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(input_card, text="ax² + bx + c = 0", style="Formula.TLabel").pack(anchor="center", pady=(0, 12))

        grid_frame = ttk.Frame(input_card, style="Card.TFrame")
        grid_frame.pack(fill=tk.X)

        self.entry_a = self.create_input(grid_frame, "Coeficiente a:", "1", 0)
        self.entry_b = self.create_input(grid_frame, "Coeficiente b:", "-5", 1)
        self.entry_c = self.create_input(grid_frame, "Coeficiente c:", "6", 2)

        # Botões
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(btn_frame, text="Calcular Raízes", command=self.calcular).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(btn_frame, text="Limpar", style="Clear.TButton", command=self.limpar).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # Área de Resultados e Passo a Passo
        ttk.Label(left_frame, text="Resolução Passo a Passo:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 5))
        
        self.result_text = tk.Text(
            left_frame, width=42, height=15, bg="#181825", fg="#a6e3a1",
            font=("Consolas", 11), relief="flat", padx=12, pady=12, state="disabled"
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Painel Direito: Gráfico da Parábola
        right_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor="#252538")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#181825")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_input(self, parent, label_text, default_val, row):
        ttk.Label(parent, text=label_text, style="Card.TLabel").grid(row=row, column=0, sticky="w", pady=6)
        entry = tk.Entry(
            parent, font=("Segoe UI", 11), bg="#181825", fg="#cdd6f4",
            insertbackground="#cdd6f4", relief="flat", width=15
        )
        entry.insert(0, default_val)
        entry.grid(row=row, column=1, pady=6, padx=(15, 0), ipady=4)
        entry.bind("<Return>", lambda event: self.calcular())
        return entry

    def calcular(self):
        try:
            a = float(self.entry_a.get().replace(",", "."))
            b = float(self.entry_b.get().replace(",", "."))
            c = float(self.entry_c.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos para a, b e c.")
            return

        if a == 0:
            messagebox.showwarning("Atenção", "O coeficiente 'a' não pode ser zero em uma equação do 2º grau.")
            return

        delta = (b ** 2) - (4 * a * c)
        xv = -b / (2 * a)
        yv = -delta / (4 * a)
        concavidade = "Para cima (Ponto de Mínimo)" if a > 0 else "Para baixo (Ponto de Máximo)"

        res = []
        res.append(f"Equação: ({a:g})x² + ({b:g})x + ({c:g}) = 0")
        res.append("-" * 38)
        res.append("1. Cálculo do Discriminante (Δ):")
        res.append(f"   Δ = b² - 4·a·c")
        res.append(f"   Δ = ({b:g})² - 4·({a:g})·({c:g})")
        res.append(f"   Δ = {b**2:g} - ({4*a*c:g})")
        res.append(f"   Δ = {delta:g}\n")

        res.append("2. Cálculo das Raízes (Bhaskara):")
        raizes_reais = []

        if delta > 0:
            x1 = (-b + math.sqrt(delta)) / (2 * a)
            x2 = (-b - math.sqrt(delta)) / (2 * a)
            raizes_reais = [x1, x2]
            res.append("   Δ > 0: Duas raízes reais e distintas.")
            res.append(f"   x = (-b ± √Δ) / (2·a)")
            res.append(f"   x₁ = ({-b:g} + {math.sqrt(delta):.4g}) / {2*a:g} = {x1:.4f}")
            res.append(f"   x₂ = ({-b:g} - {math.sqrt(delta):.4g}) / {2*a:g} = {x2:.4f}\n")
        elif delta == 0:
            x1 = -b / (2 * a)
            raizes_reais = [x1]
            res.append("   Δ = 0: Uma raiz real dupla.")
            res.append(f"   x = -b / (2·a)")
            res.append(f"   x₁ = x₂ = {x1:.4f}\n")
        else:
            real_part = -b / (2 * a)
            imag_part = math.sqrt(-delta) / (2 * a)
            res.append("   Δ < 0: Não possui raízes reais.")
            res.append("   Raízes Complexas:")
            res.append(f"   x₁ = {real_part:.4g} + { abs(imag_part):.4g}i")
            res.append(f"   x₂ = {real_part:.4g} - { abs(imag_part):.4g}i\n")

        res.append("3. Vértice e Concavidade:")
        res.append(f"   Xv = -b / (2a) = {xv:.4f}")
        res.append(f"   Yv = -Δ / (4a) = {yv:.4f}")
        res.append(f"   Vértice V({xv:.2f}, {yv:.2f})")
        res.append(f"   Concavidade: {concavidade}")

        self.mostrar_texto("\n".join(res))
        self.plotar_grafico(a, b, c, xv, yv, raizes_reais)

    def mostrar_texto(self, texto):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, texto)
        self.result_text.config(state="disabled")

    def plotar_grafico(self, a, b, c, xv, yv, raizes):
        self.ax.clear()
        self.ax.set_facecolor("#181825")

        # Define o intervalo de X centralizado no vértice e englobando as raízes
        alcance = max(abs(r - xv) for r in raizes) * 1.8 if raizes else 5.0
        alcance = max(alcance, 4.0)

        x = np.linspace(xv - alcance, xv + alcance, 400)
        y = a * (x ** 2) + b * x + c

        # Eixos X e Y
        self.ax.axhline(0, color="#585b70", linewidth=1.2, linestyle="--")
        self.ax.axvline(0, color="#585b70", linewidth=1.2, linestyle="--")

        # Curva da parábola
        self.ax.plot(x, y, color="#89b4fa", linewidth=2.5, label=f"f(x) = {a:g}x² + {b:g}x + {c:g}")

        # Ponto do Vértice
        self.ax.scatter([xv], [yv], color="#f38ba8", s=70, zorder=5, label=f"Vértice ({xv:.2f}, {yv:.2f})")

        # Pontos das Raízes Reais
        if raizes:
            self.ax.scatter(raizes, [0]*len(raizes), color="#a6e3a1", s=70, zorder=5, label="Raízes Reais")

        self.ax.set_title("Gráfico da Parábola", color="#cdd6f4", fontsize=12, fontweight="bold", pad=12)
        self.ax.tick_params(colors="#cdd6f4")
        for spine in self.ax.spines.values():
            spine.set_color("#45475a")
        
        self.ax.grid(True, linestyle=":", alpha=0.3, color="#cdd6f4")
        self.ax.legend(facecolor="#252538", edgecolor="#45475a", labelcolor="#cdd6f4", fontsize=9)

        self.fig.tight_layout()
        self.canvas.draw()

    def limpar(self):
        for entry, val in [(self.entry_a, "1"), (self.entry_b, "0"), (self.entry_c, "0")]:
            entry.delete(0, tk.END)
            entry.insert(0, val)
        self.calcular()

if __name__ == "__main__":
    root = tk.Tk()
    app = BhaskaraApp(root)
    root.mainloop()
