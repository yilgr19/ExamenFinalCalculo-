import math
import sympy as sp
import sys

def calcular_integral_manual():
    # Configurar codificación de salida
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Definir valores
    r_min = 2
    r_max = 3
    theta_min = math.pi/4
    theta_max = math.pi/2
    z_min = 1
    z_max = 2

    # Componentes del cálculo
    z_component = z_max - z_min  # 2 - 1 = 1
    
    # Componente theta: sin(π/2) - sin(π/4)
    theta_component = math.sin(theta_max) - math.sin(theta_min)
    
    # Componente r: (3³ - 2³) / 3
    r_component = (r_max**3 - r_min**3) / 3
    
    # Cálculo simbólico para mayor precisión
    r, theta, z = sp.symbols('r theta z')
    
    # Cálculo simbólico de la integral
    z_integral = z_max - z_min
    theta_integral = sp.sin(theta_max) - sp.sin(theta_min)
    r_integral = (sp.sympify(r_max)**3 - sp.sympify(r_min)**3) / 3
    
    # Resultado final
    resultado_numerico = z_component * theta_component * r_component
    resultado_simbolico = z_integral * theta_integral * r_integral

    # Imprimir con manejo de codificación
    print("Calculo detallado de la integral:")
    print(f"Componente z (intervalo): {z_component}")
    print(f"Componente theta (sin(pi/2) - sin(pi/4)): {theta_component}")
    print(f"Componente r ((3^3 - 2^3) / 3): {r_component}")
    print("\nResultados:")
    print(f"Resultado numerico: {resultado_numerico}")
    print(f"Resultado simbolico: {resultado_simbolico}")
    print(f"Resultado simbolico evaluado: {float(resultado_simbolico)}")

def main():
    calcular_integral_manual()

if __name__ == "__main__":
    main()
