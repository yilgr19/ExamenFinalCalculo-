import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import sys
import re
import importlib

# Importar el módulo
import integral_calculator


class IntegralApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Calculadora de Integrales Triples")
        self.root.geometry("700x850")

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
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        title_label = ttk.Label(main_frame, text="Calculadora de Integrales Triples", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Sistema de coordenadas
        ttk.Label(main_frame, text="Sistema de Coordenadas:").grid(row=1, column=0, sticky=tk.W, pady=5)
        coordinate_combo = ttk.Combobox(main_frame, textvariable=self.coordinate_system, 
                                        values=["rectangular", "cilíndrico", "esférico"], 
                                        state="readonly", width=25)
        coordinate_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        coordinate_combo.bind("<<ComboboxSelected>>", self.update_coordinate_labels)

        # Función a integrar
        ttk.Label(main_frame, text="Función a integrar:").grid(row=2, column=0, sticky=tk.W, pady=5)
        function_entry = ttk.Entry(main_frame, textvariable=self.function_var, width=40)
        function_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

        # Ayuda de sintaxis
        help_text = "💡 Sintaxis: x*y, x^2, sin(x), cos(y), exp(z), sqrt(x), pi, e | Decimales: 0.5 o 0,5"
        ttk.Label(main_frame, text=help_text, font=("Arial", 8), foreground="gray").grid(row=3, column=0, columnspan=2, pady=5)

        # Frame de límites
        limits_frame = ttk.LabelFrame(main_frame, text="Límites de Integración", padding="10")
        limits_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        self.limit_labels = {
            "x_min": ttk.Label(limits_frame, text="x mín:"),
            "x_max": ttk.Label(limits_frame, text="x máx:"),
            "y_min": ttk.Label(limits_frame, text="y mín:"),
            "y_max": ttk.Label(limits_frame, text="y máx:"),
            "z_min": ttk.Label(limits_frame, text="z mín:"),
            "z_max": ttk.Label(limits_frame, text="z máx:")
        }

        self.limit_entries = {
            "x_min": ttk.Entry(limits_frame, textvariable=self.x_min, width=12),
            "x_max": ttk.Entry(limits_frame, textvariable=self.x_max, width=12),
            "y_min": ttk.Entry(limits_frame, textvariable=self.y_min, width=12),
            "y_max": ttk.Entry(limits_frame, textvariable=self.y_max, width=12),
            "z_min": ttk.Entry(limits_frame, textvariable=self.z_min, width=12),
            "z_max": ttk.Entry(limits_frame, textvariable=self.z_max, width=12)
        }

        positions = [
            ("x_min", 0, 0), ("x_max", 0, 2),
            ("y_min", 1, 0), ("y_max", 1, 2),
            ("z_min", 2, 0), ("z_max", 2, 2)
        ]
        for name, r, c in positions:
            self.limit_labels[name].grid(row=r, column=c, sticky=tk.E, padx=5, pady=3)
            self.limit_entries[name].grid(row=r, column=c+1, sticky=tk.W, padx=5, pady=3)

        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)
        ttk.Button(button_frame, text="🧮 Calcular Integral", command=self.calculate_integral).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Limpiar", command=self.clear_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📚 Ejemplos", command=self.show_examples).pack(side=tk.LEFT, padx=5)

        # Resultado
        result_frame = ttk.LabelFrame(main_frame, text="Resultado", padding="5")
        result_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky='nsew')
        self.result_text = tk.Text(result_frame, height=22, width=80, wrap=tk.WORD,
                                   font=("Consolas", 9), bg="#f5f5f5")
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.result_text.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(6, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        self.update_coordinate_labels()
        self.result_text.insert(1.0, "👋 Bienvenido a la Calculadora de Integrales Triples\n\n"
                                    "Ingresa una función y límites, luego presiona 'Calcular Integral'.\n"
                                    "Usa el botón 'Ejemplos' para ver funciones de prueba.\n\n"
                                    "🔄 AUTO-RELOAD ACTIVADO: Los cambios en integral_calculator.py\n"
                                    "   se cargarán automáticamente en cada cálculo.")

    # ======================== 🔧 PARSER CORREGIDO ========================
    def parse_function_complete(self, func_str):
        """Parser matemático completo corregido (soporta sin**2(x), cos**3(phi), etc.)"""
        print("=" * 60)
        print(f"📝 Parseando función: '{func_str}'")

        func_str = re.sub(r'(\d+),(\d+)', r'\1.\2', func_str)
        func_str = func_str.replace('^', '**').replace('√', 'sqrt').replace('π', 'pi')
        func_str = func_str.replace('×', '*').replace('÷', '/')

        # Reescribir sin**2(phi) → (sin(phi))**2
        func_str = re.sub(r'(sin|cos|tan|sec|csc|cot)\*\*\s*(\d+)\s*\(\s*([a-zA-Z0-9_+\-*/^ ]+)\s*\)',
                          r'(\1(\3))**\2', func_str)

        # Multiplicaciones implícitas
        func_str = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', func_str)
        func_str = re.sub(r'([a-zA-Z)])(\d)', r'\1*\2', func_str)
        func_str = re.sub(r'\)(\()', r')*\1', func_str)

        print(f"✅ Después de limpieza final: '{func_str}'")

        x, y, z = sp.symbols('x y z', real=True)
        r, theta, rho, phi = sp.symbols('r theta rho phi', real=True, positive=True)
        locals_dict = {
            'x': x, 'y': y, 'z': z,
            'r': r, 'theta': theta, 'rho': rho, 'phi': phi,
            'pi': sp.pi, 'e': sp.E,
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
            'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
            'exp': sp.exp, 'log': sp.log, 'ln': sp.log,
            'sqrt': sp.sqrt, 'abs': sp.Abs
        }

        try:
            parsed_func = sp.sympify(func_str, locals=locals_dict)
            print(f"✅ Función parseada correctamente: {parsed_func}")
            return parsed_func
        except Exception as e:
            print(f"❌ ERROR al parsear: {e}")
            raise ValueError(f"No se pudo parsear la función: {func_str}\nError: {e}")

    # ===============================================================
    def parse_limit(self, limit_str):
        limit_str = re.sub(r'(\d+),(\d+)', r'\1.\2', limit_str)
        limit_str = limit_str.replace('π', 'pi').replace('^', '**')
        return sp.sympify(limit_str, locals={'pi': sp.pi, 'e': sp.E})

    def update_coordinate_labels(self, event=None):
        sistema = self.coordinate_system.get()
        if sistema == "rectangular":
            labels = ["x mín:", "x máx:", "y mín:", "y máx:", "z mín:", "z máx:"]
        elif sistema == "cilíndrico":
            labels = ["r mín:", "r máx:", "θ mín:", "θ máx:", "z mín:", "z máx:"]
        else:
            labels = ["ρ mín:", "ρ máx:", "θ mín:", "θ máx:", "φ mín:", "φ máx:"]
        for name, label in zip(self.limit_labels.keys(), labels):
            self.limit_labels[name].config(text=label)

    def clear_results(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, "✅ Resultados limpios. Listo para un nuevo cálculo.")

    def show_examples(self):
        examples = """╔═══════════════════════════════════════════════════════════════════╗
║                📚 EJEMPLOS DE FUNCIONES                           ║
╚═══════════════════════════════════════════════════════════════════╝

🔹 BÁSICAS:
   • x*y*z                    → Producto simple
   • x^2 + y^2 + z^2          → Suma de cuadrados
   • 2*x*y + 3*z              → Combinación lineal

🔹 CILÍNDRICAS:
   • r**2*sin(theta)
   • r**3*cos(theta)

🔹 ESFÉRICAS:
   • rho**2*sin(phi)**2
   • rho**3*cos(phi)

═══════════════════════════════════════════════════════════════════
"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, examples)

    def calculate_integral(self):
        """Ejecuta el cálculo real"""
        try:
            print("\n" + "="*60)
            print("🚀 NUEVA EJECUCIÓN DE CÁLCULO")
            print("="*60)

            importlib.reload(integral_calculator)
            IntegralCalculator = integral_calculator.IntegralCalculator

            coordinate_system = self.coordinate_system.get().lower()
            func_str = self.function_var.get()

            f = self.parse_function_complete(func_str)

            if coordinate_system in ['cilindrico', 'cilíndrico']:
                r_min = self.parse_limit(self.x_min.get())
                r_max = self.parse_limit(self.x_max.get())
                theta_min = self.parse_limit(self.y_min.get())
                theta_max = self.parse_limit(self.y_max.get())
                z_min = self.parse_limit(self.z_min.get())
                z_max = self.parse_limit(self.z_max.get())
                resultado = IntegralCalculator.integral_cylindrical(
                    f, [r_min, r_max], [theta_min, theta_max], [z_min, z_max]
                )

            elif coordinate_system in ['esferico', 'esférico']:
                rho_min = self.parse_limit(self.x_min.get())
                rho_max = self.parse_limit(self.x_max.get())
                theta_min = self.parse_limit(self.y_min.get())
                theta_max = self.parse_limit(self.y_max.get())
                phi_min = self.parse_limit(self.z_min.get())
                phi_max = self.parse_limit(self.z_max.get())
                resultado = IntegralCalculator.integral_spherical(
                    f, [rho_min, rho_max], [theta_min, theta_max], [phi_min, phi_max]
                )

            else:
                x_min = self.parse_limit(self.x_min.get())
                x_max = self.parse_limit(self.x_max.get())
                y_min = self.parse_limit(self.y_min.get())
                y_max = self.parse_limit(self.y_max.get())
                z_min = self.parse_limit(self.z_min.get())
                z_max = self.parse_limit(self.z_max.get())
                resultado = IntegralCalculator.integral_rectangular(
                    f, [x_min, x_max], [y_min, y_max], [z_min, z_max]
                )

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, resultado["pasos"])
            self.result_text.insert(tk.END, f"\n\n✅ Resultado simbólico: {resultado['resultado_simbolico']}")
            self.result_text.insert(tk.END, f"\n✅ Valor numérico: {resultado['resultado_manual']}")
        except Exception as e:
            messagebox.showerror("Error en el cálculo", str(e))
            print(e)


def main():
    root = tk.Tk()
    app = IntegralApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
