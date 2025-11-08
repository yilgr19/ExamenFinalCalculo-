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
        resultado_label = ttk.Label(main_frame, textvariable=self.result_var, wraplength=500, justify=tk.LEFT, font=("Courier", 10))
        resultado_label.grid(row=5, column=0, columnspan=2, pady=10, sticky='w')

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
            # Importaciones necesarias
            import sympy as sp
            import re
            import traceback
            import sys
            
            # Configurar codificación
            sys.stdout.reconfigure(encoding='utf-8')
            
            # Definir símbolos matemáticos
            pi = sp.pi
            
            # Crear símbolos de manera más explícita
            x, y, z, r, theta, rho = sp.symbols('x y z r theta rho', real=True, positive=True)
            
            # Función de depuración
            def debug_print(message):
                try:
                    print(message)
                except Exception:
                    print(message.encode('ascii', 'ignore').decode('ascii'))
            
            # Parsear la función con símbolos matemáticos
            def parse_function(func_str):
                # Preprocesamiento de la función
                debug_print(f"DEBUG: Parseando función original: {func_str}")
                
                # Reemplazar potencias con ^
                func_str = func_str.replace('^', '**')
                
                # Preservar funciones trigonométricas
                func_str = re.sub(r'\b(sin|cos|tan)\(', r'\1(', func_str)
                
                # Agregar multiplicación implícita
                func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)
                func_str = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_str)
                
                debug_print(f"DEBUG: Función después de preprocesamiento: {func_str}")
                
                # Diccionario de locales para evaluación segura
                locals_dict = {
                    'x': x, 'y': y, 'z': z, 
                    'r': r, 'theta': theta, 'rho': rho,
                    'pi': pi, 
                    'sin': sp.sin, 
                    'cos': sp.cos, 
                    'tan': sp.tan
                }
                
                try:
                    # Convertir a expresión sympy
                    f = sp.sympify(func_str, locals=locals_dict)
                    debug_print(f"DEBUG: Función parseada: {f}")
                    return f
                except Exception as e:
                    debug_print(f"Error al parsear función: {e}")
                    raise
            
            # Parsear límites
            def parse_limit(limit_str, symbol=None):
                # Preprocesamiento de límites
                debug_print(f"DEBUG: Parseando límite original: {limit_str}")
                
                # Reemplazar pi por su valor simbólico
                limit_str = limit_str.replace('π', 'pi')
                
                # Reemplazar potencias con ^
                limit_str = limit_str.replace('^', '**')
                
                debug_print(f"DEBUG: Límite después de reemplazos: {limit_str}")
                
                # Diccionario de locales para evaluación segura
                locals_dict = {'pi': pi}
                
                try:
                    # Convertir a valor numérico o simbólico
                    limit = sp.sympify(limit_str, locals=locals_dict)
                    debug_print(f"DEBUG: Límite parseado: {limit}")
                    return limit
                except Exception as e:
                    debug_print(f"Error al parsear límite: {e}")
                    raise
            
            # Obtener valores de la interfaz
            coordinate_system = self.coordinate_system.get().lower()
            func_str = self.function_var.get()
            
            # Validar sistema de coordenadas
            valid_systems = ['rectangular', 'cilindrico', 'cilíndrico', 'esférico', 'esf', 'esferico']
            if coordinate_system not in valid_systems:
                raise ValueError(f"Sistema de coordenadas no válido: {coordinate_system}")
            
            # Normalizar sistema de coordenadas
            if coordinate_system in ['cilindrico', 'cilíndrico']:
                coordinate_system = 'cilindrico'
            elif coordinate_system in ['esférico', 'esf', 'esferico']:
                coordinate_system = 'esférico'
            
            # Parsear función
            f = parse_function(func_str)
            
            # Parsear límites según el sistema de coordenadas
            if coordinate_system == 'rectangular':
                # Parsear límites para coordenadas rectangulares
                x_min = parse_limit(self.x_min.get())
                x_max = parse_limit(self.x_max.get())
                y_min = parse_limit(self.y_min.get())
                y_max = parse_limit(self.y_max.get())
                z_min = parse_limit(self.z_min.get())
                z_max = parse_limit(self.z_max.get())
                
                # Calcular integral rectangular
                resultado = IntegralCalculator.integral_rectangular(
                    f, [x_min, x_max], [y_min, y_max], [z_min, z_max]
                )
            
            elif coordinate_system == 'cilindrico':
                # Parsear límites para coordenadas cilíndricas
                r_min = parse_limit(self.x_min.get())
                r_max = parse_limit(self.x_max.get())
                theta_min = parse_limit(self.y_min.get())
                theta_max = parse_limit(self.y_max.get())
                z_min = parse_limit(self.z_min.get())
                z_max = parse_limit(self.z_max.get())
                
                # Calcular integral cilíndrica
                resultado = IntegralCalculator.integral_cylindrical(
                    f, [r_min, r_max], [theta_min, theta_max], [z_min, z_max]
                )
            
            elif coordinate_system == 'esférico':
                # Parsear límites para coordenadas esféricas
                rho_min = parse_limit(self.x_min.get())
                rho_max = parse_limit(self.x_max.get())
                theta_min = parse_limit(self.y_min.get())
                theta_max = parse_limit(self.y_max.get())
                phi_min = parse_limit(self.z_min.get())
                phi_max = parse_limit(self.z_max.get())
                
                # Calcular integral esférica
                resultado = IntegralCalculator.integral_spherical(
                    f, [rho_min, rho_max], [theta_min, theta_max], [phi_min, phi_max]
                )
            
            else:
                raise ValueError("Sistema de coordenadas no válido")
            
            # Mostrar resultados
            resultado_manual = resultado['resultado_manual']
            resultado_simbolico = resultado['resultado_simbolico']
            resultado_simbolico_evaluado = resultado['resultado_simbolico_evaluado']
            pasos = resultado['pasos']
            
            # Limpiar pantalla de resultados
            self.result_var.set("") # Clear the StringVar
            self.result_var.set(f"""Procedimiento paso a paso:
{pasos}

Límites:
r: {self.x_min.get()} → {self.x_max.get()}
θ: {self.y_min.get()} → {self.y_max.get()}
z: {self.z_min.get()} → {self.z_max.get()}

Resultado de la integral:
Valor numérico: {resultado_manual}
Valor simbólico: {resultado_simbolico}
Valor simbólico evaluado: {resultado_simbolico_evaluado}

∫ f(r,θ,z) dz dθ dr = {resultado_simbolico} = {resultado_manual}""")
        
        except Exception as e:
            # Mostrar mensaje de error
            import traceback
            error_msg = f"Error: {str(e)}\n\nDetalles:\n{traceback.format_exc()}"
            
            # Mostrar error en la interfaz
            self.result_var.set(f"Error: {error_msg}")
            
            # Opcional: mostrar mensaje de error en una ventana emergente
            messagebox.showerror("Error en el cálculo", error_msg)

def main():
    root = tk.Tk()
    app = IntegralApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
