import sympy as sp

class IntegralCalculator:
    """Calculadora de integrales triples en múltiples sistemas de coordenadas"""
    
    @staticmethod
    def _convertir_a_numerico(resultado_simbolico):
        """Convierte resultado simbólico a numérico"""
        metodos_conversion = [
            lambda x: float(x),
            lambda x: float(sp.N(x, 15)),
            lambda x: float(x.evalf(15)),
            lambda x: float(sp.simplify(x).evalf(15))
        ]
        
        for metodo in metodos_conversion:
            try:
                return metodo(resultado_simbolico)
            except Exception:
                continue
        
        return None

    @staticmethod
    def integral_rectangular(f, x_lim, y_lim, z_lim):
        """Calcula integral triple rectangular con límites variables"""
        x, y, z = sp.symbols('x y z', real=True)
        
        x_symbols = set()
        y_symbols = set()
        z_symbols = set()
        
        for lim in x_lim:
            x_symbols.update(lim.free_symbols if hasattr(lim, 'free_symbols') else set())
        for lim in y_lim:
            y_symbols.update(lim.free_symbols if hasattr(lim, 'free_symbols') else set())
        for lim in z_lim:
            z_symbols.update(lim.free_symbols if hasattr(lim, 'free_symbols') else set())
        
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
                 f"\n📌 Orden de integración detectado: {orden}\n"]

        resultado_actual = f
        
        for i, (var, lims, nombre_var) in enumerate(var_orden, 1):
            pasos.append("="*60)
            pasos.append(f"PASO {i}: Integración respecto a {nombre_var}")
            pasos.append("="*60)
            pasos.append(f"∫ ({resultado_actual}) d{nombre_var}  con {nombre_var} ∈ [{lims[0]}, {lims[1]}]")
            
            resultado_actual = sp.integrate(resultado_actual, (var, lims[0], lims[1]))
            resultado_actual = sp.simplify(resultado_actual)
            
            pasos.append(f"\n🔸 Resultado después de integrar en {nombre_var}:")
            if i < 3:
                vars_restantes = [v[2] for v in var_orden[i:]]
                pasos.append(f"   f_{i}({','.join(vars_restantes)}) = {resultado_actual}")
            else:
                pasos.append(f"   Resultado final = {resultado_actual}")

        f3 = resultado_actual
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

    @staticmethod
    def integral_cylindrical(f, r_lim, theta_lim, z_lim):
        """Calcula integral triple cilíndrica"""
        f = sp.sympify(f)
        r_lim = [sp.sympify(x) for x in r_lim]
        theta_lim = [sp.sympify(x) for x in theta_lim]
        z_lim = [sp.sympify(x) for x in z_lim]
        
        x, y, z_cart = sp.symbols('x y z', real=True)
        r, theta, z = sp.symbols('r theta z', real=True, positive=True)
        
        pasos = ["╔═══════════════════════════════════════════════════════════════╗",
                 "║     INTEGRAL TRIPLE EN COORDENADAS CILÍNDRICAS              ║",
                 "╚═══════════════════════════════════════════════════════════════╝"]
        
        simbolos_func = f.free_symbols
        usa_cartesianas = any(s in simbolos_func for s in [x, y, z_cart])
        
        f_cyl = f
        
        if usa_cartesianas:
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
            pasos.append(f"\n📌 Función: f(r,θ,z) = {f}")
        
        pasos.extend([
            f"📌 Jacobiano cilíndrico: r",
            f"📌 Límites de integración:",
            f"   • r: [{r_lim[0]}] → [{r_lim[1]}]",
            f"   • θ: [{theta_lim[0]}] → [{theta_lim[1]}]",
            f"   • z: [{z_lim[0]}] → [{z_lim[1]}]",
            f"\n📌 Orden de integración: ∫∫∫ r dz dr dθ\n"
        ])

        integrand = sp.simplify(f_cyl * r)
        pasos.append("="*60)
        pasos.append("PREPARACIÓN: Aplicar Jacobiano")
        pasos.append("="*60)
        pasos.append(f"Integrando: {f_cyl}")
        pasos.append(f"Jacobiano: r")
        pasos.append(f"Integrando con Jacobiano: {integrand}")

        pasos.append("\n" + "="*60)
        pasos.append("PASO 1: Integración respecto a z")
        pasos.append("="*60)
        pasos.append(f"∫ ({integrand}) dz  con z ∈ [{z_lim[0]}, {z_lim[1]}]")
        
        f1 = sp.integrate(integrand, (z, z_lim[0], z_lim[1]))
        f1 = sp.simplify(f1)
        
        pasos.append(f"\n🔸 Resultado después de integrar en z:")
        pasos.append(f"   f₁(r,θ) = {f1}")

        pasos.append("\n" + "="*60)
        pasos.append("PASO 2: Integración respecto a r")
        pasos.append("="*60)
        pasos.append(f"∫ ({f1}) dr  con r ∈ [{r_lim[0]}, {r_lim[1]}]")
        
        f2 = sp.integrate(f1, (r, r_lim[0], r_lim[1]))
        f2 = sp.simplify(f2)
        
        pasos.append(f"\n🔸 Resultado después de integrar en r:")
        pasos.append(f"   f₂(θ) = {f2}")

        pasos.append("\n" + "="*60)
        pasos.append("PASO 3: Integración respecto a θ")
        pasos.append("="*60)
        pasos.append(f"∫ ({f2}) dθ  con θ ∈ [{theta_lim[0]}, {theta_lim[1]}]")
        
        f3 = sp.integrate(f2, (theta, theta_lim[0], theta_lim[1]))
        f3 = sp.simplify(f3)
        
        pasos.append(f"\n🔸 Resultado final:")
        pasos.append(f"   {f3}")

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

    @staticmethod
    def integral_spherical(f, rho_lim, theta_lim, phi_lim):
        """Calcula integral triple esférica"""
        f = sp.sympify(f)
        rho_lim = [sp.sympify(x) for x in rho_lim]
        theta_lim = [sp.sympify(x) for x in theta_lim]
        phi_lim = [sp.sympify(x) for x in phi_lim]
        
        x, y, z_cart = sp.symbols('x y z', real=True)
        rho, theta, phi = sp.symbols('rho theta phi', real=True, positive=True)
        
        pasos = ["╔═══════════════════════════════════════════════════════════════╗",
                 "║     INTEGRAL TRIPLE EN COORDENADAS ESFÉRICAS                ║",
                 "╚═══════════════════════════════════════════════════════════════╝"]
        
        simbolos_func = f.free_symbols
        usa_cartesianas = any(s in simbolos_func for s in [x, y, z_cart])
        
        f_sph = f
        
        if usa_cartesianas:
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
            pasos.append(f"\n📌 Función: f(ρ,θ,φ) = {f}")
        
        pasos.extend([
            f"📌 Jacobiano esférico: ρ²·sin(φ)",
            f"📌 Límites de integración:",
            f"   • ρ: [{rho_lim[0]}] → [{rho_lim[1]}]",
            f"   • θ: [{theta_lim[0]}] → [{theta_lim[1]}]",
            f"   • φ: [{phi_lim[0]}] → [{phi_lim[1]}]",
            f"\n📌 Orden de integración: ∫∫∫ ρ²sin(φ) dρ dθ dφ\n"
        ])

        integrand = sp.simplify(f_sph * rho**2 * sp.sin(phi))
        pasos.append("="*60)
        pasos.append("PREPARACIÓN: Aplicar Jacobiano")
        pasos.append("="*60)
        pasos.append(f"Integrando: {f_sph}")
        pasos.append(f"Jacobiano: ρ²·sin(φ)")
        pasos.append(f"Integrando con Jacobiano: {integrand}")

        pasos.append("\n" + "="*60)
        pasos.append("PASO 1: Integración respecto a ρ")
        pasos.append("="*60)
        pasos.append(f"∫ ({integrand}) dρ  con ρ ∈ [{rho_lim[0]}, {rho_lim[1]}]")
        
        f1 = sp.integrate(integrand, (rho, rho_lim[0], rho_lim[1]))
        f1 = sp.simplify(f1)
        
        pasos.append(f"\n🔸 Resultado después de integrar en ρ:")
        pasos.append(f"   f₁(θ,φ) = {f1}")

        pasos.append("\n" + "="*60)
        pasos.append("PASO 2: Integración respecto a θ")
        pasos.append("="*60)
        pasos.append(f"∫ ({f1}) dθ  con θ ∈ [{theta_lim[0]}, {theta_lim[1]}]")
        
        f2 = sp.integrate(f1, (theta, theta_lim[0], theta_lim[1]))
        f2 = sp.simplify(f2)
        
        pasos.append(f"\n🔸 Resultado después de integrar en θ:")
        pasos.append(f"   f₂(φ) = {f2}")

        pasos.append("\n" + "="*60)
        pasos.append("PASO 3: Integración respecto a φ")
        pasos.append("="*60)
        pasos.append(f"∫ ({f2}) dφ  con φ ∈ [{phi_lim[0]}, {phi_lim[1]}]")
        
        f3 = sp.integrate(f2, (phi, phi_lim[0], phi_lim[1]))
        f3 = sp.simplify(f3)
        
        pasos.append(f"\n🔸 Resultado final:")
        pasos.append(f"   {f3}")

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


if __name__ == "__main__":
    print("Módulo integral_calculator cargado correctamente")