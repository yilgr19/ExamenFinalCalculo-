import sympy as sp
from sympy.vector import CoordSys3D, divergence, curl, gradient
import numpy as np

class VectorTheorems:
    
    @staticmethod
    def _convertir_a_numerico(resultado_simbolico):
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

    @staticmethod
    def green_theorem(P, Q, region_bounds, tipo_region="rectangular"):
        x, y = sp.symbols('x y', real=True)
        r, theta = sp.symbols('r theta', real=True)
        
        pasos = [
            "Teorema de Green",
            "Formula: Integral de linea = Integral de superficie",
            "Campo vectorial F = (P, Q):",
            f"   P(x,y) = {P}",
            f"   Q(x,y) = {Q}",
            "Calculo de derivadas parciales"
        ]
        
        dQ_dx = sp.diff(Q, x)
        dP_dy = sp.diff(P, y)
        
        pasos.extend([
            f"dQ/dx = {dQ_dx}",
            f"dP/dy = {dP_dy}"
        ])
        
        integrand = sp.simplify(dQ_dx - dP_dy)
        
        pasos.extend([
            "Calculo de (dQ/dx - dP/dy)",
            f"Integrando: {integrand}"
        ])
        
        if tipo_region == "polar":
            pasos.append("Conversion a coordenadas polares")
            
            integrand_polar = integrand.subs([
                (x, r*sp.cos(theta)),
                (y, r*sp.sin(theta))
            ])
            integrand_polar = sp.simplify(integrand_polar * r)
            
            r_lim = region_bounds['r']
            theta_lim = region_bounds['theta']
            
            pasos.append(f"Integracion respecto a r [{r_lim[0]}, {r_lim[1]}]:")
            resultado_r = sp.integrate(integrand_polar, (r, r_lim[0], r_lim[1]))
            resultado_r = sp.simplify(resultado_r)
            pasos.append(f"Resultado: {resultado_r}")
            
            pasos.append(f"Integracion respecto a theta [{theta_lim[0]}, {theta_lim[1]}]:")
            resultado_final = sp.integrate(resultado_r, (theta, theta_lim[0], theta_lim[1]))
            
        else:
            x_lim = region_bounds['x']
            y_lim = region_bounds['y']
            
            pasos.append(f"Integracion respecto a y [{y_lim[0]}, {y_lim[1]}]:")
            resultado_y = sp.integrate(integrand, (y, y_lim[0], y_lim[1]))
            resultado_y = sp.simplify(resultado_y)
            pasos.append(f"Resultado: {resultado_y}")
            
            pasos.append(f"Integracion respecto a x [{x_lim[0]}, {x_lim[1]}]:")
            resultado_final = sp.integrate(resultado_y, (x, x_lim[0], x_lim[1]))
        
        resultado_final = sp.simplify(resultado_final)
        valor_numerico = VectorTheorems._convertir_a_numerico(resultado_final)
        
        pasos.extend([
            "Resultado Final",
            f"Resultado simbolico: {resultado_final}",
            f"Valor numerico: {valor_numerico}"
        ])
        
        return {
            "resultado_simbolico": resultado_final,
            "resultado_numerico": valor_numerico,
            "pasos": "\n".join(pasos)
        }

    @staticmethod
    def stokes_theorem(F_components, surface_params, param_bounds):
        x, y, z = sp.symbols('x y z', real=True)
        u, v = sp.symbols('u v', real=True)
        
        F_x, F_y, F_z = F_components
        
        pasos = [
            "Teorema de Stokes",
            "Formula: Integral de linea = Integral de superficie",
            "Campo vectorial F = (Fx, Fy, Fz):",
            f"   Fx = {F_x}",
            f"   Fy = {F_y}",
            f"   Fz = {F_z}",
            "Calculo del rotacional"
        ]
        
        curl_x = sp.diff(F_z, y) - sp.diff(F_y, z)
        curl_y = sp.diff(F_x, z) - sp.diff(F_z, x)
        curl_z = sp.diff(F_y, x) - sp.diff(F_x, y)
        
        pasos.extend([
            "Rotacional (curl) de F:",
            f"(curl F)_x = {curl_x}",
            f"(curl F)_y = {curl_y}",
            f"(curl F)_z = {curl_z}"
        ])
        
        pasos.append("Parametrizacion de la superficie")
        
        r_u = [sp.diff(param, u) for param in surface_params]
        r_v = [sp.diff(param, v) for param in surface_params]
        
        pasos.extend([
            f"dr/du = {r_u}",
            f"dr/dv = {r_v}"
        ])
        
        n_x = r_u[1]*r_v[2] - r_u[2]*r_v[1]
        n_y = r_u[2]*r_v[0] - r_u[0]*r_v[2]
        n_z = r_u[0]*r_v[1] - r_u[1]*r_v[0]
        
        pasos.append(f"Vector normal n = {sp.simplify(n_x)}, {sp.simplify(n_y)}, {sp.simplify(n_z)}")
        
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
        
        dot_product = sp.simplify(
            curl_x_param * n_x + curl_y_param * n_y + curl_z_param * n_z
        )
        
        pasos.append(f"(curl F)·n = {dot_product}")
        
        u_lim = param_bounds['u']
        v_lim = param_bounds['v']
        
        pasos.append(f"Integracion respecto a v [{v_lim[0]}, {v_lim[1]}]:")
        resultado_v = sp.integrate(dot_product, (v, v_lim[0], v_lim[1]))
        resultado_v = sp.simplify(resultado_v)
        pasos.append(f"Resultado: {resultado_v}")
        
        pasos.append(f"Integracion respecto a u [{u_lim[0]}, {u_lim[1]}]:")
        resultado_final = sp.integrate(resultado_v, (u, u_lim[0], u_lim[1]))
        resultado_final = sp.simplify(resultado_final)
        
        valor_numerico = VectorTheorems._convertir_a_numerico(resultado_final)
        
        pasos.extend([
            "Resultado Final",
            f"Resultado simbolico: {resultado_final}",
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
        x, y, z = sp.symbols('x y z', real=True)
        r, theta = sp.symbols('r theta', real=True, positive=True)
        rho, phi = sp.symbols('rho phi', real=True, positive=True)
        
        F_x, F_y, F_z = F_components
        
        pasos = [
            "Teorema de la Divergencia (Gauss)",
            "Formula: Integral de superficie = Integral de volumen",
            "Campo vectorial F = (Fx, Fy, Fz):",
            f"   Fx = {F_x}",
            f"   Fy = {F_y}",
            f"   Fz = {F_z}",
            "Calculo de la divergencia"
        ]
        
        div_F = sp.diff(F_x, x) + sp.diff(F_y, y) + sp.diff(F_z, z)
        div_F = sp.simplify(div_F)
        
        pasos.extend([
            "Divergencia de F:",
            f"div F = {div_F}"
        ])
        
        if region_type == "spherical":
            pasos.append("Conversion a coordenadas esfericas")
            
            div_F_sph = div_F.subs([
                (x, rho*sp.sin(phi)*sp.cos(theta)),
                (y, rho*sp.sin(phi)*sp.sin(theta)),
                (z, rho*sp.cos(phi))
            ])
            integrand = sp.simplify(div_F_sph * rho**2 * sp.sin(phi))
            
            pasos.append(f"Integrando: {integrand}")
            
            rho_lim = bounds['rho']
            theta_lim = bounds['theta']
            phi_lim = bounds['phi']
            
            pasos.append(f"Integracion respecto a phi [{phi_lim[0]}, {phi_lim[1]}]:")
            try:
                integrand_expandido = sp.expand(integrand)
                resultado = sp.integrate(integrand_expandido, (phi, phi_lim[0], phi_lim[1]))
                resultado = sp.simplify(resultado)
                pasos.append(f"Resultado: {resultado}")
            except Exception as e:
                pasos.append(f"Error en integracion de phi: {e}")
                try:
                    resultado = sp.integrate(integrand, (phi, phi_lim[0], phi_lim[1]))
                    resultado = resultado.evalf()
                    pasos.append(f"Resultado (numerico): {resultado}")
                except:
                    resultado = integrand
            
            pasos.append(f"Integracion respecto a theta [{theta_lim[0]}, {theta_lim[1]}]:")
            try:
                resultado_expandido = sp.expand(resultado)
                resultado = sp.integrate(resultado_expandido, (theta, theta_lim[0], theta_lim[1]))
                resultado = sp.simplify(resultado)
                pasos.append(f"Resultado: {resultado}")
            except Exception as e:
                pasos.append(f"Error en integracion de theta: {e}")
                try:
                    resultado = sp.integrate(resultado, (theta, theta_lim[0], theta_lim[1]))
                    resultado = resultado.evalf()
                    pasos.append(f"Resultado (numerico): {resultado}")
                except:
                    pass
            
            pasos.append(f"Integracion respecto a rho [{rho_lim[0]}, {rho_lim[1]}]:")
            try:
                resultado_expandido = sp.expand(resultado)
                resultado_final = sp.integrate(resultado_expandido, (rho, rho_lim[0], rho_lim[1]))
                resultado_final = sp.simplify(resultado_final)
                pasos.append(f"Resultado: {resultado_final}")
            except Exception as e:
                pasos.append(f"Error en integracion de rho: {e}")
                try:
                    resultado_final = sp.integrate(resultado, (rho, rho_lim[0], rho_lim[1]))
                    resultado_final = resultado_final.evalf()
                    pasos.append(f"Resultado (numerico): {resultado_final}")
                except:
                    resultado_final = resultado
            
        elif region_type == "cylindrical":
            pasos.append("Conversion a coordenadas cilindricas")
            
            div_F_cyl = div_F.subs([
                (x, r*sp.cos(theta)),
                (y, r*sp.sin(theta))
            ])
            integrand = sp.simplify(div_F_cyl * r)
            
            pasos.append(f"Integrando: {integrand}")
            
            r_lim = bounds['r']
            theta_lim = bounds['theta']
            z_lim = bounds['z']
            
            pasos.append(f"Integracion respecto a z [{z_lim[0]}, {z_lim[1]}]:")
            resultado = sp.integrate(integrand, (z, z_lim[0], z_lim[1]))
            resultado = sp.simplify(resultado)
            pasos.append(f"Resultado: {resultado}")
            
            pasos.append(f"Integracion respecto a theta [{theta_lim[0]}, {theta_lim[1]}]:")
            resultado = sp.integrate(resultado, (theta, theta_lim[0], theta_lim[1]))
            resultado = sp.simplify(resultado)
            pasos.append(f"Resultado: {resultado}")
            
            pasos.append(f"Integracion respecto a r [{r_lim[0]}, {r_lim[1]}]:")
            resultado_final = sp.integrate(resultado, (r, r_lim[0], r_lim[1]))
            
        else:
            x_lim = bounds['x']
            y_lim = bounds['y']
            z_lim = bounds['z']
            
            pasos.append(f"Integracion respecto a z [{z_lim[0]}, {z_lim[1]}]:")
            resultado = sp.integrate(div_F, (z, z_lim[0], z_lim[1]))
            resultado = sp.simplify(resultado)
            pasos.append(f"Resultado: {resultado}")
            
            pasos.append(f"Integracion respecto a y [{y_lim[0]}, {y_lim[1]}]:")
            resultado = sp.integrate(resultado, (y, y_lim[0], y_lim[1]))
            resultado = sp.simplify(resultado)
            pasos.append(f"Resultado: {resultado}")
            
            pasos.append(f"Integracion respecto a x [{x_lim[0]}, {x_lim[1]}]:")
            resultado_final = sp.integrate(resultado, (x, x_lim[0], x_lim[1]))
        
        resultado_final = sp.simplify(resultado_final)
        valor_numerico = VectorTheorems._convertir_a_numerico(resultado_final)
        
        pasos.extend([
            "Resultado Final",
            f"Resultado simbolico: {resultado_final}",
            f"Valor numerico: {valor_numerico}"
        ])
        
        return {
            "resultado_simbolico": resultado_final,
            "resultado_numerico": valor_numerico,
            "divergencia": div_F,
            "pasos": "\n".join(pasos)
        }


if __name__ == "__main__":
    print("="*70)
    print("PRUEBAS DE TEOREMAS VECTORIALES")
    print("="*70)
    
    x, y, z = sp.symbols('x y z', real=True)
    
    print("\nEJEMPLO: TEOREMA DE GREEN")
    
    P = -y
    Q = x
    region = {'x': [0, 1], 'y': [0, 1]}
    
    resultado_green = VectorTheorems.green_theorem(P, Q, region, "rectangular")
    print(resultado_green["pasos"])
    
    print("\nEJEMPLO: TEOREMA DE STOKES")
    
    F = [y, -x, z]
    u, v = sp.symbols('u v', real=True)
    superficie = [u*sp.cos(v), u*sp.sin(v), 1 - u**2]
    limites = {'u': [0, 1], 'v': [0, 2*sp.pi]}
    
    resultado_stokes = VectorTheorems.stokes_theorem(F, superficie, limites)
    print(resultado_stokes["pasos"])
    
    print("\nEJEMPLO: TEOREMA DE LA DIVERGENCIA")
    
    F = [x, y, z]
    bounds = {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]}
    
    resultado_div = VectorTheorems.divergence_theorem(F, "rectangular", bounds)
    print(resultado_div["pasos"])