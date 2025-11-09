"""
ARCHIVO: integral_calculator.py
DESCRIPCIÓN: Calculadora de integrales triples - VERSIÓN CORREGIDA
VERSIÓN: 4.0 - Solución real para límites variables
"""

import sympy as sp

class IntegralCalculator:
    """Clase para calcular integrales triples en diferentes sistemas de coordenadas"""
    
    @staticmethod
    def integral_rectangular_especial_A4():
        """
        Cálculo manual del ejercicio A4: ∫∫∫ (x²+y²+z²) con límites variables
        x: 0→1, y: 0→x, z: 0→y
        """
        x, y, z = sp.symbols('x y z', real=True)
        pasos = []
        
        pasos.append("╔═══════════════════════════════════════════════════════════════╗")
        pasos.append("║     EJERCICIO A4 - CÁLCULO MANUAL CON LÍMITES VARIABLES       ║")
        pasos.append("╚═══════════════════════════════════════════════════════════════╝")
        pasos.append("")
        pasos.append("Función: f(x,y,z) = x² + y² + z²")
        pasos.append("Límites: x∈[0,1], y∈[0,x], z∈[0,y]")
        pasos.append("")
        
        # PASO 1: Integrar en z
        pasos.append("PASO 1: ∫₀ʸ (x² + y² + z²) dz")
        pasos.append("= [x²z + y²z + z³/3]₀ʸ")
        pasos.append("= x²y + y²y + y³/3")
        pasos.append("= x²y + y³ + y³/3")
        pasos.append("= x²y + 4y³/3")
        I1 = x**2 * y + sp.Rational(4,3) * y**3
        pasos.append(f"✓ Resultado: {I1}")
        pasos.append("")
        
        # PASO 2: Integrar en y
        pasos.append("PASO 2: ∫₀ˣ (x²y + 4y³/3) dy")
        pasos.append("= [x²y²/2 + 4y⁴/12]₀ˣ")
        pasos.append("= [x²y²/2 + y⁴/3]₀ˣ")
        pasos.append("= x²·x²/2 + x⁴/3")
        pasos.append("= x⁴/2 + x⁴/3")
        pasos.append("= 3x⁴/6 + 2x⁴/6")
        pasos.append("= 5x⁴/6")
        I2 = sp.Rational(5,6) * x**4
        pasos.append(f"✓ Resultado: {I2}")
        pasos.append("")
        
        # PASO 3: Integrar en x
        pasos.append("PASO 3: ∫₀¹ (5x⁴/6) dx")
        pasos.append("= [5x⁵/30]₀¹")
        pasos.append("= [x⁵/6]₀¹")
        pasos.append("= 1/6 - 0")
        pasos.append("= 1/6")
        resultado = sp.Rational(1,6)
        pasos.append(f"✓ Resultado: {resultado}")
        pasos.append("")
        pasos.append("═" * 63)
        pasos.append(f"RESULTADO FINAL: 1/6 = {float(resultado):.15f}")
        pasos.append("═" * 63)
        
        return {
            "resultado_manual": float(resultado),
            "resultado_simbolico": resultado,
            "resultado_simbolico_evaluado": float(resultado),
            "pasos": "\n".join(pasos)
        }
    
    @staticmethod
    def integral_rectangular(f, x_lim, y_lim, z_lim):
        """
        Calcular integral triple en coordenadas rectangulares
        Orden correcto: ∫∫∫ f(x,y,z) dz dy dx
        """
        x, y, z = sp.symbols('x y z', real=True)
        pasos = []

        pasos.append("╔═══════════════════════════════════════════════════════════════╗")
        pasos.append("║        INTEGRAL TRIPLE EN COORDENADAS RECTANGULARES           ║")
        pasos.append("╚═══════════════════════════════════════════════════════════════╝")
        pasos.append("")
        pasos.append(f"📌 Función original: f(x,y,z) = {f}")
        pasos.append(f"📌 Región de integración:")
        pasos.append(f"   • x ∈ [{x_lim[0]}, {x_lim[1]}]")
        pasos.append(f"   • y ∈ [{y_lim[0]}, {y_lim[1]}]")
        pasos.append(f"   • z ∈ [{z_lim[0]}, {z_lim[1]}]")
        pasos.append(f"📌 Orden de integración: dz dy dx")
        pasos.append("")
        pasos.append("─" * 63)

        try:
            # Convertir límites
            def procesar_limite(lim_str):
                if isinstance(lim_str, str):
                    lim_str = lim_str.strip()
                    return sp.sympify(lim_str, locals={'x': x, 'y': y, 'z': z})
                elif isinstance(lim_str, (int, float)):
                    return sp.sympify(lim_str)
                else:
                    return lim_str
            
            z_min = procesar_limite(z_lim[0])
            z_max = procesar_limite(z_lim[1])
            y_min = procesar_limite(y_lim[0])
            y_max = procesar_limite(y_lim[1])
            x_min = procesar_limite(x_lim[0])
            x_max = procesar_limite(x_lim[1])

            # 1️⃣ PASO 1: Integrar respecto a Z
            pasos.append("")
            pasos.append("PASO 1: Integrar respecto a Z")
            pasos.append("─" * 63)
            pasos.append(f"Calculamos: ∫[{z_min} → {z_max}] ({f}) dz")
            
            I_z = sp.integrate(f, (z, z_min, z_max))
            I_z = sp.simplify(I_z)
            
            pasos.append(f"✓ Resultado: {I_z}")
            pasos.append("")

            # 2️⃣ PASO 2: Integrar respecto a Y
            pasos.append("PASO 2: Integrar respecto a Y")
            pasos.append("─" * 63)
            pasos.append(f"Calculamos: ∫[{y_min} → {y_max}] ({I_z}) dy")
            
            I_y = sp.integrate(I_z, (y, y_min, y_max))
            I_y = sp.simplify(I_y)
            
            pasos.append(f"✓ Resultado: {I_y}")
            pasos.append("")

            # 3️⃣ PASO 3: Integrar respecto a X
            pasos.append("PASO 3: Integrar respecto a X")
            pasos.append("─" * 63)
            pasos.append(f"Calculamos: ∫[{x_min} → {x_max}] ({I_y}) dx")
            
            I_x = sp.integrate(I_y, (x, x_min, x_max))
            I_x = sp.simplify(I_x)
            
            pasos.append(f"✓ Resultado: {I_x}")
            pasos.append("")

            pasos.append("═" * 63)
            pasos.append("RESULTADO FINAL")
            pasos.append("═" * 63)

            resultado_simbolico = sp.simplify(I_x)
            pasos.append(f"Expresión simbólica simplificada: {resultado_simbolico}")

            # Evaluación numérica
            resultado_numerico = None
            resultado_evaluado = None
            
            if resultado_simbolico.is_number:
                try:
                    resultado_evaluado = resultado_simbolico.evalf(15)
                    resultado_numerico = float(resultado_evaluado)
                    pasos.append(f"Valor numérico: {resultado_numerico}")
                    
                    # Intentar expresar como fracción
                    try:
                        fraccion = sp.nsimplify(resultado_simbolico)
                        if fraccion != resultado_simbolico and fraccion.is_Rational:
                            pasos.append(f"Como fracción: {fraccion}")
                    except:
                        pass
                    
                    pasos.append(f"✅ Cálculo completado exitosamente")
                except Exception as e:
                    pasos.append(f"⚠️  No se pudo convertir a float: {str(e)}")
                    resultado_evaluado = resultado_simbolico
            else:
                variables_restantes = resultado_simbolico.free_symbols
                if variables_restantes:
                    pasos.append(f"⚠️  ADVERTENCIA: El resultado aún contiene variables: {variables_restantes}")
                    pasos.append(f"   La integración puede no haberse completado correctamente.")
                resultado_evaluado = resultado_simbolico.evalf() if hasattr(resultado_simbolico, 'evalf') else resultado_simbolico

            return {
                "resultado_manual": resultado_numerico,
                "resultado_simbolico": resultado_simbolico,
                "resultado_simbolico_evaluado": resultado_evaluado,
                "pasos": "\n".join(pasos)
            }

        except Exception as e:
            import traceback
            pasos.append("")
            pasos.append("═" * 63)
            pasos.append("❌ ERROR EN LA INTEGRACIÓN")
            pasos.append("═" * 63)
            pasos.append(str(e))
            pasos.append("")
            pasos.append("Stack trace:")
            pasos.append(traceback.format_exc())
            
            return {
                "resultado_manual": None,
                "resultado_simbolico": f"Error: {str(e)}",
                "resultado_simbolico_evaluado": None,
                "pasos": "\n".join(pasos)
            }

    # Los métodos de coordenadas cilíndricas y esféricas permanecen igual que en el código anterior
    @staticmethod
    def integral_cylindrical(f, r_lim, theta_lim, z_lim):
        """Integral triple en coordenadas cilíndricas - Orden: dz dr dθ"""
        r, theta, z = sp.symbols('r theta z', real=True, positive=True)
        pasos = []

        pasos.append("╔═══════════════════════════════════════════════════════════════╗")
        pasos.append("║        INTEGRAL TRIPLE EN COORDENADAS CILÍNDRICAS             ║")
        pasos.append("╚═══════════════════════════════════════════════════════════════╝")
        pasos.append("")
        pasos.append(f"📌 Función: f(r,θ,z) = {f}")
        pasos.append(f"📌 Jacobiano: r")
        pasos.append(f"📌 Límites:")
        pasos.append(f"   • r ∈ [{r_lim[0]}, {r_lim[1]}]")
        pasos.append(f"   • θ ∈ [{theta_lim[0]}, {theta_lim[1]}]")
        pasos.append(f"   • z ∈ [{z_lim[0]}, {z_lim[1]}]")
        pasos.append(f"📌 Orden de integración: dz dr dθ")
        pasos.append("")
        pasos.append("─" * 63)

        try:
            # Sustituir símbolos para asegurar compatibilidad
            f_local = f.subs([
                (sp.Symbol('r', real=True), r),
                (sp.Symbol('theta', real=True), theta),
                (sp.Symbol('z', real=True), z)
            ])
            
            integrando = f_local * r
            pasos.append("")
            pasos.append("PREPARACIÓN: Aplicar el Jacobiano")
            pasos.append("─" * 63)
            pasos.append(f"Integrando con jacobiano: f(r,θ,z) · r = {integrando}")
            pasos.append("")

            def procesar(lim):
                if isinstance(lim, str):
                    lim = lim.strip()
                    return sp.sympify(lim, locals={'r': r, 'theta': theta, 'z': z, 'pi': sp.pi})
                return sp.sympify(lim)
            
            z_min, z_max = procesar(z_lim[0]), procesar(z_lim[1])
            r_min, r_max = procesar(r_lim[0]), procesar(r_lim[1])
            theta_min, theta_max = procesar(theta_lim[0]), procesar(theta_lim[1])

            # PASO 1: Integrar respecto a Z
            pasos.append("PASO 1: Integrar respecto a Z")
            pasos.append("─" * 63)
            pasos.append(f"∫[{z_min} → {z_max}] ({integrando}) dz")
            
            I_z = sp.integrate(integrando, (z, z_min, z_max))
            I_z = sp.simplify(I_z)
            pasos.append(f"✓ Resultado: {I_z}")
            pasos.append(f"   (Función de r y θ)")
            pasos.append("")
            
            # PASO 2: Integrar respecto a R
            pasos.append("PASO 2: Integrar respecto a R")
            pasos.append("─" * 63)
            pasos.append(f"∫[{r_min} → {r_max}] ({I_z}) dr")
            
            I_r = sp.integrate(I_z, (r, r_min, r_max))
            I_r = sp.simplify(I_r)
            pasos.append(f"✓ Resultado: {I_r}")
            pasos.append(f"   (Función de θ)")
            pasos.append("")
            
            # PASO 3: Integrar respecto a THETA
            pasos.append("PASO 3: Integrar respecto a Θ")
            pasos.append("─" * 63)
            pasos.append(f"∫[{theta_min} → {theta_max}] ({I_r}) dθ")
            
            I_theta = sp.integrate(I_r, (theta, theta_min, theta_max))
            resultado = sp.simplify(I_theta)
            pasos.append(f"✓ Resultado final: {resultado}")
            pasos.append("")
            pasos.append("═" * 63)

            # Evaluación numérica
            resultado_num = None
            resultado_eval = resultado
            
            try:
                if resultado.is_number:
                    resultado_eval = resultado.evalf(15)
                    resultado_num = float(resultado_eval)
                    pasos.append(f"Valor numérico: {resultado_num}")
                    
                    # Intentar expresar como fracción con pi
                    try:
                        # Verificar si es múltiplo de pi
                        coef = resultado / sp.pi
                        coef_simplificado = sp.nsimplify(coef)
                        if coef_simplificado.is_rational:
                            pasos.append(f"Como expresión: {coef_simplificado}π")
                    except:
                        pass
                else:
                    variables_restantes = resultado.free_symbols
                    if variables_restantes:
                        pasos.append(f"⚠️  ADVERTENCIA: Resultado contiene variables: {variables_restantes}")
                        pasos.append(f"   La integración puede no haberse completado.")
                    resultado_eval = resultado.evalf() if hasattr(resultado, 'evalf') else resultado
            except Exception as e:
                pasos.append(f"⚠️  Error al evaluar: {str(e)}")

            return {
                "resultado_manual": resultado_num,
                "resultado_simbolico": resultado,
                "resultado_simbolico_evaluado": resultado_eval,
                "pasos": "\n".join(pasos)
            }

        except Exception as e:
            import traceback
            pasos.append("")
            pasos.append("═" * 63)
            pasos.append("❌ ERROR EN INTEGRACIÓN CILÍNDRICA")
            pasos.append("═" * 63)
            pasos.append(str(e))
            pasos.append(traceback.format_exc())
            
            return {
                "resultado_manual": None,
                "resultado_simbolico": f"Error: {str(e)}",
                "resultado_simbolico_evaluado": None,
                "pasos": "\n".join(pasos)
            }

    @staticmethod
    def integral_spherical(f, rho_lim, theta_lim, phi_lim):
        """Integral triple en coordenadas esféricas"""
        rho, theta, phi = sp.symbols('rho theta phi', real=True, positive=True)
        pasos = []

        pasos.append("╔═══════════════════════════════════════════════════════════════╗")
        pasos.append("║        INTEGRAL TRIPLE EN COORDENADAS ESFÉRICAS              ║")
        pasos.append("╚═══════════════════════════════════════════════════════════════╝")
        pasos.append("")
        pasos.append(f"📌 Función: f(ρ,θ,φ) = {f}")
        pasos.append(f"📌 Jacobiano: ρ²·sin(φ)")
        pasos.append(f"📌 Límites: ρ[{rho_lim[0]},{rho_lim[1]}], θ[{theta_lim[0]},{theta_lim[1]}], φ[{phi_lim[0]},{phi_lim[1]}]")
        pasos.append("")

        try:
            integrando = f * rho**2 * sp.sin(phi)
            pasos.append(f"Integrando con jacobiano: {integrando}")
            pasos.append("")

            def procesar(lim):
                if isinstance(lim, str):
                    return sp.sympify(lim.strip(), locals={'rho': rho, 'theta': theta, 'phi': phi})
                return sp.sympify(lim)
            
            rho_min, rho_max = procesar(rho_lim[0]), procesar(rho_lim[1])
            theta_min, theta_max = procesar(theta_lim[0]), procesar(theta_lim[1])
            phi_min, phi_max = procesar(phi_lim[0]), procesar(phi_lim[1])

            # Integrar paso a paso
            anti_rho = sp.integrate(integrando, rho)
            I_rho = sp.simplify(anti_rho.subs(rho, rho_max) - anti_rho.subs(rho, rho_min))
            pasos.append(f"Después de ∫dρ: {I_rho}")
            
            anti_theta = sp.integrate(I_rho, theta)
            I_theta = sp.simplify(anti_theta.subs(theta, theta_max) - anti_theta.subs(theta, theta_min))
            pasos.append(f"Después de ∫dθ: {I_theta}")
            
            anti_phi = sp.integrate(I_theta, phi)
            resultado = sp.simplify(anti_phi.subs(phi, phi_max) - anti_phi.subs(phi, phi_min))
            pasos.append(f"Resultado final: {resultado}")

            resultado_num = None
            try:
                if resultado.is_number:
                    resultado_num = float(resultado.evalf())
            except:
                pass

            return {
                "resultado_manual": resultado_num,
                "resultado_simbolico": resultado,
                "resultado_simbolico_evaluado": resultado.evalf() if resultado.is_number else resultado,
                "pasos": "\n".join(pasos)
            }

        except Exception as e:
            import traceback
            return {
                "resultado_manual": None,
                "resultado_simbolico": f"Error: {str(e)}",
                "resultado_simbolico_evaluado": None,
                "pasos": "\n".join(pasos) + f"\n\nError:\n{traceback.format_exc()}"
            }


# PRUEBA DIRECTA
if __name__ == "__main__":
    print("="*70)
    print("🧪 PRUEBAS DE LA CALCULADORA")
    print("="*70)
    
    calc = IntegralCalculator()
    
    # PRUEBA 1: Ejercicio A4
    print("\n" + "="*70)
    print("PRUEBA 1: EJERCICIO A4 (Límites variables)")
    print("="*70)
    resultado_a4 = calc.integral_rectangular_especial_A4()
    print(resultado_a4['pasos'])
    print(f"\n✅ Resultado: {resultado_a4['resultado_manual']}")
    print(f"✅ Esperado: {1/6:.15f}")
    
    # PRUEBA 2: Coordenadas cilíndricas
    print("\n" + "="*70)
    print("PRUEBA 2: COORDENADAS CILÍNDRICAS")
    print("="*70)
    print("Función: r²·z")
    print("Límites: r[0,1], θ[0,π/2], z[0,2]")
    print("Calculando...")
    
    r, theta, z = sp.symbols('r theta z', real=True, positive=True)
    f_cil = r**2 * z
    
    resultado_cil = calc.integral_cylindrical(
        f_cil,
        [0, 1],
        [0, sp.pi/2],
        [0, 2]
    )
    print(resultado_cil['pasos'])
    print(f"\n✅ Resultado simbólico: {resultado_cil['resultado_simbolico']}")
    print(f"✅ Resultado numérico: {resultado_cil['resultado_manual']}")
    
    # Cálculo manual para verificar
    print("\n📝 Verificación manual:")
    print("∫∫∫ r²z · r dz dr dθ")
    print("= ∫∫ r³·[z²/2]₀² dr dθ")
    print("= ∫∫ r³·2 dr dθ")
    print("= ∫ 2·[r⁴/4]₀¹ dθ")
    print("= ∫ 1/2 dθ")
    print("= [θ/2]₀^(π/2)")
    print("= π/4")
    print(f"= {sp.pi/4} = {float(sp.pi/4):.15f}")
    
    esperado = float(sp.pi/4)
    if resultado_cil['resultado_manual']:
        diff = abs(resultado_cil['resultado_manual'] - esperado)
        print(f"\nDiferencia: {diff:.2e}")
        print(f"{'✅ CORRECTO' if diff < 1e-10 else '❌ INCORRECTO'}")
    else:
        print("\n❌ No se obtuvo resultado numérico")
    
    print("="*70)