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
    
    # Función a integrar
    f = r**2 * sp.cos(theta)
    
    print("Detalles de la integral:")
    print(f"Función: {f}")
    print("Límites:")
    print(f"r: {r_min} a {r_max}")
    print(f"θ: {theta_min} a {theta_max}")
    print(f"z: {z_min} a {z_max}")
    
    # Paso 1: Integral respecto a z
    integral_z = f * (z_max - z_min)
    print("\nPaso 1 - Integral respecto a z:")
    print(f"∫{z_min}^{z_max} {f} dz = {integral_z}")
    
    # Paso 2: Integral respecto a θ
    integral_theta = sp.integrate(integral_z * sp.cos(theta), (theta, theta_min, theta_max))
    print("\nPaso 2 - Integral respecto a θ:")
    print(f"∫{theta_min}^{theta_max} {integral_z} * cos(θ) dθ = {integral_theta}")
    
    # Paso 3: Integral respecto a r
    integral_r = sp.integrate(integral_theta * r, (r, r_min, r_max))
    print("\nPaso 3 - Integral respecto a r:")
    print(f"∫{r_min}^{r_max} {integral_theta} * r dr = {integral_r}")
    
    # Evaluación numérica
    resultado_simbolico = integral_r
    resultado_numerico = float(sp.N(resultado_simbolico, 15))
    
    print("\nResultados:")
    print(f"Resultado simbólico: {resultado_simbolico}")
    print(f"Resultado numérico: {resultado_numerico}")
    
    # Desglose de componentes
    print("\nDesglose de componentes:")
    
    # Componente z
    z_component = z_max - z_min
    print(f"Componente z (intervalo): {z_component}")
    print(f"  Límites z: {z_min} → {z_max}")
    print(f"  Cálculo: {z_max} - {z_min} = {z_component}")
    
    # Componente θ
    theta_component = float(sp.sin(theta_max) - sp.sin(theta_min))
    print(f"\nComponente θ (sin(θ_max) - sin(θ_min)): {theta_component}")
    print(f"  Límites θ: {theta_min} → {theta_max}")
    print(f"  Cálculo: sin({theta_max}) - sin({theta_min}) = {theta_component}")
    
    # Componente r
    r_component = (r_max**3 - r_min**3) / 3
    print(f"\nComponente r ((r_max³ - r_min³) / 3): {r_component}")
    print(f"  Límites r: {r_min} → {r_max}")
    print(f"  Cálculo: ({r_max}³ - {r_min}³) / 3 = {r_component}")
    
    # Resultado manual
    resultado_manual = z_component * theta_component * r_component
    print(f"\nResultado manual:")
    print(f"  {z_component} * {theta_component} * {r_component} = {resultado_manual}")

def main():
    calcular_integral_cilindrica()

if __name__ == "__main__":
    main()
