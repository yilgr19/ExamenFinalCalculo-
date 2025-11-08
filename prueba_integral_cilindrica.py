import sympy as sp
import re
import sys

def parse_function(func_str):
    """Parsear función con manejo detallado de símbolos y funciones"""
    print(f"DEBUG: Parseando función original: {func_str}")
    
    # Definir símbolos
    r, theta, z = sp.symbols('r theta z', real=True)
    pi = sp.pi
    
    # Reemplazar potencias con ^
    func_str = func_str.replace('^', '**')
    
    # Preservar funciones trigonométricas
    func_str = re.sub(r'\b(sin|cos|tan)\(', r'\1(', func_str)
    
    # Agregar multiplicación implícita
    func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)
    func_str = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_str)
    
    print(f"DEBUG: Función después de preprocesamiento: {func_str}")
    
    # Diccionario de locales para evaluación segura
    locals_dict = {
        'r': r, 'theta': theta, 'z': z, 
        'pi': pi, 
        'sin': sp.sin, 
        'cos': sp.cos, 
        'tan': sp.tan
    }
    
    try:
        # Convertir a expresión sympy
        f = sp.sympify(func_str, locals=locals_dict)
        print(f"DEBUG: Función parseada: {f}")
        return f
    except Exception as e:
        print(f"ERROR al parsear función: {e}")
        raise

def main():
    # Configurar codificación
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Ejemplo de función de integral cilíndrica
    funcion = "r**2 * cos(theta)"
    
    # Parsear la función
    f = parse_function(funcion)
    
    # Límites de integración
    r_min, r_max = 2, 3
    theta_min, theta_max = sp.pi/4, sp.pi/2
    z_min, z_max = 1, 2
    
    # Imprimir detalles
    print("\nDetalles de la integral:")
    print(f"Función: {f}")
    print("Límites:")
    print(f"r: {r_min} a {r_max}")
    print(f"θ: {theta_min} a {theta_max}")
    print(f"z: {z_min} a {z_max}")

if __name__ == "__main__":
    main()
