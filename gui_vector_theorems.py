"""
GUI para Teoremas Vectoriales (Green, Stokes, Divergencia)
VERSIÓN MEJORADA - Maneja campos complejos como 2*x*r**2
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import importlib
import re

try:
    import vector_theorems
    MODULO_DISPONIBLE = True
except ImportError:
    MODULO_DISPONIBLE = False


class VectorTheoremsApp:
    def __init__(self, root):
        self.root = root
        if not hasattr(root, 'title'):
            raise ValueError("root debe ser una ventana Tk válida")
            
        self.root.title("🧮 Teoremas Vectoriales")
        
        if not MODULO_DISPONIBLE:
            self.mostrar_error_inicial()
            return
        
        try:
            self.root.geometry("900x1100")
        except:
            pass
        
        self.theorem_type = tk.StringVar(value="divergencia")
        
        self.green_P = tk.StringVar(value="-y")
        self.green_Q = tk.StringVar(value="x")
        self.green_tipo = tk.StringVar(value="rectangular")
        self.green_x_min = tk.StringVar(value="0")
        self.green_x_max = tk.StringVar(value="1")
        self.green_y_min = tk.StringVar(value="0")
        self.green_y_max = tk.StringVar(value="1")
        
        self.stokes_Fx = tk.StringVar(value="y")
        self.stokes_Fy = tk.StringVar(value="-x")
        self.stokes_Fz = tk.StringVar(value="z")
        self.stokes_x_param = tk.StringVar(value="u*cos(v)")
        self.stokes_y_param = tk.StringVar(value="u*sin(v)")
        self.stokes_z_param = tk.StringVar(value="1-u**2")
        self.stokes_u_min = tk.StringVar(value="0")
        self.stokes_u_max = tk.StringVar(value="1")
        self.stokes_v_min = tk.StringVar(value="0")
        self.stokes_v_max = tk.StringVar(value="2*pi")
        
        self.div_Fx = tk.StringVar(value="2*x*r**2")
        self.div_Fy = tk.StringVar(value="2*y*r**2")
        self.div_Fz = tk.StringVar(value="2*z*r**2")
        self.div_tipo = tk.StringVar(value="spherical")
        self.div_x_min = tk.StringVar(value="0")
        self.div_x_max = tk.StringVar(value="1")
        self.div_y_min = tk.StringVar(value="0")
        self.div_y_max = tk.StringVar(value="2*pi")
        self.div_z_min = tk.StringVar(value="0")
        self.div_z_max = tk.StringVar(value="pi")
        
        self.create_widgets()
    
    def mostrar_error_inicial(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(frame, text="⚠️ ERROR: Módulo no encontrado",
                  font=("Arial", 14, "bold"), foreground="red").pack(pady=20)
        ttk.Label(frame, text="No se pudo cargar 'vector_theorems.py'",
                  font=("Arial", 11)).pack(pady=10)
        ttk.Button(frame, text="Cerrar", command=self.root.destroy).pack(pady=20)
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Calculadora de Teoremas Vectoriales",
                  font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(main_frame, text="Seleccionar Teorema:").grid(row=1, column=0, sticky=tk.W, pady=5)
        theorem_combo = ttk.Combobox(main_frame, textvariable=self.theorem_type,
                                    values=["green", "stokes", "divergencia"],
                                    state="readonly", width=25)
        theorem_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        theorem_combo.bind("<<ComboboxSelected>>", self.change_theorem)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, columnspan=2, pady=10, sticky='nsew')
        
        self.create_green_tab()
        self.create_stokes_tab()
        self.create_divergence_tab()
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        ttk.Button(button_frame, text="🧮 Calcular",
                  command=self.calculate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Limpiar",
                  command=self.clear_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📚 Ejemplos",
                  command=self.show_examples).pack(side=tk.LEFT, padx=5)
        
        result_frame = ttk.LabelFrame(main_frame, text="Resultado Detallado", padding="5")
        result_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky='nsew')
        
        self.result_text = tk.Text(result_frame, height=20, width=100, wrap=tk.WORD,
                                    font=("Consolas", 9), bg="#f5f5f5", state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.result_text.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        self.show_welcome_message()
    
    def create_green_tab(self):
        green_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(green_frame, text="Teorema de Green")
        
        ttk.Label(green_frame, text="Campo Vectorial F = (P, Q)",
                 font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(green_frame, text="P(x,y) =").grid(row=1, column=0, sticky=tk.E, padx=5)
        ttk.Entry(green_frame, textvariable=self.green_P, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(green_frame, text="Q(x,y) =").grid(row=2, column=0, sticky=tk.E, padx=5)
        ttk.Entry(green_frame, textvariable=self.green_Q, width=30).grid(row=2, column=1, pady=5)
        
        ttk.Label(green_frame, text="Tipo de región:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=10)
        ttk.Combobox(green_frame, textvariable=self.green_tipo,
                    values=["rectangular", "polar"], state="readonly", width=27).grid(row=3, column=1)
        
        limits_frame = ttk.LabelFrame(green_frame, text="Límites", padding="5")
        limits_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky='ew')
        
        ttk.Label(limits_frame, text="x mín:").grid(row=0, column=0, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.green_x_min, width=10).grid(row=0, column=1, padx=5)
        ttk.Label(limits_frame, text="x máx:").grid(row=0, column=2, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.green_x_max, width=10).grid(row=0, column=3, padx=5)
        
        ttk.Label(limits_frame, text="y mín:").grid(row=1, column=0, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.green_y_min, width=10).grid(row=1, column=1, padx=5)
        ttk.Label(limits_frame, text="y máx:").grid(row=1, column=2, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.green_y_max, width=10).grid(row=1, column=3, padx=5)
    
    def create_stokes_tab(self):
        stokes_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(stokes_frame, text="Teorema de Stokes")
        
        ttk.Label(stokes_frame, text="Campo Vectorial F = (Fx, Fy, Fz)",
                 font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(stokes_frame, text="Fx(x,y,z) =").grid(row=1, column=0, sticky=tk.E, padx=5)
        ttk.Entry(stokes_frame, textvariable=self.stokes_Fx, width=30).grid(row=1, column=1, pady=3)
        
        ttk.Label(stokes_frame, text="Fy(x,y,z) =").grid(row=2, column=0, sticky=tk.E, padx=5)
        ttk.Entry(stokes_frame, textvariable=self.stokes_Fy, width=30).grid(row=2, column=1, pady=3)
        
        ttk.Label(stokes_frame, text="Fz(x,y,z) =").grid(row=3, column=0, sticky=tk.E, padx=5)
        ttk.Entry(stokes_frame, textvariable=self.stokes_Fz, width=30).grid(row=3, column=1, pady=3)
        
        param_frame = ttk.LabelFrame(stokes_frame, text="Parametrización r(u,v)", padding="5")
        param_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky='ew')
        
        ttk.Label(param_frame, text="x(u,v) =").grid(row=0, column=0, sticky=tk.E, padx=5)
        ttk.Entry(param_frame, textvariable=self.stokes_x_param, width=25).grid(row=0, column=1, pady=3)
        
        ttk.Label(param_frame, text="y(u,v) =").grid(row=1, column=0, sticky=tk.E, padx=5)
        ttk.Entry(param_frame, textvariable=self.stokes_y_param, width=25).grid(row=1, column=1, pady=3)
        
        ttk.Label(param_frame, text="z(u,v) =").grid(row=2, column=0, sticky=tk.E, padx=5)
        ttk.Entry(param_frame, textvariable=self.stokes_z_param, width=25).grid(row=2, column=1, pady=3)
        
        limits_frame = ttk.LabelFrame(stokes_frame, text="Límites de Parámetros", padding="5")
        limits_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky='ew')
        
        ttk.Label(limits_frame, text="u mín:").grid(row=0, column=0, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.stokes_u_min, width=10).grid(row=0, column=1, padx=5)
        ttk.Label(limits_frame, text="u máx:").grid(row=0, column=2, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.stokes_u_max, width=10).grid(row=0, column=3, padx=5)
        
        ttk.Label(limits_frame, text="v mín:").grid(row=1, column=0, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.stokes_v_min, width=10).grid(row=1, column=1, padx=5)
        ttk.Label(limits_frame, text="v máx:").grid(row=1, column=2, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.stokes_v_max, width=10).grid(row=1, column=3, padx=5)
    
    def create_divergence_tab(self):
        div_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(div_frame, text="Teorema Divergencia")
        
        ttk.Label(div_frame, text="Campo Vectorial F = (Fx, Fy, Fz)",
                 font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(div_frame, text="Fx(x,y,z) =").grid(row=1, column=0, sticky=tk.E, padx=5)
        ttk.Entry(div_frame, textvariable=self.div_Fx, width=30).grid(row=1, column=1, pady=3)
        
        ttk.Label(div_frame, text="Fy(x,y,z) =").grid(row=2, column=0, sticky=tk.E, padx=5)
        ttk.Entry(div_frame, textvariable=self.div_Fy, width=30).grid(row=2, column=1, pady=3)
        
        ttk.Label(div_frame, text="Fz(x,y,z) =").grid(row=3, column=0, sticky=tk.E, padx=5)
        ttk.Entry(div_frame, textvariable=self.div_Fz, width=30).grid(row=3, column=1, pady=3)
        
        ttk.Label(div_frame, text="Sistema:").grid(row=4, column=0, sticky=tk.E, padx=5, pady=10)
        ttk.Combobox(div_frame, textvariable=self.div_tipo,
                    values=["rectangular", "cylindrical", "spherical"],
                    state="readonly", width=27).grid(row=4, column=1)
        
        limits_frame = ttk.LabelFrame(div_frame, text="Límites", padding="5")
        limits_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky='ew')
        
        ttk.Label(limits_frame, text="x/r/ρ mín:").grid(row=0, column=0, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.div_x_min, width=10).grid(row=0, column=1, padx=5)
        ttk.Label(limits_frame, text="máx:").grid(row=0, column=2, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.div_x_max, width=10).grid(row=0, column=3, padx=5)
        
        ttk.Label(limits_frame, text="y/θ mín:").grid(row=1, column=0, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.div_y_min, width=10).grid(row=1, column=1, padx=5)
        ttk.Label(limits_frame, text="máx:").grid(row=1, column=2, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.div_y_max, width=10).grid(row=1, column=3, padx=5)
        
        ttk.Label(limits_frame, text="z/φ mín:").grid(row=2, column=0, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.div_z_min, width=10).grid(row=2, column=1, padx=5)
        ttk.Label(limits_frame, text="máx:").grid(row=2, column=2, sticky=tk.E, padx=5)
        ttk.Entry(limits_frame, textvariable=self.div_z_max, width=10).grid(row=2, column=3, padx=5)
    
    def change_theorem(self, event=None):
        theorem = self.theorem_type.get()
        if theorem == "green":
            self.notebook.select(0)
        elif theorem == "stokes":
            self.notebook.select(1)
        else:
            self.notebook.select(2)
    
    def parse_expression(self, expr_str):
        expr_str = str(expr_str).replace('^', '**').replace('π', 'pi')
        expr_str = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr_str)
        
        x, y, z = sp.symbols('x y z', real=True)
        u, v = sp.symbols('u v', real=True)
        r, theta = sp.symbols('r theta', real=True, positive=True)
        rho, phi = sp.symbols('rho phi', real=True, positive=True)
        
        locals_dict = {
            'x': x, 'y': y, 'z': z, 'u': u, 'v': v,
            'r': r, 'theta': theta, 'rho': rho, 'phi': phi,
            'pi': sp.pi, 'e': sp.E,
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'sqrt': sp.sqrt, 'exp': sp.exp, 'log': sp.log
        }
        
        return sp.sympify(expr_str, locals=locals_dict)
    
    def calculate(self):
        try:
            importlib.reload(vector_theorems)
            VectorTheorems = vector_theorems.VectorTheorems
            
            theorem = self.theorem_type.get()
            
            if theorem == "green":
                self.calculate_green(VectorTheorems)
            elif theorem == "stokes":
                self.calculate_stokes(VectorTheorems)
            else:
                self.calculate_divergence(VectorTheorems)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo:\n\n{str(e)}")
    
    def calculate_green(self, VectorTheorems):
        P = self.parse_expression(self.green_P.get())
        Q = self.parse_expression(self.green_Q.get())
        tipo = self.green_tipo.get()
        
        if tipo == "polar":
            bounds = {
                'r': [self.parse_expression(self.green_x_min.get()),
                     self.parse_expression(self.green_x_max.get())],
                'theta': [self.parse_expression(self.green_y_min.get()),
                         self.parse_expression(self.green_y_max.get())]
            }
        else:
            bounds = {
                'x': [self.parse_expression(self.green_x_min.get()),
                     self.parse_expression(self.green_x_max.get())],
                'y': [self.parse_expression(self.green_y_min.get()),
                     self.parse_expression(self.green_y_max.get())]
            }
        
        resultado = VectorTheorems.green_theorem(P, Q, bounds, tipo)
        self.display_result(resultado["pasos"])
    
    def calculate_stokes(self, VectorTheorems):
        Fx = self.parse_expression(self.stokes_Fx.get())
        Fy = self.parse_expression(self.stokes_Fy.get())
        Fz = self.parse_expression(self.stokes_Fz.get())
        
        x_param = self.parse_expression(self.stokes_x_param.get())
        y_param = self.parse_expression(self.stokes_y_param.get())
        z_param = self.parse_expression(self.stokes_z_param.get())
        
        bounds = {
            'u': [self.parse_expression(self.stokes_u_min.get()),
                 self.parse_expression(self.stokes_u_max.get())],
            'v': [self.parse_expression(self.stokes_v_min.get()),
                 self.parse_expression(self.stokes_v_max.get())]
        }
        
        resultado = VectorTheorems.stokes_theorem([Fx, Fy, Fz], [x_param, y_param, z_param], bounds)
        self.display_result(resultado["pasos"])
    
    def calculate_divergence(self, VectorTheorems):
        Fx = self.parse_expression(self.div_Fx.get())
        Fy = self.parse_expression(self.div_Fy.get())
        Fz = self.parse_expression(self.div_Fz.get())
        tipo = self.div_tipo.get()
        
        if tipo == "spherical":
            bounds = {
                'rho': [self.parse_expression(self.div_x_min.get()),
                       self.parse_expression(self.div_x_max.get())],
                'theta': [self.parse_expression(self.div_y_min.get()),
                         self.parse_expression(self.div_y_max.get())],
                'phi': [self.parse_expression(self.div_z_min.get()),
                       self.parse_expression(self.div_z_max.get())]
            }
        elif tipo == "cylindrical":
            bounds = {
                'r': [self.parse_expression(self.div_x_min.get()),
                     self.parse_expression(self.div_x_max.get())],
                'theta': [self.parse_expression(self.div_y_min.get()),
                         self.parse_expression(self.div_y_max.get())],
                'z': [self.parse_expression(self.div_z_min.get()),
                     self.parse_expression(self.div_z_max.get())]
            }
        else:
            bounds = {
                'x': [self.parse_expression(self.div_x_min.get()),
                     self.parse_expression(self.div_x_max.get())],
                'y': [self.parse_expression(self.div_y_min.get()),
                     self.parse_expression(self.div_y_max.get())],
                'z': [self.parse_expression(self.div_z_min.get()),
                     self.parse_expression(self.div_z_max.get())]
            }
        
        resultado = VectorTheorems.divergence_theorem([Fx, Fy, Fz], tipo, bounds)
        self.display_result(resultado["pasos"])
    
    def display_result(self, pasos):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, pasos)
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)
    
    def clear_results(self):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.show_welcome_message()
        self.result_text.config(state=tk.DISABLED)
    
    def show_welcome_message(self):
        mensaje = """Bienvenido a la Calculadora de Teoremas Vectoriales

TEOREMAS DISPONIBLES:

🟢 TEOREMA DE GREEN
   ∮_C (P dx + Q dy) = ∬_R (∂Q/∂x - ∂P/∂y) dA

🔵 TEOREMA DE STOKES
   ∮_C F·dr = ∬_S (∇×F)·n dS

🔴 TEOREMA DE LA DIVERGENCIA (GAUSS)
   ∬_S F·n dS = ∭_V (∇·F) dV

📚 Presiona 'Ejemplos' para ver casos de uso
🧮 Selecciona un teorema y presiona 'Calcular'
"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(1.0, mensaje)
        self.result_text.config(state=tk.DISABLED)
    
    def show_examples(self):
        examples = """EJEMPLOS DE USO

🟢 TEOREMA DE GREEN - Ejemplo:
    P = -y,  Q = x
    Región: [0,1] × [0,1]
    Resultado: 2

🔵 TEOREMA DE STOKES - Ejemplo:
    F = (y, -x, z)
    Superficie: z = 1 - x² - y²
    Parametrización: x=u·cos(v), y=u·sin(v), z=1-u²
    Límites: u∈[0,1], v∈[0,2π]

🔴 TEOREMA DIVERGENCIA - Ejemplo (Campo radial):
    F = (2xr², 2yr², 2zr²)  donde r = √(x²+y²+z²)
    Sistema: esférico
    Límites: ρ∈[0,1], θ∈[0,2π], φ∈[0,π]
    Divergencia: ∇·F = 5ρ²
    Resultado: 4π/5 × (5) = 4π
"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, examples)
        self.result_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = VectorTheoremsApp(root)
    root.mainloop()