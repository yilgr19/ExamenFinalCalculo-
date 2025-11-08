import sympy as sp
import math
import sys

def integral_cilindrica_detallada():
    # Configurar codificación
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Definir símbolos
    r, theta, z = sp.symbols('r theta z', real=True)
    pi = sp.pi
    
    # Función a integrar
    f = r**2 * sp.cos(theta)
    
    # Límites de integración
    r_min, r_max = 2, 3
    theta_min, theta_max = pi/4, pi/2
    z_min, z_max = 1, 2
    
    # Integración paso a paso
    print("Integración paso a paso:")
    
    # Paso 1: Integrar respecto a z
    integral_z = sp.integrate(f, (z, z_min, z_max))
    print(f"1. Integral respecto a z: {integral_z}")
    
    # Paso 2: Integrar respecto a theta
    integral_theta = sp.integrate(integral_z, (theta, theta_min, theta_max))
    print(f"2. Integral respecto a theta: {integral_theta}")
    
    # Paso 3: Integrar respecto a r
    resultado_final = sp.integrate(integral_theta, (r, r_min, r_max))
    print(f"3. Integral respecto a r: {resultado_final}")
    
    # Evaluación numérica
    resultado_numerico = float(sp.N(resultado_final, 15))
    print(f"\nResultado numérico: {resultado_numerico}")
    
    # Cálculo manual de componentes
    z_component = z_max - z_min
    theta_component = float(sp.sin(theta_max) - sp.sin(theta_min))
    r_component = (r_max**3 - r_min**3) / 3
    
    print("\nDesglose de componentes:")
    print(f"Componente z: {z_component}")
    print(f"Componente theta: {theta_component}")
    print(f"Componente r: {r_component}")
    
    # Cálculo manual multiplicativo
    resultado_manual = z_component * theta_component * r_component
    print(f"\nResultado manual: {resultado_manual}")

def main():
    integral_cilindrica_detallada()

if __name__ == "__main__":
    main()
