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
        if resultado_simbolico is None:
            return None
        
        try:
            resultado_simbolico = sp.simplify(resultado_simbolico)
        except:
            pass
        
        metodos = [
            lambda x: float(x),
            lambda x: float(sp.N(x, 15)),
            lambda x: float(x.evalf(15)),
            lambda x: float(sp.simplify(x).evalf(15)),
            lambda x: float(sp.nsimplify(x).evalf(15))
        ]
        
        for metodo in metodos:
            try:
                return metodo(resultado_simbolico)
            except:
                continue
        return None

    @staticmethod
    def green_theorem(P, Q, region_bounds, tipo_region="rectangular"):
        """
        Teorema de Green: ∮_C (P dx + Q dy) = ∬_R (∂Q/∂x - ∂P/∂y) dA
        """
        x, y = sp.symbols('x y', real=True)
        r, theta = sp.symbols('r theta', real=True)
        
        pasos = [
            "Teorema de la Circulacion de Green",
            "Formula: ∮_C (P dx + Q dy) = ∬_R (∂Q/∂x - ∂P/∂y) dA",
            f"\nCampo vectorial F = (P, Q):",
            f"   P(x,y) = {P}",
            f"   Q(x,y) = {Q}",
            "\n" + "="*60,
            "PASO 1: Calcular derivadas parciales",
            "="*60
        ]
        
        dQ_dx = sp.diff(Q, x)
        dP_dy = sp.diff(P, y)
        
        pasos.extend([
            f"∂Q/∂x = {dQ_dx}",
            f"∂P/∂y = {dP_dy}"
        ])
        
        integrand = sp.simplify(dQ_dx - dP_dy)
        
        pasos.extend([
            "\n" + "="*60,
            "PASO 2: Calcular (∂Q/∂x - ∂P/∂y)",
            "="*60,
            f"∂Q/∂x - ∂P/∂y = {dQ_dx} - ({dP_dy})",
            f"            = {integrand}"
        ])
        
        if tipo_region == "polar":
            pasos.extend([
                "\n" + "="*60,
                "PASO 3: Integracion en coordenadas polares",
                "="*60,
                "Conversion: x = r·cos(θ), y = r·sin(θ), dA = r dr dθ"
            ])
            
            integrand_polar = integrand.subs([
                (x, r*sp.cos(theta)),
                (y, r*sp.sin(theta))
            ])
            integrand_polar = sp.simplify(integrand_polar * r)
            
            pasos.append(f"Integrando en polares: {integrand_polar}")
            
            r_lim = region_bounds['r']
            theta_lim = region_bounds['theta']
            
            pasos.append(f"\nIntegracion respecto a r ∈ [{r_lim[0]}, {r_lim[1]}]:")
            resultado_r = sp.integrate(integrand_polar, (r, r_lim[0], r_lim[1]))
            resultado_r = sp.simplify(resultado_r)
            pasos.append(f"Resultado: {resultado_r}")
            
            pasos.append(f"\nIntegracion respecto a θ ∈ [{theta_lim[0]}, {theta_lim[1]}]:")
            resultado_final = sp.integrate(resultado_r, (theta, theta_lim[0], theta_lim[1]))
            
        else:
            pasos.extend([
                "\n" + "="*60,
                "PASO 3: Integracion en coordenadas rectangulares",
                "="*60
            ])
            
            x_lim = region_bounds['x']
            y_lim = region_bounds['y']
            
            pasos.append(f"Integracion respecto a y ∈ [{y_lim[0]}, {y_lim[1]}]:")
            resultado_y = sp.integrate(integrand, (y, y_lim[0], y_lim[1]))
            resultado_y = sp.simplify(resultado_y)
            pasos.append(f"Resultado: {resultado_y}")
            
            pasos.append(f"\nIntegracion respecto a x ∈ [{x_lim[0]}, {x_lim[1]}]:")
            resultado_final = sp.integrate(resultado_y, (x, x_lim[0], x_lim[1]))
        
        resultado_final = sp.simplify(resultado_final)
        valor_numerico = VectorTheorems._convertir_a_numerico(resultado_final)
        
        pasos.extend([
            "\n" + "="*60,
            "RESULTADO FINAL",
            "="*60,
            f"Circulacion: ∮_C (P dx + Q dy) = {resultado_final}",
            f"Valor numerico: {valor_numerico}"
        ])
        
        return {
            "resultado_simbolico": resultado_final,
            "resultado_numerico": valor_numerico,
            "pasos": "\n".join(pasos)
        }

    @staticmethod
    def stokes_theorem(F_components, surface_params, param_bounds):
        """
        Teorema de Stokes: ∮_C F·dr = ∬_S (∇×F)·n dS
        """
        x, y, z = sp.symbols('x y z', real=True)
        u, v = sp.symbols('u v', real=True)
        
        F_x, F_y, F_z = F_components
        
        pasos = [
            "Teorema de Stokes",
            "Formula: ∮_C F·dr = ∬_S (∇×F)·n dS",
            f"\nCampo vectorial F = (F_x, F_y, F_z):",
            f"   F_x = {F_x}",
            f"   F_y = {F_y}",
            f"   F_z = {F_z}",
            "\n" + "="*60,
            "PASO 1: Calcular el rotacional ∇×F",
            "="*60
        ]
        
        curl_x = sp.diff(F_z, y) - sp.diff(F_y, z)
        curl_y = sp.diff(F_x, z) - sp.diff(F_z, x)
        curl_z = sp.diff(F_y, x) - sp.diff(F_x, y)
        
        pasos.extend([
            "(∇×F)_x = ∂F_z/∂y - ∂F_y/∂z = " + str(curl_x),
            "(∇×F)_y = ∂F_x/∂z - ∂F_z/∂x = " + str(curl_y),
            "(∇×F)_z = ∂F_y/∂x - ∂F_x/∂y = " + str(curl_z)
        ])
        
        pasos.extend([
            "\n" + "="*60,
            "PASO 2: Parametrizacion de la superficie S",
            "="*60,
            f"r(u,v) = ({surface_params[0]}, {surface_params[1]}, {surface_params[2]})"
        ])
        
        r_u = [sp.diff(param, u) for param in surface_params]
        r_v = [sp.diff(param, v) for param in surface_params]
        
        n_x = r_u[1]*r_v[2] - r_u[2]*r_v[1]
        n_y = r_u[2]*r_v[0] - r_u[0]*r_v[2]
        n_z = r_u[0]*r_v[1] - r_u[1]*r_v[0]
        
        pasos.append("\n" + "="*60)
        pasos.append("PASO 3: Calcular (∇×F)·n")
        pasos.append("="*60)
        
        curl_x_param = curl_x.subs([(x, surface_params[0]), (y, surface_params[1]), (z, surface_params[2])])
        curl_y_param = curl_y.subs([(x, surface_params[0]), (y, surface_params[1]), (z, surface_params[2])])
        curl_z_param = curl_z.subs([(x, surface_params[0]), (y, surface_params[1]), (z, surface_params[2])])
        
        dot_product = sp.simplify(curl_x_param * n_x + curl_y_param * n_y + curl_z_param * n_z)
        pasos.append(f"(∇×F)·n = {dot_product}")
        
        pasos.extend([
            "\n" + "="*60,
            "PASO 4: Integracion doble",
            "="*60
        ])
        
        u_lim = param_bounds['u']
        v_lim = param_bounds['v']
        
        pasos.append(f"Integracion respecto a v ∈ [{v_lim[0]}, {v_lim[1]}]:")
        resultado_v = sp.integrate(dot_product, (v, v_lim[0], v_lim[1]))
        resultado_v = sp.simplify(resultado_v)
        pasos.append(f"Resultado: {resultado_v}")
        
        pasos.append(f"\nIntegracion respecto a u ∈ [{u_lim[0]}, {u_lim[1]}]:")
        resultado_final = sp.integrate(resultado_v, (u, u_lim[0], u_lim[1]))
        resultado_final = sp.simplify(resultado_final)
        
        valor_numerico = VectorTheorems._convertir_a_numerico(resultado_final)
        
        pasos.extend([
            "\n" + "="*60,
            "RESULTADO FINAL",
            "="*60,
            f"Circulacion: ∮_C F·dr = ∬_S (∇×F)·n dS = {resultado_final}",
            f"Valor numerico: {valor_numerico}"
        ])
        
        return {
            "resultado_simbolico": resultado_final,
            "resultado_numerico": valor_numerico,
            "curl": [curl_x, curl_y, curl_z],
            "pasos": "\n".join(pasos)
        }

    @staticmethod
    def divergence_theorem(F_components, region_type, bounds):
        """
        Teorema de la Divergencia: ∬_S F·n dS = ∭_V (∇·F) dV
        """
        x, y, z = sp.symbols('x y z', real=True)
        r, theta = sp.symbols('r theta', real=True, positive=True)
        rho, phi = sp.symbols('rho phi', real=True, positive=True)
        
        F_x, F_y, F_z = F_components
        
        pasos = [
            "Teorema de la Divergencia (GAUSS)",
            "Formula: Integral de superficie = Integral de volumen",
            "∬_S F·n dS = ∭_V (∇·F) dV",
            f"\nCampo vectorial F = (F_x, F_y, F_z):",
            f"   F_x = {F_x}",
            f"   F_y = {F_y}",
            f"   F_z = {F_z}",
            "\n" + "="*60,
            "PASO 1: Calcular la divergencia ∇·F",
            "="*60
        ]
        
        div_F = sp.diff(F_x, x) + sp.diff(F_y, y) + sp.diff(F_z, z)
        div_F = sp.simplify(div_F)
        
        pasos.extend([
            "∇·F = ∂F_x/∂x + ∂F_y/∂y + ∂F_z/∂z",
            f"    = {sp.diff(F_x, x)} + {sp.diff(F_y, y)} + {sp.diff(F_z, z)}",
            f"    = {div_F}"
        ])
        
        if region_type == "spherical":
            pasos.extend([
                "\n" + "="*60,
                "PASO 2: Integracion en coordenadas esfericas",
                "="*60,
                "Conversion: x = ρ·sin(φ)·cos(θ), y = ρ·sin(φ)·sin(θ), z = ρ·cos(φ)",
                "Jacobiano: ρ²·sin(φ)"
            ])
            
            div_F_sph = div_F.subs([
                (x, rho*sp.sin(phi)*sp.cos(theta)),
                (y, rho*sp.sin(phi)*sp.sin(theta)),
                (z, rho*sp.cos(phi))
            ])
            integrand = sp.simplify(div_F_sph * rho**2 * sp.sin(phi))
            
            pasos.append(f"Divergencia en esfericas: {div_F_sph}")
            pasos.append(f"Integrando con Jacobiano: {integrand}")
            
            rho_lim = bounds['rho']
            theta_lim = bounds['theta']
            phi_lim = bounds['phi']
            
            pasos.append(f"\n" + "="*60)
            pasos.append(f"PASO 3: Integraciones sucesivas")
            pasos.append(f"="*60)
            pasos.append(f"\nIntegracion respecto a ρ ∈ [{rho_lim[0]}, {rho_lim[1]}]:")
            
            try:
                f1 = sp.integrate(integrand, (rho, rho_lim[0], rho_lim[1]))
                f1 = sp.simplify(f1)
                pasos.append(f"Resultado: {f1}")
                
                pasos.append(f"\nIntegracion respecto a θ ∈ [{theta_lim[0]}, {theta_lim[1]}]:")
                f2 = sp.integrate(f1, (theta, theta_lim[0], theta_lim[1]))
                f2 = sp.simplify(f2)
                pasos.append(f"Resultado: {f2}")
                
                pasos.append(f"\nIntegracion respecto a φ ∈ [{phi_lim[0]}, {phi_lim[1]}]:")
                resultado_final = sp.integrate(f2, (phi, phi_lim[0], phi_lim[1]))
                resultado_final = sp.simplify(resultado_final)
                pasos.append(f"Resultado: {resultado_final}")
            except Exception as e:
                pasos.append(f"Error en integracion: {str(e)}")
                resultado_final = integrand
        
        elif region_type == "cylindrical":
            pasos.extend([
                "\n" + "="*60,
                "PASO 2: Integracion en coordenadas cilindricas",
                "="*60,
                "Conversion: x = r·cos(θ), y = r·sin(θ), z = z",
                "Jacobiano: r"
            ])
            
            div_F_cyl = div_F.subs([
                (x, r*sp.cos(theta)),
                (y, r*sp.sin(theta))
            ])
            integrand = sp.simplify(div_F_cyl * r)
            
            pasos.append(f"Integrando con Jacobiano: {integrand}")
            
            r_lim = bounds['r']
            theta_lim = bounds['theta']
            z_lim = bounds['z']
            
            pasos.append(f"\nIntegracion respecto a z ∈ [{z_lim[0]}, {z_lim[1]}]:")
            f1 = sp.integrate(integrand, (z, z_lim[0], z_lim[1]))
            f1 = sp.simplify(f1)
            pasos.append(f"Resultado: {f1}")
            
            pasos.append(f"\nIntegracion respecto a θ ∈ [{theta_lim[0]}, {theta_lim[1]}]:")
            f2 = sp.integrate(f1, (theta, theta_lim[0], theta_lim[1]))
            f2 = sp.simplify(f2)
            pasos.append(f"Resultado: {f2}")
            
            pasos.append(f"\nIntegracion respecto a r ∈ [{r_lim[0]}, {r_lim[1]}]:")
            resultado_final = sp.integrate(f2, (r, r_lim[0], r_lim[1]))
            resultado_final = sp.simplify(resultado_final)
            pasos.append(f"Resultado: {resultado_final}")
        
        else:
            pasos.extend([
                "\n" + "="*60,
                "PASO 2: Integracion en coordenadas rectangulares",
                "="*60
            ])
            
            x_lim = bounds['x']
            y_lim = bounds['y']
            z_lim = bounds['z']
            
            pasos.append(f"Integracion respecto a z ∈ [{z_lim[0]}, {z_lim[1]}]:")
            f1 = sp.integrate(div_F, (z, z_lim[0], z_lim[1]))
            f1 = sp.simplify(f1)
            pasos.append(f"Resultado: {f1}")
            
            pasos.append(f"\nIntegracion respecto a y ∈ [{y_lim[0]}, {y_lim[1]}]:")
            f2 = sp.integrate(f1, (y, y_lim[0], y_lim[1]))
            f2 = sp.simplify(f2)
            pasos.append(f"Resultado: {f2}")
            
            pasos.append(f"\nIntegracion respecto a x ∈ [{x_lim[0]}, {x_lim[1]}]:")
            resultado_final = sp.integrate(f2, (x, x_lim[0], x_lim[1]))
            resultado_final = sp.simplify(resultado_final)
            pasos.append(f"Resultado: {resultado_final}")
        
        resultado_final = sp.simplify(resultado_final)
        valor_numerico = VectorTheorems._convertir_a_numerico(resultado_final)
        
        pasos.extend([
            "\n" + "="*60,
            "RESULTADO FINAL",
            "="*60,
            f"Flujo: ∭_V (∇·F) dV = {resultado_final}",
            f"Valor numerico: {valor_numerico}"
        ])
        
        return {
            "resultado_simbolico": resultado_final,
            "resultado_numerico": valor_numerico,
            "divergencia": div_F,
            "pasos": "\n".join(pasos)
        }


if __name__ == "__main__":
    print("Modulo vector_theorems cargado correctamente")