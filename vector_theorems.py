import sympy as sp
import sys

# Definición de Símbolos SimPy Globales para TODO el proyecto
# Esto asegura que P en gui.py y P en vector_theorems.py compartan la misma variable 'x', 'y', etc.
# Esto se hace aquí para evitar re-creación en cada llamada a la clase.
try:
    x, y, z = sp.symbols('x y z', real=True)
    r, theta = sp.symbols('r theta', real=True, positive=True) # r, theta para cilíndricas/polares
    rho, phi = sp.symbols('rho phi', real=True, positive=True) # rho, phi para esféricas
    u, v = sp.symbols('u v', real=True)
except Exception as e:
    # Si falla la definición, salir con error
    sys.stderr.write(f"Error fatal al definir símbolos SymPy: {e}\n")
    sys.exit(1)


class VectorTheorems:
    
    # -------------------------------------------------------------------------
    # Símbolos referenciados desde la definición global superior
    # -------------------------------------------------------------------------
    x, y, z = x, y, z
    r, theta = r, theta
    rho, phi = rho, phi
    u, v = u, v
    
    # -------------------------------------------------------------------------
    # TEOREMA DE GREEN
    # -------------------------------------------------------------------------
    @staticmethod
    def green_theorem(P, Q, bounds, coord_system="rectangular"):
        # 1. Calcular Curl 2D: ∂Q/∂x - ∂P/∂y
        curl_2d = sp.diff(Q, VectorTheorems.x) - sp.diff(P, VectorTheorems.y)
        
        # 2. Configurar la integral
        if coord_system == "polar":
            # Coordenadas polares: dA = r dr d(theta)
            integrand = curl_2d.subs([
                (VectorTheorems.x, VectorTheorems.r * sp.cos(VectorTheorems.theta)),
                (VectorTheorems.y, VectorTheorems.r * sp.sin(VectorTheorems.theta))
            ])
            integrand = sp.simplify(integrand * VectorTheorems.r) # Multiplicar por Jacobiano r
            
            limits = [
                (VectorTheorems.theta, bounds['theta'][0], bounds['theta'][1]),
                (VectorTheorems.r, bounds['r'][0], bounds['r'][1])
            ]
        else: # Rectangular
            integrand = curl_2d
            limits = [
                (VectorTheorems.y, bounds['y'][0], bounds['y'][1]),
                (VectorTheorems.x, bounds['x'][0], bounds['x'][1])
            ]
        
        # 3. Integrar
        try:
            integral_result = sp.integrate(integrand, *limits)
            integral_result_num = float(integral_result.evalf())
        except Exception as e:
            integral_result = f"Error de integración: {e}"
            integral_result_num = "N/A"
            
        pasos = f"Diferencial: ∂Q/∂x - ∂P/∂y = {curl_2d}\n"
        pasos += f"Sistema: {coord_system.capitalize()}\n"
        if coord_system == "polar":
             pasos += f"Integrando (polar, incluyendo r): {integrand}\n"
        else:
             pasos += f"Integrando: {integrand}\n"
        pasos += f"Límites de integración: {limits}\n"
        pasos += f"Resultado Simbólico: {integral_result}\n"
        pasos += f"Valor Numérico: {integral_result_num}"
        
        return {"resultado": integral_result, "pasos": pasos}

    # -------------------------------------------------------------------------
    # TEOREMA DE STOKES
    # -------------------------------------------------------------------------
    @staticmethod
    def stokes_theorem(F, r_vec, bounds):
        Fx, Fy, Fz = F
        x_param, y_param, z_param = r_vec
        
        # 1. Calcular el Rotacional (Curl)
        F_sympy = [Fx, Fy, Fz]
        nabla = sp.Matrix([sp.diff(Fz, VectorTheorems.y) - sp.diff(Fy, VectorTheorems.z),
                           sp.diff(Fx, VectorTheorems.z) - sp.diff(Fz, VectorTheorems.x),
                           sp.diff(Fy, VectorTheorems.x) - sp.diff(Fx, VectorTheorems.y)])
        
        curl = sp.simplify(nabla)
        
        # 2. Parametrización y Jacobiano
        r_uv = sp.Matrix([x_param, y_param, z_param])
        
        r_u = sp.diff(r_uv, VectorTheorems.u)
        r_v = sp.diff(r_uv, VectorTheorems.v)
        
        # Vector Normal N = r_u x r_v
        N = r_u.cross(r_v)
        
        # 3. Sustitución y Producto Punto (∇×F) · N
        curl_subs = curl.subs([
            (VectorTheorems.x, x_param),
            (VectorTheorems.y, y_param),
            (VectorTheorems.z, z_param)
        ])
        
        integrand = sp.simplify(curl_subs.dot(N))
        
        # 4. Integración
        limits = [
            (VectorTheorems.v, bounds['v'][0], bounds['v'][1]),
            (VectorTheorems.u, bounds['u'][0], bounds['u'][1])
        ]
        
        try:
            integral_result = sp.integrate(integrand, *limits)
            integral_result_num = float(integral_result.evalf())
        except Exception as e:
            integral_result = f"Error de integración: {e}"
            integral_result_num = "N/A"

        pasos = f"Campo F = ({Fx}, {Fy}, {Fz})\n"
        pasos += f"Rotacional ∇×F = ({curl[0]}, {curl[1]}, {curl[2]})\n"
        pasos += f"Vector Normal N = ({N[0]}, {N[1]}, {N[2]})\n"
        pasos += f"Integrando (∇×F) · N: {integrand}\n"
        pasos += f"Límites de integración: {limits}\n"
        pasos += f"Resultado Simbólico: {integral_result}\n"
        pasos += f"Valor Numérico: {integral_result_num}"
        
        return {"resultado": integral_result, "pasos": pasos}

    # -------------------------------------------------------------------------
    # TEOREMA DE LA DIVERGENCIA
    # -------------------------------------------------------------------------
    @staticmethod
    def divergence_theorem(F, coord_system, bounds):
        Fx, Fy, Fz = F
        
        # 1. Calcular la Divergencia (∇·F)
        if coord_system == "rectangular":
            div_F = sp.diff(Fx, VectorTheorems.x) + sp.diff(Fy, VectorTheorems.y) + sp.diff(Fz, VectorTheorems.z)
            variables = [VectorTheorems.z, VectorTheorems.y, VectorTheorems.x]
            pasos_div = f"Divergencia de F (Cartesiana):\n div F = {div_F}\n"
            integrand = div_F
            
        elif coord_system == "cylindrical":
            # Asume Fx, Fy, Fz son funciones de r, theta, z
            F_r, F_theta, F_z = Fx, Fy, Fz 
            
            # Fórmula de la Divergencia en Coordenadas Cilíndricas
            div_F = sp.diff(F_r*VectorTheorems.r, VectorTheorems.r) / VectorTheorems.r + \
                    sp.diff(F_theta, VectorTheorems.theta) / VectorTheorems.r + \
                    sp.diff(F_z, VectorTheorems.z)
                    
            div_F = sp.simplify(div_F)
            variables = [VectorTheorems.z, VectorTheorems.theta, VectorTheorems.r]
            pasos_div = f"Divergencia de F (Cilíndricas):\n div F = {div_F}\n"
            integrand = sp.simplify(div_F * VectorTheorems.r) # Multiplicar por Jacobiano r

        elif coord_system == "spherical":
            # Asume Fx, Fy, Fz son las componentes F_rho, F_phi, F_theta
            F_rho, F_phi, F_theta = Fx, Fy, Fz 
            
            # Fórmula de la Divergencia en Coordenadas Esféricas
            div_F = 1 / (VectorTheorems.rho**2 * sp.sin(VectorTheorems.phi)) * (
                sp.diff(VectorTheorems.rho**2 * F_rho * sp.sin(VectorTheorems.phi), VectorTheorems.rho) +
                sp.diff(VectorTheorems.rho * F_phi * sp.sin(VectorTheorems.phi), VectorTheorems.phi) +
                sp.diff(VectorTheorems.rho * F_theta, VectorTheorems.theta) # Corregida la derivada de F_theta
            )

            # Simplificar para obtener el 5*rho^2 esperado del ejemplo
            div_F = sp.simplify(div_F)
            variables = [VectorTheorems.rho, VectorTheorems.phi, VectorTheorems.theta]

            pasos_div = f"Divergencia de F (Esféricas, componentes Fρ, Fφ, Fθ):\n div F = {div_F}\n"
            
            # Jacobiano Esférico: rho^2 * sin(phi)
            integrand = sp.simplify(div_F * VectorTheorems.rho**2 * sp.sin(VectorTheorems.phi))

        else:
            raise ValueError("Sistema de coordenadas no soportado.")
            
        # 2. Configurar límites
        if coord_system == "spherical":
            limits = [
                (VectorTheorems.theta, bounds['theta'][0], bounds['theta'][1]),
                (VectorTheorems.phi, bounds['phi'][0], bounds['phi'][1]),
                (VectorTheorems.rho, bounds['rho'][0], bounds['rho'][1])
            ]
        elif coord_system == "cylindrical":
             limits = [
                (VectorTheorems.z, bounds['z'][0], bounds['z'][1]),
                (VectorTheorems.theta, bounds['theta'][0], bounds['theta'][1]),
                (VectorTheorems.r, bounds['r'][0], bounds['r'][1])
            ]
        else: # Rectangular
            limits = [
                (VectorTheorems.z, bounds['z'][0], bounds['z'][1]),
                (VectorTheorems.y, bounds['y'][0], bounds['y'][1]),
                (VectorTheorems.x, bounds['x'][0], bounds['x'][1])
            ]

        # 3. Integrar
        try:
            integral_result = sp.integrate(integrand, *limits)
            integral_result_num = float(integral_result.evalf())
        except Exception as e:
            integral_result = f"Error de integración: {e}"
            integral_result_num = "N/A"
            
        pasos = pasos_div
        pasos += f"Integrando (incluyendo Jacobiano): {integrand}\n"
        pasos += f"Límites de integración: {limits}\n"
        pasos += f"Resultado Simbólico: {integral_result}\n"
        pasos += f"Valor Numérico: {integral_result_num}"
        
        return {"resultado": integral_result, "pasos": pasos}