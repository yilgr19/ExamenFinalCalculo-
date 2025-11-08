import sympy as sp
import numpy as np
import math
import sys

def calcular_integral_cilindrica_precision():
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
    print(f"Límites:")
    print(f"r: {r_min} → {r_max}")
    print(f"θ: {theta_min} → {theta_max}")
    print(f"z: {z_min} → {z_max}")
    
    # Método 1: Integración simbólica paso a paso
    print("\n--- Método 1: Integración Simbólica Paso a Paso ---")
    
    # Paso 1: Integral respecto a z
    integral_z = f * (z_max - z_min)
    print(f"1. Integral en z: {integral_z}")
    
    # Paso 2: Integral respecto a θ
    integral_theta = sp.integrate(integral_z * sp.cos(theta), (theta, theta_min, theta_max))
    print(f"2. Integral en θ: {integral_theta}")
    
    # Paso 3: Integral respecto a r
    integral_r = sp.integrate(integral_theta * r, (r, r_min, r_max))
    print(f"3. Integral en r: {integral_r}")
    
    # Evaluación numérica simbólica
    resultado_simbolico = integral_r
    resultado_numerico_simbolico = float(sp.N(resultado_simbolico, 15))
    print(f"\nResultado simbólico: {resultado_simbolico}")
    print(f"Resultado numérico simbólico: {resultado_numerico_simbolico}")
    
    # Método 2: Cálculo manual detallado
    print("\n--- Método 2: Cálculo Manual Detallado ---")
    
    # Componentes del cálculo
    z_component = z_max - z_min
    theta_component = float(sp.sin(theta_max) - sp.sin(theta_min))
    r_component = (r_max**3 - r_min**3) / 3
    
    print(f"Componente z (intervalo): {z_component}")
    print(f"Componente θ (sin(θ_max) - sin(θ_min)): {theta_component}")
    print(f"Componente r ((r_max³ - r_min³) / 3): {r_component}")
    
    # Cálculo manual multiplicativo
    resultado_manual = z_component * theta_component * r_component
    print(f"Resultado manual: {resultado_manual}")
    
    # Método 3: Integración numérica
    print("\n--- Método 3: Integración Numérica ---")
    
    def funcion_integracion(r_val, theta_val, z_val):
        return r_val**2 * math.cos(theta_val)
    
    # Método de Simpson para integración numérica
    def integrar_simpson_3d(f, x_min, x_max, y_min, y_max, z_min, z_max, nx=50, ny=50, nz=50):
        x = np.linspace(x_min, x_max, nx)
        y = np.linspace(y_min, y_max, ny)
        z = np.linspace(z_min, z_max, nz)
        
        dx = (x_max - x_min) / (nx - 1)
        dy = (y_max - y_min) / (ny - 1)
        dz = (z_max - z_min) / (nz - 1)
        
        integral = 0.0
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    integral += f(x[i], y[j], z[k])
        
        integral *= dx * dy * dz
        return integral
    
    # Realizar integración numérica
    resultado_numerico = integrar_simpson_3d(
        funcion_integracion, 
        r_min, r_max, 
        theta_min, theta_max, 
        z_min, z_max
    )
    print(f"Resultado numérico (integración Simpson): {resultado_numerico}")
    
    # Comparación de resultados
    print("\n--- Comparación de Resultados ---")
    print(f"Método Simbólico: {resultado_numerico_simbolico}")
    print(f"Método Manual: {resultado_manual}")
    print(f"Método Numérico: {resultado_numerico}")

def main():
    calcular_integral_cilindrica_precision()

if __name__ == "__main__":
    main()
