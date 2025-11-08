import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
from integral_calculator import IntegralCalculator

class IntegralApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Integrales Triples")
        self.root.geometry("600x700")

        # Variables de control
        self.coordinate_system = tk.StringVar(value="rectangular")
        self.function_var = tk.StringVar(value="x*y*z")
        
        # Límites de integración
        self.x_min = tk.StringVar(value="0")
        self.x_max = tk.StringVar(value="1")
        self.y_min = tk.StringVar(value="0")
        self.y_max = tk.StringVar(value="1")
        self.z_min = tk.StringVar(value="0")
        self.z_max = tk.StringVar(value="1")

        self.create_widgets()

    def create_widgets(self):
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        ttk.Label(main_frame, text="Calculadora de Integrales Triples", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Selector de sistema de coordenadas
        ttk.Label(main_frame, text="Sistema de Coordenadas:").grid(row=1, column=0, sticky=tk.W)
        coordinate_combo = ttk.Combobox(main_frame, textvariable=self.coordinate_system, 
                                        values=["rectangular", "cilíndrico", "esférico"], 
                                        state="readonly", width=20)
        coordinate_combo.grid(row=1, column=1, sticky=tk.W)
        coordinate_combo.bind("<<ComboboxSelected>>", self.update_coordinate_labels)

        # Función a integrar
        ttk.Label(main_frame, text="Función a integrar (f(x,y,z)):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.function_var, width=30).grid(row=2, column=1, sticky=tk.W)

        # Marcos para límites
        limits_frame = ttk.LabelFrame(main_frame, text="Límites de Integración")
        limits_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        # Etiquetas de límites
        self.limit_labels = {
            "x_min": ttk.Label(limits_frame, text="x mín:"),
            "x_max": ttk.Label(limits_frame, text="x máx:"),
            "y_min": ttk.Label(limits_frame, text="y mín:"),
            "y_max": ttk.Label(limits_frame, text="y máx:"),
            "z_min": ttk.Label(limits_frame, text="z mín:"),
            "z_max": ttk.Label(limits_frame, text="z máx:")
        }

        # Entradas de límites
        self.limit_entries = {
            "x_min": ttk.Entry(limits_frame, textvariable=self.x_min, width=10),
            "x_max": ttk.Entry(limits_frame, textvariable=self.x_max, width=10),
            "y_min": ttk.Entry(limits_frame, textvariable=self.y_min, width=10),
            "y_max": ttk.Entry(limits_frame, textvariable=self.y_max, width=10),
            "z_min": ttk.Entry(limits_frame, textvariable=self.z_min, width=10),
            "z_max": ttk.Entry(limits_frame, textvariable=self.z_max, width=10)
        }

        # Colocar etiquetas y entradas
        limit_positions = [
            ("x_min", 0, 0), ("x_max", 0, 1), 
            ("y_min", 1, 0), ("y_max", 1, 1), 
            ("z_min", 2, 0), ("z_max", 2, 1)
        ]
        for name, row, col in limit_positions:
            self.limit_labels[name].grid(row=row, column=col*2, sticky=tk.W, padx=5)
            self.limit_entries[name].grid(row=row, column=col*2+1, sticky=tk.W, padx=5)

        # Botón de cálculo
        ttk.Button(main_frame, text="Calcular Integral", command=self.calculate_integral).grid(row=4, column=0, columnspan=2, pady=10)

        # Resultado
        self.result_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.result_var, wraplength=500).grid(row=5, column=0, columnspan=2, pady=10)

        # Actualizar etiquetas iniciales
        self.update_coordinate_labels()

    def update_coordinate_labels(self, event=None):
        """Actualizar etiquetas de límites según el sistema de coordenadas"""
        sistema = self.coordinate_system.get()
        
        if sistema == "rectangular":
            labels = ["x mín:", "x máx:", "y mín:", "y máx:", "z mín:", "z máx:"]
        elif sistema == "cilíndrico":
            labels = ["r mín:", "r máx:", "θ mín:", "θ máx:", "z mín:", "z máx:"]
        else:  # esférico
            labels = ["ρ mín:", "ρ máx:", "θ mín:", "θ máx:", "φ mín:", "φ máx:"]
        
        limit_names = ["x_min", "x_max", "y_min", "y_max", "z_min", "z_max"]
        
        for name, label in zip(limit_names, labels):
            self.limit_labels[name].config(text=label)

    def calculate_integral(self):
        """Calcular la integral según el sistema de coordenadas seleccionado"""
        try:
            # Parsear la función
            x, y, z = sp.symbols('x y z')
            f = sp.sympify(self.function_var.get())

            # Obtener límites
            sistema = self.coordinate_system.get()
            
            if sistema == "rectangular":
                x_limits = [float(self.x_min.get()), float(self.x_max.get())]
                y_limits = [float(self.y_min.get()), float(self.y_max.get())]
                z_limits = [float(self.z_min.get()), float(self.z_max.get())]
                
                resultado = IntegralCalculator.integral_rectangular(f, x_limits, y_limits, z_limits)
            
            elif sistema == "cilíndrico":
                r_limits = [float(self.x_min.get()), float(self.x_max.get())]
                theta_limits = [float(self.y_min.get()), float(self.y_max.get())]
                z_limits = [float(self.z_min.get()), float(self.z_max.get())]
                
                resultado = IntegralCalculator.integral_cylindrical(f, r_limits, theta_limits, z_limits)
            
            else:  # esférico
                rho_limits = [float(self.x_min.get()), float(self.x_max.get())]
                theta_limits = [float(self.y_min.get()), float(self.y_max.get())]
                phi_limits = [float(self.z_min.get()), float(self.z_max.get())]
                
                resultado = IntegralCalculator.integral_spherical(f, rho_limits, theta_limits, phi_limits)
            
            # Mostrar resultado
            self.result_var.set(f"Resultado de la integral: {resultado}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular la integral: {str(e)}")

def main():
    root = tk.Tk()
    app = IntegralApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
