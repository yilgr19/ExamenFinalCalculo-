import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sympy as sp
import sys
import re
import importlib

import integral_calculator


class IntegralApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Integrales Triples")
        self.root.geometry("1000x700")
        self.root.state('zoomed')  # Maximizar ventana

        self.coordinate_system = tk.StringVar(value="rectangular")
        self.function_var = tk.StringVar(value="x+y")
        
        self.x_min = tk.StringVar(value="0")
        self.x_max = tk.StringVar(value="2")
        self.y_min = tk.StringVar(value="0")
        self.y_max = tk.StringVar(value="2-x")
        self.z_min = tk.StringVar(value="0")
        self.z_max = tk.StringVar(value="1")

        self.create_widgets()

    def create_widgets(self):
        # Frame principal con dos columnas
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)

        # PANEL IZQUIERDO - Controles
        left_frame = ttk.Frame(main_frame, padding="5")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(left_frame, text="Calculadora de Integrales Triples", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(left_frame, text="Sistema de Coordenadas:").grid(row=1, column=0, sticky=tk.W, pady=5)
        coordinate_combo = ttk.Combobox(left_frame, textvariable=self.coordinate_system, 
                                        values=["rectangular", "cilindrico", "esferico"], 
                                        state="readonly", width=20)
        coordinate_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        coordinate_combo.bind("<<ComboboxSelected>>", self.update_coordinate_labels)

        ttk.Label(left_frame, text="Funcion a integrar:").grid(row=2, column=0, sticky=tk.W, pady=5)
        function_entry = ttk.Entry(left_frame, textvariable=self.function_var, width=25)
        function_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        # Guía de sintaxis compacta
        syntax_frame = ttk.LabelFrame(left_frame, text="📖 Sintaxis", padding="5")
        syntax_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        syntax_label = ttk.Label(syntax_frame, 
                                text="Operadores: + - * / **\n"
                                     "Funciones: sin() cos() sqrt() exp() log()\n"
                                     "Constantes: pi, e\n"
                                     "Ejemplo: x*y^2, sin(x)*cos(y)",
                                font=("Arial", 8), justify=tk.LEFT)
        syntax_label.pack(anchor=tk.W)

        limits_frame = ttk.LabelFrame(left_frame, text="Limites de Integracion", padding="5")
        limits_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        instruccion = ttk.Label(limits_frame, 
                               text="Puedes usar variables\n(ej: 2-x, sqrt(y))",
                               font=("Arial", 8, "bold"), foreground="blue")
        instruccion.grid(row=0, column=0, columnspan=4, pady=5)

        self.limit_labels = {
            "x_min": ttk.Label(limits_frame, text="x min:"),
            "x_max": ttk.Label(limits_frame, text="x max:"),
            "y_min": ttk.Label(limits_frame, text="y min:"),
            "y_max": ttk.Label(limits_frame, text="y max:"),
            "z_min": ttk.Label(limits_frame, text="z min:"),
            "z_max": ttk.Label(limits_frame, text="z max:")
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
            ("x_min", 1, 0), ("x_max", 1, 2),
            ("y_min", 2, 0), ("y_max", 2, 2),
            ("z_min", 3, 0), ("z_max", 3, 2)
        ]
        for name, r, c in positions:
            self.limit_labels[name].grid(row=r, column=c, sticky=tk.E, padx=3, pady=3)
            self.limit_entries[name].grid(row=r, column=c+1, sticky=(tk.W, tk.E), padx=3, pady=3)

        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="Calcular", 
                  command=self.calculate_integral, width=15).pack(pady=3)
        ttk.Button(button_frame, text="Limpiar", 
                  command=self.clear_results, width=15).pack(pady=3)
        ttk.Button(button_frame, text="Ejemplos", 
                  command=self.show_examples, width=15).pack(pady=3)
        ttk.Button(button_frame, text="Teoremas Vectoriales", 
                  command=self.open_vector_theorems, width=15).pack(pady=3)

        # PANEL DERECHO - Resultados (MÁS GRANDE)
        right_frame = ttk.LabelFrame(main_frame, text="📊 Resultado Detallado", padding="5")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        # Usar ScrolledText para mejor scroll
        self.result_text = scrolledtext.ScrolledText(
            right_frame, 
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#f5f5f5",
            relief=tk.SOLID,
            borderwidth=1
        )
        self.result_text.grid(row=0, column=0, sticky='nsew')

        self.update_coordinate_labels()
        self.result_text.insert(1.0, """═══════════════════════════════════════════════════════════
  CALCULADORA DE INTEGRALES TRIPLES - VERSIÓN MEJORADA
═══════════════════════════════════════════════════════════

✓ Soporta límites con variables (ej: y ≤ 2-x, z ≤ x)
✓ Procedimiento matemático detallado paso a paso
✓ Muestra evaluación en límites superior e inferior
✓ Teoremas Vectoriales (Green, Stokes, Divergencia)

EJEMPLOS DE LÍMITES VARIABLES:

A5) Función: x+y
    x: 0 → 2
    y: 0 → 2-x  ← Depende de x
    z: 0 → 1
    Resultado: 8/3

A6) Función: x*y^2*z
    x: 1 → 2
    y: 0 → 1
    z: 0 → x    ← Depende de x
    Resultado: 7/6

A7) Función: x^2 + y
    x: 0 → 1
    y: 0 → 1
    z: x → 1    ← Límite inferior depende de x
    Resultado: 5/6

═══════════════════════════════════════════════════════════
Presiona 'Calcular' para comenzar
Presiona 'Ejemplos' para ver más casos de uso
═══════════════════════════════════════════════════════════
""")

    def open_vector_theorems(self):
        try:
            nueva_ventana = tk.Toplevel(self.root)
            nueva_ventana.title("Teoremas Vectoriales")
            nueva_ventana.geometry("900x1150")
            
            import gui_vector_theorems
            importlib.reload(gui_vector_theorems)
            
            gui_vector_theorems.VectorTheoremsApp(nueva_ventana)
            
            nueva_ventana.update_idletasks()
            x = (nueva_ventana.winfo_screenwidth() // 2) - (450)
            y = (nueva_ventana.winfo_screenheight() // 2) - (550)
            nueva_ventana.geometry(f"+{x}+{y}")
            
        except ImportError as e:
            messagebox.showerror(
                "Error al abrir Teoremas Vectoriales",
                "No se pudo cargar el modulo 'gui_vector_theorems.py'\n\n"
                "Asegurate de que el archivo este en la misma carpeta que app.py\n\n"
                f"Error tecnico: {str(e)}"
            )
        except AttributeError as e:
            messagebox.showerror(
                "Error de Configuracion",
                "El modulo 'gui_vector_theorems' no tiene la clase 'VectorTheoremsApp'\n\n"
                "Verifica que el archivo este completo y correctamente guardado.\n\n"
                f"Error tecnico: {str(e)}"
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Ocurrio un error al abrir Teoremas Vectoriales:\n\n{str(e)}"
            )
            import traceback
            traceback.print_exc()

    def parse_function_complete(self, func_str):
        print("="*60)
        print(f"Parseando funcion: '{func_str}'")

        func_str = re.sub(r'(\d+),(\d+)', r'\1.\2', func_str)
        
        func_str = func_str.replace('^', '**').replace('√', 'sqrt').replace('π', 'pi')
        func_str = func_str.replace('×', '*').replace('÷', '/')

        func_str = re.sub(
            r'(sin|cos|tan|sec|csc|cot)\*\*\s*(\d+)\s*\(\s*([a-zA-Z0-9_+\-*/^ ]+)\s*\)',
            r'(\1(\3))**\2', 
            func_str
        )

        func_str = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', func_str)
        func_str = re.sub(r'([a-zA-Z)])(\d)', r'\1*\2', func_str)
        func_str = re.sub(r'\)(\()', r')*\1', func_str)

        print(f"Despues de limpieza: '{func_str}'")

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
            print(f"Funcion parseada: {parsed_func}")
            return parsed_func
        except Exception as e:
            print(f"ERROR al parsear: {e}")
            raise ValueError(f"No se pudo parsear: {func_str}\nError: {e}")

    def parse_limit(self, limit_str):
        limit_str = re.sub(r'(\d+),(\d+)', r'\1.\2', limit_str)
        limit_str = limit_str.replace('π', 'pi').replace('^', '**')
        
        x, y, z = sp.symbols('x y z', real=True)
        r, theta, rho, phi = sp.symbols('r theta rho phi', real=True, positive=True)
        
        locals_dict = {
            'x': x, 'y': y, 'z': z,
            'r': r, 'theta': theta, 'rho': rho, 'phi': phi,
            'pi': sp.pi, 'e': sp.E,
            'sqrt': sp.sqrt, 'exp': sp.exp, 'log': sp.log, 'ln': sp.log,
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan
        }
        
        return sp.sympify(limit_str, locals=locals_dict)

    def update_coordinate_labels(self, event=None):
        sistema = self.coordinate_system.get()
        if sistema == "rectangular":
            labels = ["x min:", "x max:", "y min:", "y max:", "z min:", "z max:"]
        elif sistema == "cilindrico":
            labels = ["r min:", "r max:", "theta min:", "theta max:", "z min:", "z max:"]
        else:
            labels = ["rho min:", "rho max:", "theta min:", "theta max:", "phi min:", "phi max:"]
        
        for name, label in zip(self.limit_labels.keys(), labels):
            self.limit_labels[name].config(text=label)

    def clear_results(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, "═══════════════════════════════════════════\nResultados limpiados.\nListo para un nuevo cálculo.\n═══════════════════════════════════════════")

    def show_examples(self):
        examples = """═══════════════════════════════════════════════════════════
  EJEMPLOS DE FUNCIONES Y LÍMITES
═══════════════════════════════════════════════════════════

EJERCICIO A5 - Límites variables:
   Sistema: Rectangular
   Función: x+y
   Límites:
     x: 0 → 2
     y: 0 → 2-x     ← Variable
     z: 0 → 1
   Resultado: 8/3 ≈ 2.666667

EJERCICIO A6 - Límites variables:
   Sistema: Rectangular
   Función: x*y^2*z
   Límites:
     x: 1 → 2
     y: 0 → 1
     z: 0 → x       ← Variable
   Resultado: 7/6 ≈ 1.166667

EJERCICIO A7 - Límites variables:
   Sistema: Rectangular
   Función: x^2 + y
   Límites:
     x: 0 → 1
     y: 0 → 1
     z: x → 1       ← Límite inferior variable
   Resultado: 5/6 ≈ 0.833333

COORDENADAS CILÍNDRICAS:
   Función: r**2*sin(theta)
   Límites:
     r: 0 → 2
     theta: 0 → pi
     z: 0 → 3

COORDENADAS ESFÉRICAS:
   Función: rho**2*sin(phi)
   Límites:
     rho: 0 → 1
     theta: 0 → 2*pi
     phi: 0 → pi

TIP: Los límites pueden contener expresiones algebraicas
     con las variables de integración anteriores.

═══════════════════════════════════════════════════════════
Para teoremas de Green, Stokes y Divergencia,
usa el botón 'Teoremas Vectoriales'
═══════════════════════════════════════════════════════════
"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, examples)

    def calculate_integral(self):
        try:
            print("\n" + "="*60)
            print("Nueva ejecucion de calculo")
            print("="*60)

            importlib.reload(integral_calculator)
            IntegralCalculator = integral_calculator.IntegralCalculator

            coordinate_system = self.coordinate_system.get().lower()
            func_str = self.function_var.get()

            f = self.parse_function_complete(func_str)

            if coordinate_system in ['cilindrico', 'cilindrico']:
                r_min = self.parse_limit(self.x_min.get())
                r_max = self.parse_limit(self.x_max.get())
                theta_min = self.parse_limit(self.y_min.get())
                theta_max = self.parse_limit(self.y_max.get())
                z_min = self.parse_limit(self.z_min.get())
                z_max = self.parse_limit(self.z_max.get())
                resultado = IntegralCalculator.integral_cylindrical(
                    f, [r_min, r_max], [theta_min, theta_max], [z_min, z_max]
                )

            elif coordinate_system in ['esferico', 'esferico']:
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
            self.result_text.see(1.0)  # Volver al inicio
            
            print("\nCalculo completado exitosamente")
            
        except Exception as e:
            error_msg = f"Error en el calculo:\n\n{str(e)}\n\n"
            error_msg += "Verifica:\n"
            error_msg += "• La sintaxis de la funcion\n"
            error_msg += "• Los limites de integracion\n"
            error_msg += "• Que las variables en limites sean correctas"
            
            messagebox.showerror("Error en el calculo", error_msg)
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()


def main():
    root = tk.Tk()
    app = IntegralApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()