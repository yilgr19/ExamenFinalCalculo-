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
    
    print("Detalles de la integral:")
    print(f"Función: {f}")
    print("Límites:")
    print(f"r: {r_min} a {r_max}")
    print(f"θ: {theta_min} a {theta_max}")
    print(f"z: {z_min} a {z_max}")
    
    # Integración paso a paso
    print("\nPaso 1: Integración respecto a z")
    integral_z = f * (z_max - z_min)
    print(f"Integral z: {integral_z}")
    
    # Paso 2: Integración respecto a theta
    print("\nPaso 2: Integración respecto a θ")
    integral_theta = sp.integrate(integral_z * sp.cos(theta), (theta, theta_min, theta_max))
    print(f"Integral θ: {integral_theta}")
    
    # Paso 3: Integración respecto a r
    print("\nPaso 3: Integración respecto a r")
    resultado_final = sp.integrate(integral_theta * r, (r, r_min, r_max))
    print(f"Resultado final simbólico: {resultado_final}")
    
    # Evaluación numérica
    resultado_numerico = float(sp.N(resultado_final, 15))
    print(f"\nResultado numérico: {resultado_numerico}")
    
    # Cálculo manual detallado
    print("\nCálculo manual de componentes:")
    
    # Componente z
    z_component = z_max - z_min
    print(f"Componente z (intervalo): {z_component}")
    
    # Componente theta
    theta_component = float(sp.sin(theta_max) - sp.sin(theta_min))
    print(f"Componente θ (sin(θ_max) - sin(θ_min)): {theta_component}")
    
    # Componente r
    r_component = (r_max**3 - r_min**3) / 3
    print(f"Componente r ((r_max³ - r_min³) / 3): {r_component}")
    
    # Cálculo manual multiplicativo
    resultado_manual = z_component * theta_component * r_component
    print(f"\nResultado manual (z * θ * r): {resultado_manual}")
    
    # Cálculo con factor Jacobiano
    resultado_jacobiano = resultado_manual * r_max**2
    print(f"Resultado con factor Jacobiano r²: {resultado_jacobiano}")

def main():
    integral_cilindrica_detallada()

if __name__ == "__main__":
    main()
