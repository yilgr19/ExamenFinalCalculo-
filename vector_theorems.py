import sympy as sp
from sympy.vector import CoordSys3D, divergence, curl, gradient
import numpy as np

class VectorTheorems:
    """
    Clase para calcular Teorema de Green, Stokes y Divergencia
    con procedimientos paso a paso
    """
    
    @staticmethod
    def _convertir_a_numerico(resultado_simbolico):
        """Convierte resultado simbólico a numérico"""
        metodos = [
            lambda x: float(x),
            lambda x: float(sp.N(x, 15)),
            lambda x: float(x.evalf(15)),
            lambda x: float(sp.simplify(x).evalf(15))
        ]
        
        for metodo in metodos:
            try:
                return metodo(resultado_simbolico)
            except:
                continue
        return None

    # =====================================================
    # TEOREMA DE GREEN
    # =====================================================
    @staticmethod
    def green_theorem(P, Q, region_bounds, tipo_region="rectangular"):
        """
        Teorema de Green: ∮_C (P dx + Q dy) = ∬_R (∂Q/∂x - ∂P/∂y) dA
        
        Args:
            P: Componente P(x,y) del campo vectorial
            Q: Componente Q(x,y) del campo vectorial
            region_bounds: Límites de la región
                - rectangular: {'x': [x_min, x_max], 'y': [y_min, y_max]}
                - polar: {'r': [r_min, r_max], 'theta': [theta_min, theta_max]}
            tipo_region: "rectangular" o "polar"
        """
        x, y = sp.symbols('x y', real=True)
        r, theta = sp.symbols('r theta', real=True)
        
        pasos = [
            "╔═══════════════════════════════════════════════════════════════╗",
            "║                    TEOREMA DE GREEN                           ║",
            "╚═══════════════════════════════════════════════════════════════╝",
            "\n📌 FÓRMULA DEL TEOREMA DE GREEN:",
            "   ∮_C (P dx + Q dy) = ∬_R (∂Q/∂x - ∂P/∂y) dA",
            "\n📌 Campo vectorial F = (P, Q):",
            f"   P(x,y) = {P}",
            f"   Q(x,y) = {Q}",
            "\n" + "="*60,
            "PASO 1: Calcular derivadas parciales",
            "="*60
        ]
        
        # Calcular derivadas parciales
        dQ_dx = sp.diff(Q, x)
        dP_dy = sp.diff(P, y)
        
        pasos.extend([
            f"∂Q/∂x = ∂({Q})/∂x = {dQ_dx}",
            f"∂P/∂y = ∂({P})/∂y = {dP_dy}"
        ])
        
        # Calcular ∂Q/∂x - ∂P/∂y
        integrand = sp.simplify(dQ_dx - dP_dy)
        
        pasos.extend([
            "\n" + "="*60,
            "PASO 2: Calcular (∂Q/∂x - ∂P/∂y)",
            "="*60,
            f"∂Q/∂x - ∂P/∂y = {dQ_dx} - ({dP_dy})",
            f"            = {integrand}"
        ])
        
        # Integración según tipo de región
        if tipo_region == "polar":
            pasos.extend([
                "\n" + "="*60,
                "PASO 3: Integración en coordenadas polares",
                "="*60,
                "Conversión: x = r·cos(θ), y = r·sin(θ), dA = r dr dθ"
            ])
            
            # Sustituir a polares
            integrand_polar = integrand.subs([
                (x, r*sp.cos(theta)),
                (y, r*sp.sin(theta))
            ])
            integrand_polar = sp.simplify(integrand_polar * r)  # Jacobiano
            
            pasos.append(f"Integrando en polares: {integrand_polar}")
            
            # Integrar
            r_lim = region_bounds['r']
            theta_lim = region_bounds['theta']
            
            pasos.append(f"\nIntegración respecto a r ∈ [{r_lim[0]}, {r_lim[1]}]:")
            resultado_r = sp.integrate(integrand_polar, (r, r_lim[0], r_lim[1]))
            resultado_r = sp.simplify(resultado_r)
            pasos.append(f"Resultado: {resultado_r}")
            
            pasos.append(f"\nIntegración respecto a θ ∈ [{theta_lim[0]}, {theta_lim[1]}]:")
            resultado_final = sp.integrate(resultado_r, (theta, theta_lim[0], theta_lim[1]))
            
        else:  # rectangular
            pasos.extend([
                "\n" + "="*60,
                "PASO 3: Integración en coordenadas rectangulares",
                "="*60
            ])
            
            x_lim = region_bounds['x']
            y_lim = region_bounds['y']
            
            pasos.append(f"Integración respecto a y ∈ [{y_lim[0]}, {y_lim[1]}]:")
            resultado_y = sp.integrate(integrand, (y, y_lim[0], y_lim[1]))
            resultado_y = sp.simplify(resultado_y)
            pasos.append(f"Resultado: {resultado_y}")
            
            pasos.append(f"\nIntegración respecto a x ∈ [{x_lim[0]}, {x_lim[1]}]:")
            resultado_final = sp.integrate(resultado_y, (x, x_lim[0], x_lim[1]))
        
        resultado_final = sp.simplify(resultado_final)
        valor_numerico = VectorTheorems._convertir_a_numerico(resultado_final)
        
        pasos.extend([
            "\n" + "="*60,
            "RESULTADO FINAL",
            "="*60,
            f"✅ ∮_C (P dx + Q dy) = {resultado_final}",
            f"✅ Valor numérico: {valor_numerico}"
        ])
        
        return {
            "resultado_simbolico": resultado_final,
            "resultado_numerico": valor_numerico,
            "pasos": "\n".join(pasos)
        }

    # =====================================================
    # TEOREMA DE STOKES
    # =====================================================
    @staticmethod
    def stokes_theorem(F_components, surface_params, param_bounds):
        """
        Teorema de Stokes: ∮_C F·dr = ∬_S (∇×F)·n dS
        
        Args:
            F_components: [F_x, F_y, F_z] - componentes del campo vectorial
            surface_params: [x(u,v), y(u,v), z(u,v)] - parametrización de superficie
            param_bounds: {'u': [u_min, u_max], 'v': [v_min, v_max]}
        """
        x, y, z = sp.symbols('x y z', real=True)
        u, v = sp.symbols('u v', real=True)
        
        F_x, F_y, F_z = F_components
        
        pasos = [
            "╔═══════════════════════════════════════════════════════════════╗",
            "║                    TEOREMA DE STOKES                          ║",
            "╚═══════════════════════════════════════════════════════════════╝",
            "\n📌 FÓRMULA DEL TEOREMA DE STOKES:",
            "   ∮_C F·dr = ∬_S (∇×F)·n dS",
            "\n📌 Campo vectorial F = (F_x, F_y, F_z):",
            f"   F_x = {F_x}",
            f"   F_y = {F_y}",
            f"   F_z = {F_z}",
            "\n" + "="*60,
            "PASO 1: Calcular el rotacional ∇×F",
            "="*60
        ]
        
        # Calcular rotacional (curl)
        curl_x = sp.diff(F_z, y) - sp.diff(F_y, z)
        curl_y = sp.diff(F_x, z) - sp.diff(F_z, x)
        curl_z = sp.diff(F_y, x) - sp.diff(F_x, y)
        
        pasos.extend([
            "∇×F = |  i      j      k   |",
            "      | ∂/∂x   ∂/∂y   ∂/∂z |",
            "      | F_x    F_y    F_z  |",
            "",
            f"(∇×F)_x = ∂F_z/∂y - ∂F_y/∂z = {curl_x}",
            f"(∇×F)_y = ∂F_x/∂z - ∂F_z/∂x = {curl_y}",
            f"(∇×F)_z = ∂F_y/∂x - ∂F_x/∂y = {curl_z}"
        ])
        
        # Parametrización de superficie
        pasos.extend([
            "\n" + "="*60,
            "PASO 2: Parametrización de la superficie S",
            "="*60,
            f"r(u,v) = ({surface_params[0]}, {surface_params[1]}, {surface_params[2]})"
        ])
        
        # Calcular vectores tangentes
        r_u = [sp.diff(param, u) for param in surface_params]
        r_v = [sp.diff(param, v) for param in surface_params]
        
        pasos.extend([
            f"\n∂r/∂u = ({r_u[0]}, {r_u[1]}, {r_u[2]})",
            f"∂r/∂v = ({r_v[0]}, {r_v[1]}, {r_v[2]})"
        ])
        
        # Producto vectorial para vector normal
        n_x = r_u[1]*r_v[2] - r_u[2]*r_v[1]
        n_y = r_u[2]*r_v[0] - r_u[0]*r_v[2]
        n_z = r_u[0]*r_v[1] - r_u[1]*r_v[0]
        
        pasos.extend([
            "\n" + "="*60,
            "PASO 3: Vector normal n = ∂r/∂u × ∂r/∂v",
            "="*60,
            f"n = ({sp.simplify(n_x)}, {sp.simplify(n_y)}, {sp.simplify(n_z)})"
        ])
        
        # Sustituir parámetros en curl
        curl_x_param = curl_x.subs([
            (x, surface_params[0]),
            (y, surface_params[1]),
            (z, surface_params[2])
        ])
        curl_y_param = curl_y.subs([
            (x, surface_params[0]),
            (y, surface_params[1]),
            (z, surface_params[2])
        ])
        curl_z_param = curl_z.subs([
            (x, surface_params[0]),
            (y, surface_params[1]),
            (z, surface_params[2])
        ])
        
        # Producto punto (∇×F)·n
        dot_product = sp.simplify(
            curl_x_param * n_x + curl_y_param * n_y + curl_z_param * n_z
        )
        
        pasos.extend([
            "\n" + "="*60,
            "PASO 4: Calcular (∇×F)·n",
            "="*60,
            f"(∇×F)·n = {dot_product}"
        ])
        
        # Integración
        pasos.extend([
            "\n" + "="*60,
            "PASO 5: Integración doble",
            "="*60
        ])
        
        u_lim = param_bounds['u']
        v_lim = param_bounds['v']
        
        pasos.append(f"Integración respecto a v ∈ [{v_lim[0]}, {v_lim[1]}]:")
        resultado_v = sp.integrate(dot_product, (v, v_lim[0], v_lim[1]))
        resultado_v = sp.simplify(resultado_v)
        pasos.append(f"Resultado: {resultado_v}")
        
        pasos.append(f"\nIntegración respecto a u ∈ [{u_lim[0]}, {u_lim[1]}]:")
        resultado_final = sp.integrate(resultado_v, (u, u_lim[0], u_lim[1]))
        resultado_final = sp.simplify(resultado_final)
        
        valor_numerico = VectorTheorems._convertir_a_numerico(resultado_final)
        
        pasos.extend([
            "\n" + "="*60,
            "RESULTADO FINAL",
            "="*60,
            f"✅ ∮_C F·dr = ∬_S (∇×F)·n dS = {resultado_final}",
            f"✅ Valor numérico: {valor_numerico}"
        ])
        
        return {
            "resultado_simbolico": resultado_final,
            "resultado_numerico": valor_numerico,
            "curl": [curl_x, curl_y, curl_z],
            "pasos": "\n".join(pasos)
        }

    # =====================================================
    # TEOREMA DE LA DIVERGENCIA
    # =====================================================
    @staticmethod
    def divergence_theorem(F_components, region_type, bounds):
        """
        Teorema de la Divergencia: ∬_S F·n dS = ∭_V (∇·F) dV
        
        Args:
            F_components: [F_x, F_y, F_z]
            region_type: "rectangular", "cylindrical", "spherical"
            bounds: Límites de integración según el tipo
        """
        x, y, z = sp.symbols('x y z', real=True)
        r, theta = sp.symbols('r theta', real=True, positive=True)
        rho, phi = sp.symbols('rho phi', real=True, positive=True)
        
        F_x, F_y, F_z = F_components
        
        pasos = [
            "╔═══════════════════════════════════════════════════════════════╗",
            "║              TEOREMA DE LA DIVERGENCIA (GAUSS)               ║",
            "╚═══════════════════════════════════════════════════════════════╝",
            "\n📌 FÓRMULA DEL TEOREMA DE LA DIVERGENCIA:",
            "   ∬_S F·n dS = ∭_V (∇·F) dV",
            "\n📌 Campo vectorial F = (F_x, F_y, F_z):",
            f"   F_x = {F_x}",
            f"   F_y = {F_y}",
            f"   F_z = {F_z}",
            "\n" + "="*60,
            "PASO 1: Calcular la divergencia ∇·F",
            "="*60
        ]
        
        # Calcular divergencia
        div_F = sp.diff(F_x, x) + sp.diff(F_y, y) + sp.diff(F_z, z)
        div_F = sp.simplify(div_F)
        
        pasos.extend([
            "∇·F = ∂F_x/∂x + ∂F_y/∂y + ∂F_z/∂z",
            f"    = {sp.diff(F_x, x)} + {sp.diff(F_y, y)} + {sp.diff(F_z, z)}",
            f"    = {div_F}"
        ])
        
        # Integración según tipo de región
        if region_type == "spherical":
            pasos.extend([
                "\n" + "="*60,
                "PASO 2: Integración en coordenadas esféricas",
                "="*60,
                "x = ρ·sin(φ)·cos(θ), y = ρ·sin(φ)·sin(θ), z = ρ·cos(φ)",
                "Jacobiano: ρ²·sin(φ)"
            ])
            
            # Convertir a esféricas
            div_F_sph = div_F.subs([
                (x, rho*sp.sin(phi)*sp.cos(theta)),
                (y, rho*sp.sin(phi)*sp.sin(theta)),
                (z, rho*sp.cos(phi))
            ])
            integrand = sp.simplify(div_F_sph * rho**2 * sp.sin(phi))
            
            pasos.append(f"Integrando con Jacobiano: {integrand}")
            
            # Integrar
            rho_lim = bounds['rho']
            theta_lim = bounds['theta']
            phi_lim = bounds['phi']
            
            pasos.append(f"\nIntegración respecto a ρ ∈ [{rho_lim[0]}, {rho_lim[1]}]:")
            resultado = sp.integrate(integrand, (rho, rho_lim[0], rho_lim[1]))
            resultado = sp.simplify(resultado)
            pasos.append(f"Resultado: {resultado}")
            
            pasos.append(f"\nIntegración respecto a θ ∈ [{theta_lim[0]}, {theta_lim[1]}]:")
            resultado = sp.integrate(resultado, (theta, theta_lim[0], theta_lim[1]))
            resultado = sp.simplify(resultado)
            pasos.append(f"Resultado: {resultado}")
            
            pasos.append(f"\nIntegración respecto a φ ∈ [{phi_lim[0]}, {phi_lim[1]}]:")
            resultado_final = sp.integrate(resultado, (phi, phi_lim[0], phi_lim[1]))
            
        elif region_type == "cylindrical":
            pasos.extend([
                "\n" + "="*60,
                "PASO 2: Integración en coordenadas cilíndricas",
                "="*60,
                "x = r·cos(θ), y = r·sin(θ), z = z",
                "Jacobiano: r"
            ])
            
            # Convertir a cilíndricas
            div_F_cyl = div_F.subs([
                (x, r*sp.cos(theta)),
                (y, r*sp.sin(theta))
            ])
            integrand = sp.simplify(div_F_cyl * r)
            
            pasos.append(f"Integrando con Jacobiano: {integrand}")
            
            # Integrar
            r_lim = bounds['r']
            theta_lim = bounds['theta']
            z_lim = bounds['z']
            
            pasos.append(f"\nIntegración respecto a z ∈ [{z_lim[0]}, {z_lim[1]}]:")
            resultado = sp.integrate(integrand, (z, z_lim[0], z_lim[1]))
            resultado = sp.simplify(resultado)
            pasos.append(f"Resultado: {resultado}")
            
            pasos.append(f"\nIntegración respecto a r ∈ [{r_lim[0]}, {r_lim[1]}]:")
            resultado = sp.integrate(resultado, (r, r_lim[0], r_lim[1]))
            resultado = sp.simplify(resultado)
            pasos.append(f"Resultado: {resultado}")
            
            pasos.append(f"\nIntegración respecto a θ ∈ [{theta_lim[0]}, {theta_lim[1]}]:")
            resultado_final = sp.integrate(resultado, (theta, theta_lim[0], theta_lim[1]))
            
        else:  # rectangular
            pasos.extend([
                "\n" + "="*60,
                "PASO 2: Integración en coordenadas rectangulares",
                "="*60
            ])
            
            x_lim = bounds['x']
            y_lim = bounds['y']
            z_lim = bounds['z']
            
            pasos.append(f"Integración respecto a z ∈ [{z_lim[0]}, {z_lim[1]}]:")
            resultado = sp.integrate(div_F, (z, z_lim[0], z_lim[1]))
            resultado = sp.simplify(resultado)
            pasos.append(f"Resultado: {resultado}")
            
            pasos.append(f"\nIntegración respecto a y ∈ [{y_lim[0]}, {y_lim[1]}]:")
            resultado = sp.integrate(resultado, (y, y_lim[0], y_lim[1]))
            resultado = sp.simplify(resultado)
            pasos.append(f"Resultado: {resultado}")
            
            pasos.append(f"\nIntegración respecto a x ∈ [{x_lim[0]}, {x_lim[1]}]:")
            resultado_final = sp.integrate(resultado, (x, x_lim[0], x_lim[1]))
        
        resultado_final = sp.simplify(resultado_final)
        valor_numerico = VectorTheorems._convertir_a_numerico(resultado_final)
        
        pasos.extend([
            "\n" + "="*60,
            "RESULTADO FINAL",
            "="*60,
            f"✅ ∭_V (∇·F) dV = {resultado_final}",
            f"✅ Valor numérico: {valor_numerico}"
        ])
        
        return {
            "resultado_simbolico": resultado_final,
            "resultado_numerico": valor_numerico,
            "divergencia": div_F,
            "pasos": "\n".join(pasos)
        }


# =====================================================
# EJEMPLOS Y PRUEBAS
# =====================================================
if __name__ == "__main__":
    print("="*70)
    print("PRUEBAS DE TEOREMAS VECTORIALES")
    print("="*70)
    
    x, y, z = sp.symbols('x y z', real=True)
    
    # ========== TEOREMA DE GREEN ==========
    print("\n" + "🟢"*35)
    print("EJEMPLO: TEOREMA DE GREEN")
    print("🟢"*35)
    
    P = -y
    Q = x
    region = {'x': [0, 1], 'y': [0, 1]}
    
    resultado_green = VectorTheorems.green_theorem(P, Q, region, "rectangular")
    print(resultado_green["pasos"])
    
    # ========== TEOREMA DE STOKES ==========
    print("\n" + "🔵"*35)
    print("EJEMPLO: TEOREMA DE STOKES")
    print("🔵"*35)
    
    # Campo F = (y, -x, z)
    F = [y, -x, z]
    # Superficie: z = 1 - x² - y², parametrización en cilíndricas
    u, v = sp.symbols('u v', real=True)
    superficie = [u*sp.cos(v), u*sp.sin(v), 1 - u**2]
    limites = {'u': [0, 1], 'v': [0, 2*sp.pi]}
    
    resultado_stokes = VectorTheorems.stokes_theorem(F, superficie, limites)
    print(resultado_stokes["pasos"])
    
    # ========== TEOREMA DE LA DIVERGENCIA ==========
    print("\n" + "🔴"*35)
    print("EJEMPLO: TEOREMA DE LA DIVERGENCIA")
    print("🔴"*35)
    
    # Campo F = (x, y, z)
    F = [x, y, z]
    # Región: cubo [0,1]×[0,1]×[0,1]
    bounds = {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]}
    
    resultado_div = VectorTheorems.divergence_theorem(F, "rectangular", bounds)
    print(resultado_div["pasos"])