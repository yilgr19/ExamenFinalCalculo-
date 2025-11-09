import sympy as sp

class IntegralCalculator:
    @staticmethod
    def _convertir_a_numerico(resultado_simbolico):
        """
        Convierte un resultado simbólico a numérico de manera robusta
        """
        # Intentar diferentes métodos de conversión
        metodos_conversion = [
            lambda x: float(x),  # Conversión directa a float
            lambda x: float(sp.N(x, 15)),  # Evaluación numérica de SymPy
            lambda x: float(x.evalf(15)),  # Método evalf de SymPy
            lambda x: float(sp.simplify(x).evalf(15))  # Simplificar primero
        ]
        
        for metodo in metodos_conversion:
            try:
                return metodo(resultado_simbolico)
            except Exception:
                continue
        
        return None

    # =========================
    # 🔹 RECTANGULAR CON LÍMITES VARIABLES
    # =========================
    @staticmethod
    def integral_rectangular(f, x_lim, y_lim, z_lim):
        """
        Calcula integral triple con límites que pueden depender de otras variables
        Detecta automáticamente el orden correcto de integración
        """
        x, y, z = sp.symbols('x y z', real=True)
        
        # Detectar dependencias de variables en límites
        x_symbols = set()
        y_symbols = set()
        z_symbols = set()
        
        for lim in x_lim:
            x_symbols.update(lim.free_symbols if hasattr(lim, 'free_symbols') else set())
        for lim in y_lim:
            y_symbols.update(lim.free_symbols if hasattr(lim, 'free_symbols') else set())
        for lim in z_lim:
            z_symbols.update(lim.free_symbols if hasattr(lim, 'free_symbols') else set())
        
        # Determinar orden de integración correcto
        if z in z_symbols or y in z_symbols:
            orden = "dz dy dx"
            var_orden = [(z, z_lim, 'z'), (y, y_lim, 'y'), (x, x_lim, 'x')]
        elif y in y_symbols:
            if z in y_symbols:
                orden = "dy dz dx"
                var_orden = [(y, y_lim, 'y'), (z, z_lim, 'z'), (x, x_lim, 'x')]
            else:
                orden = "dz dy dx"
                var_orden = [(z, z_lim, 'z'), (y, y_lim, 'y'), (x, x_lim, 'x')]
        else:
            orden = "dz dy dx"
            var_orden = [(z, z_lim, 'z'), (y, y_lim, 'y'), (x, x_lim, 'x')]
        
        pasos = ["╔═══════════════════════════════════════════════════════════════╗",
                 "║     INTEGRAL TRIPLE EN COORDENADAS RECTANGULARES             ║",
                 "╚═══════════════════════════════════════════════════════════════╝",
                 f"\n📌 Función: f(x,y,z) = {f}",
                 f"📌 Límites de integración:",
                 f"   • x: [{x_lim[0]}] → [{x_lim[1]}]",
                 f"   • y: [{y_lim[0]}] → [{y_lim[1]}]",
                 f"   • z: [{z_lim[0]}] → [{z_lim[1]}]",
                 f"\n📌 Orden de integración detectado: {orden}",
                 f"📌 (Orden determinado por dependencias de variables)\n"]

        # Integración iterativa con orden correcto
        resultado_actual = f
        
        for i, (var, lims, nombre_var) in enumerate(var_orden, 1):
            pasos.append("="*60)
            pasos.append(f"PASO {i}: Integración respecto a {nombre_var}")
            pasos.append("="*60)
            pasos.append(f"∫ ({resultado_actual}) d{nombre_var}  con {nombre_var} ∈ [{lims[0]}, {lims[1]}]")
            
            # Integrar
            resultado_actual = sp.integrate(resultado_actual, (var, lims[0], lims[1]))
            resultado_actual = sp.simplify(resultado_actual)
            
            pasos.append(f"\n🔸 Resultado después de integrar en {nombre_var}:")
            if i < 3:
                vars_restantes = [v[2] for v in var_orden[i:]]
                pasos.append(f"   f_{i}({','.join(vars_restantes)}) = {resultado_actual}")
            else:
                pasos.append(f"   Resultado final = {resultado_actual}")

        f3 = resultado_actual

        # Convertir a numérico
        valor_numerico = IntegralCalculator._convertir_a_numerico(f3)

        pasos.append("\n" + "="*60)
        pasos.append("RESULTADO FINAL")
        pasos.append("="*60)
        pasos.append(f"✅ Resultado simbólico: {f3}")
        
        if isinstance(f3, sp.Rational):
            pasos.append(f"✅ Forma fraccionaria: {f3.p}/{f3.q}")
        
        pasos.append(f"✅ Valor numérico: {valor_numerico}")

        return {
            "resultado_simbolico": f3,
            "resultado_manual": valor_numerico,
            "pasos": "\n".join(pasos)
        }

    # =========================
    # 🔹 CILÍNDRICO - CORREGIDO ✅
    # =========================
    @staticmethod
    def integral_cylindrical(f, r_lim, theta_lim, z_lim):
        """
        Calcula integral triple cilíndrica con límites variables
        CORRECCIÓN: Detecta correctamente si la función usa r,theta,z o x,y,z
        """
        # Definir símbolos de AMBOS sistemas
        x, y, z_cart = sp.symbols('x y z', real=True)
        r, theta, z = sp.symbols('r theta z', real=True, positive=True)
        
        pasos = ["╔═══════════════════════════════════════════════════════════════╗",
                 "║     INTEGRAL TRIPLE EN COORDENADAS CILÍNDRICAS              ║",
                 "╚═══════════════════════════════════════════════════════════════╝"]
        
        # Detectar qué variables usa la función
        simbolos_func = f.free_symbols
        usa_cartesianas = any(s in simbolos_func for s in [x, y, z_cart])
        usa_cilindricas = any(s in simbolos_func for s in [r, theta, z])
        
        f_cyl = f
        
        if usa_cartesianas and not usa_cilindricas:
            # Función en cartesianas → convertir
            pasos.append(f"\n📌 Función original (cartesiana): f(x,y,z) = {f}")
            pasos.append(f"📌 Conversión a cilíndricas:")
            pasos.append(f"   x = r·cos(θ)")
            pasos.append(f"   y = r·sin(θ)")
            pasos.append(f"   z = z")
            
            f_cyl = f.subs([
                (x, r*sp.cos(theta)), 
                (y, r*sp.sin(theta)), 
                (z_cart, z)
            ])
            f_cyl = sp.simplify(f_cyl)
            pasos.append(f"📌 Función en cilíndricas: f(r,θ,z) = {f_cyl}")
        else:
            # Función ya en cilíndricas o constante
            pasos.append(f"\n📌 Función: f(r,θ,z) = {f}")
        
        pasos.extend([
            f"📌 Jacobiano cilíndrico: r",
            f"📌 Límites de integración:",
            f"   • r: [{r_lim[0]}] → [{r_lim[1]}]",
            f"   • θ: [{theta_lim[0]}] → [{theta_lim[1]}]",
            f"   • z: [{z_lim[0]}] → [{z_lim[1]}]",
            f"\n📌 Orden de integración: dz dr dθ\n"
        ])

        # Aplicar Jacobiano
        integrand = sp.simplify(f_cyl * r)
        pasos.append("="*60)
        pasos.append("PREPARACIÓN: Aplicar Jacobiano")
        pasos.append("="*60)
        pasos.append(f"Integrando: {f_cyl}")
        pasos.append(f"Jacobiano: r")
        pasos.append(f"Integrando con Jacobiano: {integrand}")

        # PASO 1: Integrar respecto a z
        pasos.append("\n" + "="*60)
        pasos.append("PASO 1: Integración respecto a z")
        pasos.append("="*60)
        pasos.append(f"∫ ({integrand}) dz  con z ∈ [{z_lim[0]}, {z_lim[1]}]")
        
        f1 = sp.integrate(integrand, (z, z_lim[0], z_lim[1]))
        f1 = sp.simplify(f1)
        
        pasos.append(f"\n🔸 Resultado después de integrar en z:")
        pasos.append(f"   f₁(r,θ) = {f1}")

        # PASO 2: Integrar respecto a r
        pasos.append("\n" + "="*60)
        pasos.append("PASO 2: Integración respecto a r")
        pasos.append("="*60)
        pasos.append(f"∫ ({f1}) dr  con r ∈ [{r_lim[0]}, {r_lim[1]}]")
        
        f2 = sp.integrate(f1, (r, r_lim[0], r_lim[1]))
        f2 = sp.simplify(f2)
        
        pasos.append(f"\n🔸 Resultado después de integrar en r:")
        pasos.append(f"   f₂(θ) = {f2}")

        # PASO 3: Integrar respecto a theta
        pasos.append("\n" + "="*60)
        pasos.append("PASO 3: Integración respecto a θ")
        pasos.append("="*60)
        pasos.append(f"∫ ({f2}) dθ  con θ ∈ [{theta_lim[0]}, {theta_lim[1]}]")
        
        f3 = sp.integrate(f2, (theta, theta_lim[0], theta_lim[1]))
        f3 = sp.simplify(f3)
        
        pasos.append(f"\n🔸 Resultado final:")
        pasos.append(f"   {f3}")

        # Convertir a numérico
        valor_numerico = IntegralCalculator._convertir_a_numerico(f3)

        pasos.append("\n" + "="*60)
        pasos.append("RESULTADO FINAL")
        pasos.append("="*60)
        pasos.append(f"✅ Resultado simbólico: {f3}")
        if isinstance(f3, sp.Rational):
            pasos.append(f"✅ Forma fraccionaria: {f3.p}/{f3.q}")
        pasos.append(f"✅ Valor numérico: {valor_numerico}")

        return {
            "resultado_simbolico": f3,
            "resultado_manual": valor_numerico,
            "pasos": "\n".join(pasos)
        }

    # =========================
    # 🔹 ESFÉRICO - CORREGIDO ✅
    # =========================
    @staticmethod
    def integral_spherical(f, rho_lim, theta_lim, phi_lim):
        """
        Calcula integral triple esférica con límites variables
        CORRECCIÓN: Detecta correctamente si la función usa rho,theta,phi o x,y,z
        """
        # Definir símbolos de AMBOS sistemas
        x, y, z_cart = sp.symbols('x y z', real=True)
        rho, theta, phi = sp.symbols('rho theta phi', real=True, positive=True)
        
        pasos = ["╔═══════════════════════════════════════════════════════════════╗",
                 "║     INTEGRAL TRIPLE EN COORDENADAS ESFÉRICAS                ║",
                 "╚═══════════════════════════════════════════════════════════════╝"]
        
        # Detectar qué variables usa la función
        simbolos_func = f.free_symbols
        usa_cartesianas = any(s in simbolos_func for s in [x, y, z_cart])
        usa_esfericas = any(s in simbolos_func for s in [rho, theta, phi])
        
        f_sph = f
        
        if usa_cartesianas and not usa_esfericas:
            # Función en cartesianas → convertir
            pasos.append(f"\n📌 Función original (cartesiana): f(x,y,z) = {f}")
            pasos.append(f"📌 Conversión a esféricas:")
            pasos.append(f"   x = ρ·sin(φ)·cos(θ)")
            pasos.append(f"   y = ρ·sin(φ)·sin(θ)")
            pasos.append(f"   z = ρ·cos(φ)")
            
            f_sph = f.subs([
                (x, rho*sp.sin(phi)*sp.cos(theta)),
                (y, rho*sp.sin(phi)*sp.sin(theta)),
                (z_cart, rho*sp.cos(phi))
            ])
            f_sph = sp.simplify(f_sph)
            pasos.append(f"📌 Función en esféricas: f(ρ,θ,φ) = {f_sph}")
        else:
            # Función ya en esféricas o constante
            pasos.append(f"\n📌 Función: f(ρ,θ,φ) = {f}")
        
        pasos.extend([
            f"📌 Jacobiano esférico: ρ²·sin(φ)",
            f"📌 Límites de integración:",
            f"   • ρ: [{rho_lim[0]}] → [{rho_lim[1]}]",
            f"   • θ: [{theta_lim[0]}] → [{theta_lim[1]}]",
            f"   • φ: [{phi_lim[0]}] → [{phi_lim[1]}]",
            f"\n📌 Orden de integración: dρ dθ dφ\n"
        ])

        # Aplicar Jacobiano
        integrand = sp.simplify(f_sph * rho**2 * sp.sin(phi))
        pasos.append("="*60)
        pasos.append("PREPARACIÓN: Aplicar Jacobiano")
        pasos.append("="*60)
        pasos.append(f"Integrando: {f_sph}")
        pasos.append(f"Jacobiano: ρ²·sin(φ)")
        pasos.append(f"Integrando con Jacobiano: {integrand}")

        # PASO 1: Integrar respecto a rho
        pasos.append("\n" + "="*60)
        pasos.append("PASO 1: Integración respecto a ρ")
        pasos.append("="*60)
        pasos.append(f"∫ ({integrand}) dρ  con ρ ∈ [{rho_lim[0]}, {rho_lim[1]}]")
        
        f1 = sp.integrate(integrand, (rho, rho_lim[0], rho_lim[1]))
        f1 = sp.simplify(f1)
        
        pasos.append(f"\n🔸 Resultado después de integrar en ρ:")
        pasos.append(f"   f₁(θ,φ) = {f1}")

        # PASO 2: Integrar respecto a theta
        pasos.append("\n" + "="*60)
        pasos.append("PASO 2: Integración respecto a θ")
        pasos.append("="*60)
        pasos.append(f"∫ ({f1}) dθ  con θ ∈ [{theta_lim[0]}, {theta_lim[1]}]")
        
        f2 = sp.integrate(f1, (theta, theta_lim[0], theta_lim[1]))
        f2 = sp.simplify(f2)
        
        pasos.append(f"\n🔸 Resultado después de integrar en θ:")
        pasos.append(f"   f₂(φ) = {f2}")

        # PASO 3: Integrar respecto a phi
        pasos.append("\n" + "="*60)
        pasos.append("PASO 3: Integración respecto a φ")
        pasos.append("="*60)
        pasos.append(f"∫ ({f2}) dφ  con φ ∈ [{phi_lim[0]}, {phi_lim[1]}]")
        
        f3 = sp.integrate(f2, (phi, phi_lim[0], phi_lim[1]))
        f3 = sp.simplify(f3)
        
        pasos.append(f"\n🔸 Resultado final:")
        pasos.append(f"   {f3}")

        # Convertir a numérico
        valor_numerico = IntegralCalculator._convertir_a_numerico(f3)

        pasos.append("\n" + "="*60)
        pasos.append("RESULTADO FINAL")
        pasos.append("="*60)
        pasos.append(f"✅ Resultado simbólico: {f3}")
        if isinstance(f3, sp.Rational):
            pasos.append(f"✅ Forma fraccionaria: {f3.p}/{f3.q}")
        pasos.append(f"✅ Valor numérico: {valor_numerico}")

        return {
            "resultado_simbolico": f3,
            "resultado_manual": valor_numerico,
            "pasos": "\n".join(pasos)
        }


# =========================
# PRUEBAS Y VERIFICACIÓN
# =========================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("VERIFICACIÓN DE TODOS LOS SISTEMAS")
    print("="*70)
    
    x, y, z = sp.symbols('x y z', real=True)
    r, theta = sp.symbols('r theta', real=True, positive=True)
    rho, phi = sp.symbols('rho phi', real=True, positive=True)
    
    # ========== PRUEBA CILÍNDRICAS ==========
    print("\n" + "🔷"*35)
    print("PRUEBA CILÍNDRICAS: ∫∫∫ r² dV")
    print("Límites: r∈[0,2], θ∈[0,π/2], z∈[0,4-r]")
    print("🔷"*35)
    
    f_cil = r**2
    resultado_cil = IntegralCalculator.integral_cylindrical(
        f_cil,
        [0, 2],        # r: 0 → 2
        [0, sp.pi/2],  # θ: 0 → π/2
        [0, 4-r]       # z: 0 → 4-r
    )
    print(resultado_cil["pasos"])
    print(f"\n🔍 Resultado: {resultado_cil['resultado_simbolico']} = {resultado_cil['resultado_manual']}")
    
    # ========== PRUEBA ESFÉRICAS ==========
    print("\n" + "🔷"*35)
    print("PRUEBA ESFÉRICAS: Volumen de esfera unitaria")
    print("Límites: ρ∈[0,1], θ∈[0,2π], φ∈[0,π]")
    print("🔷"*35)
    
    f_esf = 1
    resultado_esf = IntegralCalculator.integral_spherical(
        f_esf,
        [0, 1],
        [0, 2*sp.pi],
        [0, sp.pi]
    )
    print(resultado_esf["pasos"])
    print(f"\n✅ Esperado: 4π/3 ≈ 4.18879")
    print(f"🔍 Obtenido: {resultado_esf['resultado_simbolico']} = {resultado_esf['resultado_manual']}")