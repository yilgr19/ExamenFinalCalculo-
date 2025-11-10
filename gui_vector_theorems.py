import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import importlib
import re
import os # Añadir para manejar la caché si es necesario

try:
    # Intenta importar el módulo de lógica matemática
    import vector_theorems
    MODULO_DISPONIBLE = True
except ImportError:
    MODULO_DISPONIBLE = False

# =========================================================================
# Función auxiliar para eliminar la caché
# Esto es para ayudar a solucionar el problema de actualización de código
# =========================================================================
def clean_pycache():
    """Elimina la carpeta __pycache__ en el directorio actual."""
    cache_dir = os.path.join(os.path.dirname(__file__), '__pycache__')
    if os.path.exists(cache_dir):
        try:
            import shutil
            shutil.rmtree(cache_dir)
            print("✅ Caché de Python (__pycache__) eliminada exitosamente.")
        except Exception as e:
            print(f"⚠️ Error al intentar eliminar __pycache__: {e}")

# Llama a la limpieza al inicio para asegurar la actualización
clean_pycache()


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
            self.root.geometry("920x780")
            self.root.minsize(880, 680)
        except Exception:
            pass
        
        self.theorem_type = tk.StringVar(value="divergencia")
        
        self.green_P = tk.StringVar(value="")
        self.green_Q = tk.StringVar(value="")
        self.green_tipo = tk.StringVar(value="rectangular")
        self.green_x_min = tk.StringVar(value="0")
        self.green_x_max = tk.StringVar(value="1")
        self.green_y_min = tk.StringVar(value="0")
        self.green_y_max = tk.StringVar(value="1")
        
        self.stokes_Fx = tk.StringVar(value="")
        self.stokes_Fy = tk.StringVar(value="")
        self.stokes_Fz = tk.StringVar(value="")
        self.stokes_x_param = tk.StringVar(value="")
        self.stokes_y_param = tk.StringVar(value="")
        self.stokes_z_param = tk.StringVar(value="")
        self.stokes_u_min = tk.StringVar(value="")
        self.stokes_u_max = tk.StringVar(value="")
        self.stokes_v_min = tk.StringVar(value="")
        self.stokes_v_max = tk.StringVar(value="")
        
        self.div_Fx = tk.StringVar(value="")
        self.div_Fy = tk.StringVar(value="")
        self.div_Fz = tk.StringVar(value="")
        self.div_tipo = tk.StringVar(value="spherical")
        self.div_x_min = tk.StringVar(value="")
        self.div_x_max = tk.StringVar(value="")
        self.div_y_min = tk.StringVar(value="")
        self.div_y_max = tk.StringVar(value="")
        self.div_z_min = tk.StringVar(value="")
        self.div_z_max = tk.StringVar(value="")
        
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
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_columnconfigure(0, weight=1)
        
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        header_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(header_frame, text="Calculadora de Teoremas Vectoriales",
                  font=("Arial", 16, "bold")).grid(row=0, column=0, sticky=tk.W)
        
        controls_frame = ttk.Frame(header_frame)
        controls_frame.grid(row=0, column=1, sticky=tk.E, padx=(10, 0))
        ttk.Label(controls_frame, text="Seleccionar Teorema:").grid(row=0, column=0, sticky=tk.E, padx=(0, 6))
        theorem_combo = ttk.Combobox(controls_frame, textvariable=self.theorem_type,
                                     values=["green", "stokes", "divergencia"],
                                     state="readonly", width=20)
        theorem_combo.grid(row=0, column=1, sticky=tk.E)
        theorem_combo.bind("<<ComboboxSelected>>", self.change_theorem)
        controls_frame.grid_columnconfigure(1, weight=1)
        
        # Guía de sintaxis
        syntax_frame = ttk.LabelFrame(main_frame, text="📖 Guía Rápida de Sintaxis", padding="5")
        syntax_frame.grid(row=1, column=0, pady=(0, 8), sticky='ew')
        
        syntax_text = tk.Text(syntax_frame, height=4, width=100, wrap=tk.WORD,
                              font=("Consolas", 8), bg="#f9f9f9", relief=tk.FLAT)
        syntax_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        syntax_content = """OPERADORES: + - * / ** POTENCIAS: x**2, r^2    RAÍZ: sqrt(x)    CONSTANTES: pi, e
TRIGONOMÉTRICAS: sin(x), cos(y), tan(theta), asin(x), acos(x), atan(x)
HIPERBÓLICAS: sinh(x), cosh(x), tanh(x)    OTRAS: exp(x), log(x), ln(x), abs(x)
VARIABLES COMUNES: x, y, z, r, theta, rho, phi, u, v
EJEMPLOS: -y, 2*x*r**2, sin(theta)*cos(phi), exp(-x**2-y**2), sqrt(x**2+y**2+z**2)"""
        
        syntax_text.insert(1.0, syntax_content)
        syntax_text.config(state=tk.DISABLED)
        
        paned = ttk.Panedwindow(main_frame, orient=tk.VERTICAL)
        paned.grid(row=2, column=0, sticky='nsew')
        main_frame.grid_rowconfigure(2, weight=1)
        
        notebook_container = ttk.Frame(paned)
        notebook_container.grid_columnconfigure(0, weight=1)
        notebook_container.grid_rowconfigure(0, weight=1)
        self.notebook = ttk.Notebook(notebook_container)
        self.notebook.grid(row=0, column=0, sticky='nsew')
        
        self.create_green_tab()
        self.create_stokes_tab()
        self.create_divergence_tab()
        
        button_frame = ttk.Frame(notebook_container)
        button_frame.grid(row=1, column=0, pady=(8, 0))
        ttk.Button(button_frame, text="🧮 Calcular",
                   command=self.calculate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Limpiar",
                   command=self.clear_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📚 Ejemplos",
                   command=self.show_examples).pack(side=tk.LEFT, padx=5)
        
        paned.add(notebook_container, weight=3)
        
        result_container = ttk.Frame(paned)
        paned.add(result_container, weight=2)
        
        result_frame = ttk.LabelFrame(result_container, text="Resultado Detallado", padding="5")
        result_frame.grid(row=0, column=0, sticky='nsew')
        result_container.grid_rowconfigure(0, weight=1)
        result_container.grid_columnconfigure(0, weight=1)
        
        self.result_text = tk.Text(result_frame, height=14, width=100, wrap=tk.WORD,
                                   font=("Consolas", 9), bg="#f5f5f5", state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.result_text.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)
        
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
    
    # =========================================================================
    # 🌟 FUNCIÓN CORREGIDA CRÍTICA (parse_expression) 🌟
    # Esta función transforma la entrada de texto de la GUI en expresiones SymPy.
    # =========================================================================
    def parse_expression(self, expr_str):
        expr_str = str(expr_str).strip()
        if not expr_str:
            return sp.Integer(0)
            
        # 1. Limpieza y estandarización
        expr_str = expr_str.replace('^', '**').replace('π', 'pi')
        
        # 2. Inserción de multiplicación implícita (ej. 2x -> 2*x)
        expr_str = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr_str)
        
        # 3. Definición de Símbolos
        x, y, z = sp.symbols('x y z', real=True)
        u, v = sp.symbols('u v', real=True)
        r, theta = sp.symbols('r theta', real=True, positive=True)
        rho, phi = sp.symbols('rho phi', real=True, positive=True)
        
        # 4. Contexto local de SymPy: CRUCIAL para que SymPy reconozca todo
        locals_dict = {
            'x': x, 'y': y, 'z': z, 'u': u, 'v': v,
            'r': r, 'theta': theta, 'rho': rho, 'phi': phi,
            'pi': sp.pi, 'e': sp.E,
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
            'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
            'sqrt': sp.sqrt, 'exp': sp.exp, 'log': sp.log, 'ln': sp.log, 'abs': sp.Abs
        }
        
        try:
            # 5. Intentar convertir con el contexto completo
            # evaluate=False mejora el manejo de expresiones complejas
            parsed_expr = sp.sympify(expr_str, locals=locals_dict, evaluate=False)
            return sp.simplify(parsed_expr)
            
        except (sp.SympifyError, TypeError) as e:
            # Intenta una conversión numérica simple para límites o constantes puras
            try:
                # Intenta convertir a número puro
                return sp.sympify(float(expr_str))
            except ValueError:
                # Lanza error si no es expresión ni número
                raise ValueError(f"Expresión inválida '{expr_str}'. Revise la sintaxis. Error: {e}")
    # =========================================================================
    # 🌟 FIN DE FUNCIÓN CORREGIDA 🌟
    # =========================================================================
    
    def calculate(self):
        try:
            # Recargar el módulo para garantizar que se usa la versión más reciente
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
    Relaciona una integral de línea cerrada con una integral doble sobre la región

🔵 TEOREMA DE STOKES
    ∮_C F·dr = ∬_S (∇×F)·n dS
    Relaciona una integral de línea cerrada con una integral de superficie

🔴 TEOREMA DE LA DIVERGENCIA (GAUSS)
    ∬_S F·n dS = ∭_V (∇·F) dV
    Relaciona el flujo a través de una superficie cerrada con la divergencia en el volumen

📚 Presiona 'Ejemplos' para ver casos de uso detallados
🧮 Selecciona un teorema arriba y presiona 'Calcular'
"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(1.0, mensaje)
        self.result_text.config(state=tk.DISABLED)
    
    def show_examples(self):
        examples = """EJEMPLOS DE USO

🟢 TEOREMA DE GREEN - Ejemplo Básico:
    Campo: F = (-y, x)
    Componentes: P = -y,  Q = x
    Región: Cuadrado [0,1] × [0,1]
    Tipo: rectangular
    
    Cálculo:
    ∂Q/∂x - ∂P/∂y = ∂(x)/∂x - ∂(-y)/∂y = 1 - (-1) = 2
    Integral: ∬ 2 dA = 2 × (área) = 2 × 1 = 2
    
    Resultado: 2

🔵 TEOREMA DE STOKES - Ejemplo:
    Campo: F = (y, -x, z)
    Componentes: Fx = y, Fy = -x, Fz = z
    
    Superficie: Paraboloide z = 1 - x² - y²
    Parametrización: 
      x(u,v) = u*cos(v)
      y(u,v) = u*sin(v)
      z(u,v) = 1 - u**2
    
    Límites: u ∈ [0, 1], v ∈ [0, 2*pi]
    
    Rotacional: ∇×F = (0, 0, -2)
    El teorema calcula el flujo del rotacional a través de la superficie

🔴 TEOREMA DIVERGENCIA - Ejemplo Esférico:
    Campo: F = (rho**2*sin(phi)*cos(theta), rho**2*sin(phi)*sin(theta), rho**2*cos(phi))
    Componentes: 
      Fx = rho**2*sin(phi)*cos(theta)
      Fy = rho**2*sin(phi)*sin(theta)
      Fz = rho**2*cos(phi)
    
    Sistema: spherical (esférico)
    Región: Anillo Esférico (Shell)
    Límites: ρ ∈ [1,2], θ ∈ [0,2*pi], φ ∈ [0,pi]
    
    Divergencia: ∇·F = 4*rho (Calculado internamente)
    Resultado: 60*pi ≈ 188.5

CONSEJOS:
• Usa multiplicación explícita: 2*x en lugar de 2x
• Potencias: x**2 o x^2
• Constantes: pi para π, e para número de Euler
• Funciones: sqrt(x), sin(x), cos(x), exp(x), log(x)
• Variables de parametrización: u, v para superficies
• Coordenadas: x,y,z (rectangular), r,theta,z (cilíndrico), rho,theta,phi (esférico)
"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, examples)
        self.result_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = VectorTheoremsApp(root)
    root.mainloop()