import sympy as sp
import math
import sys

def calcular_integral_cilindrica():
    # Configurar codificación
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Definir símbolos
    r, theta, z = sp.symbols('r theta z', real=True)
    pi = sp.pi
    
    # Límites de integración
    r_min, r_max = 2, 3
    theta_min, theta_max = pi/4, pi/2
    z_min, z_max = 1, 2
    
    # Paso 1 - Integral en z
    f_z = r**3 * sp.cos(theta)
    integral_z = f_z * (z_max - z_min)
    print("Paso 1 - Integral en z:")
    print(f"Integral de {f_z} de {z_min} a {z_max}: {integral_z}")
    
    # Paso 2 - Integral en θ
    integral_theta = sp.integrate(integral_z, (theta, theta_min, theta_max))
    print("\nPaso 2 - Integral en θ:")
    print(f"Integral de {integral_z} de {theta_min} a {theta_max}: {integral_theta}")
    
    # Paso 3 - Integral en r
    integral_r = sp.integrate(integral_theta, (r, r_min, r_max))
    print("\nPaso 3 - Integral en r:")
    print(f"Integral de {integral_theta} de {r_min} a {r_max}: {integral_r}")
    
    # Evaluación numérica
    resultado_simbolico = integral_r
    resultado_numerico = float(sp.N(resultado_simbolico, 15))
    
    print("\nResultados:")
    print(f"Resultado simbólico: {resultado_simbolico}")
    print(f"Resultado numérico: {resultado_numerico}")
    
    # Cálculo manual detallado
    print("\nCálculo manual:")
    
    # Componente z
    z_component = z_max - z_min
    print(f"Componente z: {z_component}")
    
    # Componente theta
    theta_component = float(sp.sin(theta_max) - sp.sin(theta_min))
    print(f"Componente θ (sin(pi/2) - sin(pi/4)): {theta_component}")
    
    # Componente r
    r_component = (r_max**4 - r_min**4) / 4
    print(f"Componente r ((3^4 - 2^4) / 4): {r_component}")
    
    # Cálculo final
    factor = (2 - sp.sqrt(2)) / 2
    resultado_manual = 65 * factor / 8
    print(f"\nFactor (2 - raiz(2)) / 2: {factor}")
    print(f"Resultado manual: {resultado_manual}")
    print(f"Resultado manual (numerico): {float(resultado_manual)}")

def main():
    calcular_integral_cilindrica()

if __name__ == "__main__":
    main()
