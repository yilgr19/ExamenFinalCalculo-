"""
ARCHIVO: integral_calculator.py
DESCRIPCIÓN: Calculadora de integrales triples en diferentes sistemas de coordenadas
AUTOR: Versión corregida
"""

import sympy as sp


class IntegralCalculator:
    """Clase para calcular integrales triples en diferentes sistemas de coordenadas"""
    
    @staticmethod
    def integral_rectangular(f, x_lim, y_lim, z_lim):
        """
        Calcular integral triple en coordenadas rectangulares
        Orden correcto: ∫∫∫ f(x,y,z) dx dy dz
        """
        x, y, z = sp.symbols('x y z', real=True)
        pasos = []

        pasos.append("Sistema: Rectangular")
        pasos.append(f"Función original: f(x,y,z) = {f}")
        pasos.append("Orden de integración: dx dy dz")

        try:
            # 1️⃣ Integrar respecto a x
            I_x = sp.integrate(f, (x, x_lim[0], x_lim[1]))
            I_x = sp.simplify(I_x)
            pasos.append(f"1️⃣ ∫ f dx = {I_x}")

            # 2️⃣ Integrar respecto a y
            I_y = sp.integrate(I_x, (y, y_lim[0], y_lim[1]))
            I_y = sp.simplify(I_y)
            pasos.append(f"2️⃣ ∫ (resultado anterior) dy = {I_y}")

            # 3️⃣ Integrar respecto a z
            I_z = sp.integrate(I_y, (z, z_lim[0], z_lim[1]))
            I_z = sp.simplify(I_z)
            pasos.append(f"3️⃣ ∫ (resultado anterior) dz = {I_z}")

            resultado_simbolico = sp.simplify(I_z)

            try:
                resultado_numerico = float(sp.N(resultado_simbolico, 15))
            except Exception:
                resultado_numerico = None

            return {
                "resultado_manual": resultado_numerico,
                "resultado_simbolico": resultado_simbolico,
                "resultado_simbolico_evaluado": resultado_numerico,
                "pasos": "\n".join(pasos)
            }

        except Exception as e:
            return {
                "resultado_manual": None,
                "resultado_simbolico": str(e),
                "resultado_simbolico_evaluado": None,
                "pasos": f"Error en integración: {str(e)}"
            }

    @staticmethod
    def integral_cylindrical(f, r_lim, theta_lim, z_lim):
        """
        Calcular integral triple en coordenadas cilíndricas.
        Orden correcto: ∫∫∫ f(r,θ,z) * r dz dr dθ
        Jacobiano: r
        
        IMPORTANTE: La función f debe estar en términos de los símbolos
        r, theta, z definidos internamente.
        """
        # Definir símbolos locales
        r, theta, z = sp.symbols('r theta z', real=True, positive=True)
        pasos = []

        pasos.append("Sistema: Cilíndrico")
        pasos.append(f"Función original: f(r,θ,z) = {f}")
        pasos.append("Orden de integración: dz dr dθ")

        # CRÍTICO: Substituir los símbolos de la función por los locales
        # Esto asegura que estemos usando exactamente los mismos símbolos
        f_local = f.subs([
            (sp.Symbol('r', real=True), r),
            (sp.Symbol('r', real=True, positive=True), r),
            (sp.Symbol('theta', real=True), theta),
            (sp.Symbol('theta', real=True, positive=True), theta),
            (sp.Symbol('z', real=True), z),
            (sp.Symbol('z', real=True, positive=True), z)
        ])

        # Multiplicamos por el Jacobiano (r)
        integrando = f_local * r
        pasos.append(f"Integrando con Jacobiano (r): {integrando}")

        try:
            # 1️⃣ Integrar respecto a z
            I_z = sp.integrate(integrando, (z, z_lim[0], z_lim[1]))
            I_z = sp.simplify(I_z)
            pasos.append(f"1️⃣ ∫ f*r dz = {I_z}")

            # 2️⃣ Integrar respecto a r
            I_r = sp.integrate(I_z, (r, r_lim[0], r_lim[1]))
            I_r = sp.simplify(I_r)
            pasos.append(f"2️⃣ ∫ (resultado anterior) dr = {I_r}")

            # 3️⃣ Integrar respecto a θ
            I_theta = sp.integrate(I_r, (theta, theta_lim[0], theta_lim[1]))
            I_theta = sp.simplify(I_theta)
            pasos.append(f"3️⃣ ∫ (resultado anterior) dθ = {I_theta}")

            # Simplificar resultado final
            resultado_simbolico = sp.simplify(I_theta)
            
            # Forzar evaluación numérica completa
            try:
                resultado_simbolico_evaluado = sp.N(resultado_simbolico, 15)
                resultado_manual = float(resultado_simbolico_evaluado)
            except:
                resultado_simbolico_evaluado = resultado_simbolico.evalf()
                try:
                    resultado_manual = float(resultado_simbolico_evaluado)
                except:
                    resultado_manual = None

            return {
                "resultado_manual": resultado_manual,
                "resultado_simbolico": resultado_simbolico,
                "resultado_simbolico_evaluado": resultado_simbolico_evaluado,
                "pasos": "\n".join(pasos)
            }

        except Exception as e:
            return {
                "resultado_manual": None,
                "resultado_simbolico": str(e),
                "resultado_simbolico_evaluado": None,
                "pasos": f"Error en integración cilíndrica: {str(e)}"
            }

    @staticmethod
    def integral_spherical(f, rho_lim, theta_lim, phi_lim):
        """
        Calcular integral triple en coordenadas esféricas
        Orden correcto: ∫∫∫ f(ρ,θ,φ) * ρ² sin(φ) dρ dθ dφ
        Jacobiano: ρ² sin(φ)
        """
        # Definir símbolos locales
        rho, theta, phi = sp.symbols('rho theta phi', real=True, positive=True)
        pasos = []

        pasos.append("Sistema: Esférico")
        pasos.append(f"Función original: f(ρ,θ,φ) = {f}")
        pasos.append("Orden de integración: dρ dθ dφ")

        # Substituir símbolos para asegurar consistencia
        f_local = f.subs([
            (sp.Symbol('rho', real=True), rho),
            (sp.Symbol('rho', real=True, positive=True), rho),
            (sp.Symbol('theta', real=True), theta),
            (sp.Symbol('theta', real=True, positive=True), theta),
            (sp.Symbol('phi', real=True), phi),
            (sp.Symbol('phi', real=True, positive=True), phi)
        ])

        # Multiplicamos por el Jacobiano
        integrando = f_local * rho**2 * sp.sin(phi)
        pasos.append(f"Integrando con Jacobiano (ρ² sin(φ)): {integrando}")

        try:
            # 1️⃣ Integrar respecto a ρ
            I_rho = sp.integrate(integrando, (rho, rho_lim[0], rho_lim[1]))
            I_rho = sp.simplify(I_rho)
            pasos.append(f"1️⃣ ∫ f*ρ²*sin(φ) dρ = {I_rho}")

            # 2️⃣ Integrar respecto a θ
            I_theta = sp.integrate(I_rho, (theta, theta_lim[0], theta_lim[1]))
            I_theta = sp.simplify(I_theta)
            pasos.append(f"2️⃣ ∫ (resultado anterior) dθ = {I_theta}")

            # 3️⃣ Integrar respecto a φ
            I_phi = sp.integrate(I_theta, (phi, phi_lim[0], phi_lim[1]))
            I_phi = sp.simplify(I_phi)
            pasos.append(f"3️⃣ ∫ (resultado anterior) dφ = {I_phi}")

            resultado_simbolico = sp.simplify(I_phi)
            
            try:
                resultado_simbolico_evaluado = sp.N(resultado_simbolico, 15)
                resultado_manual = float(resultado_simbolico_evaluado)
            except:
                resultado_simbolico_evaluado = resultado_simbolico.evalf()
                try:
                    resultado_manual = float(resultado_simbolico_evaluado)
                except:
                    resultado_manual = None

            return {
                "resultado_manual": resultado_manual,
                "resultado_simbolico": resultado_simbolico,
                "resultado_simbolico_evaluado": resultado_simbolico_evaluado,
                "pasos": "\n".join(pasos)
            }

        except Exception as e:
            return {
                "resultado_manual": None,
                "resultado_simbolico": str(e),
                "resultado_simbolico_evaluado": None,
                "pasos": f"Error en integración esférica: {str(e)}"
            }


# Función de prueba
if __name__ == "__main__":
    print("="*60)
    print("PRUEBA DE INTEGRAL CILÍNDRICA")
    print("="*60)
    
    # Definir símbolos
    r, theta, z = sp.symbols('r theta z', real=True, positive=True)
    
    # Función: r
    f = r
    
    # Límites
    r_lim = [0, 1]
    theta_lim = [0, 2*sp.pi]
    z_lim = [0, 1]
    
    # Calcular
    calc = IntegralCalculator()
    resultado = calc.integral_cylindrical(f, r_lim, theta_lim, z_lim)
    
    print("\n" + resultado['pasos'])
    print("\n" + "="*60)
    print("RESULTADO FINAL:")
    print(f"Simbólico: {resultado['resultado_simbolico']}")
    print(f"Numérico: {resultado['resultado_manual']}")
    print(f"Esperado: 2π/3 ≈ {float((2*sp.pi/3).evalf())}")
    print("="*60)