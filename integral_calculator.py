import sympy as sp

class IntegralCalculator:
    # =========================
    # 🔹 RECTANGULAR
    # =========================
    @staticmethod
    def integral_rectangular(f, x_lim, y_lim, z_lim):
        x, y, z = sp.symbols('x y z', real=True)
        pasos = ["╔═══════════════════════════════════════════════════════════════╗",
                 "║     INTEGRAL TRIPLE EN COORDENADAS RECTANGULARES             ║",
                 "╚═══════════════════════════════════════════════════════════════╝",
                 f"\n📌 f(x,y,z) = {f}",
                 "📌 Orden: dz dy dx\n"]

        # Integración paso a paso
        f1 = sp.integrate(f, (z, z_lim[0], z_lim[1]))
        pasos.append(f"1️⃣ ∫[z] f dz = {f1}")

        f2 = sp.integrate(f1, (y, y_lim[0], y_lim[1]))
        pasos.append(f"2️⃣ ∫[y] (resultado) dy = {f2}")

        f3 = sp.integrate(f2, (x, x_lim[0], x_lim[1]))
        pasos.append(f"3️⃣ ∫[x] (resultado) dx = {f3}")

        pasos.append(f"\n✅ Resultado simbólico: {f3}")
        pasos.append(f"✅ Valor numérico: {float(f3.evalf()) if f3.is_real else None}")

        return {
            "resultado_simbolico": f3,
            "resultado_manual": float(f3.evalf()) if f3.is_real else None,
            "pasos": "\n".join(pasos)
        }

    # =========================
    # 🔹 CILÍNDRICO
    # =========================
    @staticmethod
    def integral_cylindrical(f, r_lim, theta_lim, z_lim):
        r, theta, z = sp.symbols('r theta z', real=True)
        pasos = ["╔═══════════════════════════════════════════════════════════════╗",
                 "║     INTEGRAL TRIPLE EN COORDENADAS CILÍNDRICAS              ║",
                 "╚═══════════════════════════════════════════════════════════════╝",
                 f"\n📌 f(r,θ,z) = {f}",
                 "📌 Jacobiano: r",
                 "📌 Orden: dz dr dθ\n"]

        integrand = f * r
        pasos.append(f"Integrando con Jacobiano: {integrand}")

        f1 = sp.integrate(integrand, (z, z_lim[0], z_lim[1]))
        pasos.append(f"1️⃣ ∫[z] f*r dz = {f1}")

        f2 = sp.integrate(f1, (r, r_lim[0], r_lim[1]))
        pasos.append(f"2️⃣ ∫[r] (resultado) dr = {f2}")

        f3 = sp.integrate(f2, (theta, theta_lim[0], theta_lim[1]))
        pasos.append(f"3️⃣ ∫[θ] (resultado) dθ = {f3}")

        pasos.append(f"\n✅ Resultado simbólico: {f3}")
        pasos.append(f"✅ Valor numérico: {float(f3.evalf()) if f3.is_real else None}")

        return {
            "resultado_simbolico": f3,
            "resultado_manual": float(f3.evalf()) if f3.is_real else None,
            "pasos": "\n".join(pasos)
        }

    # =========================
    # 🔹 ESFÉRICO
    # =========================
    @staticmethod
    def integral_spherical(f, rho_lim, theta_lim, phi_lim):
        rho, theta, phi = sp.symbols('rho theta phi', real=True, positive=True)
        pasos = ["╔═══════════════════════════════════════════════════════════════╗",
                 "║     INTEGRAL TRIPLE EN COORDENADAS ESFÉRICAS                ║",
                 "╚═══════════════════════════════════════════════════════════════╝",
                 f"\n📌 f(ρ,θ,φ) = {f}",
                 "📌 Jacobiano: ρ² sin(φ)",
                 "📌 Orden: dρ dθ dφ\n"]

        integrand = f * rho**2 * sp.sin(phi)
        pasos.append(f"Integrando con Jacobiano: {integrand}")

        f1 = sp.integrate(integrand, (rho, rho_lim[0], rho_lim[1]))
        pasos.append(f"1️⃣ ∫[ρ] f*ρ²*sin(φ) dρ = {f1}")

        f2 = sp.integrate(f1, (theta, theta_lim[0], theta_lim[1]))
        pasos.append(f"2️⃣ ∫[θ] (resultado) dθ = {f2}")

        f3 = sp.integrate(f2, (phi, phi_lim[0], phi_lim[1]))
        pasos.append(f"3️⃣ ∫[φ] (resultado) dφ = {f3}")

        pasos.append(f"\n✅ Resultado simbólico: {f3}")
        pasos.append(f"✅ Valor numérico: {float(f3.evalf()) if f3.is_real else None}")

        return {
            "resultado_simbolico": f3,
            "resultado_manual": float(f3.evalf()) if f3.is_real else None,
            "pasos": "\n".join(pasos)
        }


# =========================
# 🔹 PRUEBAS DIRECTAS (si se ejecuta solo)
# =========================
if __name__ == "__main__":
    # Prueba de la función de ejemplo
    f = sp.sympify("rho**2*sin(phi)**2")
    resultado = IntegralCalculator.integral_spherical(f, [0, 3], [0, sp.pi], [0, sp.pi/6])
    print(resultado["pasos"])
    print("\nResultado numérico:", resultado["resultado_manual"])
