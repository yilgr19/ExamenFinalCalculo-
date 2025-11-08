import sympy as sp
import numpy as np

class IntegralCalculator:
    @staticmethod
    def integral_rectangular(f, x_limits, y_limits, z_limits):
        """
        Calcular integral triple en coordenadas rectangulares
        
        :param f: Función a integrar (expresión sympy)
        :param x_limits: Límites de x [x_min, x_max]
        :param y_limits: Límites de y [y_min, y_max]
        :param z_limits: Límites de z [z_min, z_max]
        :return: Valor de la integral
        """
        x, y, z = sp.symbols('x y z')
        
        # Convertir límites a funciones si son constantes
        x_min, x_max = x_limits
        y_min, y_max = y_limits
        z_min, z_max = z_limits
        
        integral = sp.integrate(f, 
                                (z, z_min, z_max), 
                                (y, y_min, y_max), 
                                (x, x_min, x_max))
        
        return integral
    
    @staticmethod
    def integral_cylindrical(f, r_limits, theta_limits, z_limits):
        """
        Calcular integral triple en coordenadas cilíndricas
        
        :param f: Función a integrar (expresión sympy)
        :param r_limits: Límites de r [r_min, r_max]
        :param theta_limits: Límites de theta [theta_min, theta_max]
        :param z_limits: Límites de z [z_min, z_max]
        :return: Valor de la integral
        """
        r, theta, z = sp.symbols('r theta z')
        
        # Convertir límites a funciones si son constantes
        r_min, r_max = r_limits
        theta_min, theta_max = theta_limits
        z_min, z_max = z_limits
        
        # Factor de Jacobiano para coordenadas cilíndricas: r
        jacobiano = r
        integral_con_jacobiano = f * jacobiano
        
        integral = sp.integrate(integral_con_jacobiano, 
                                (z, z_min, z_max), 
                                (theta, theta_min, theta_max), 
                                (r, r_min, r_max))
        
        return integral
    
    @staticmethod
    def integral_spherical(f, rho_limits, theta_limits, phi_limits):
        """
        Calcular integral triple en coordenadas esféricas
        
        :param f: Función a integrar (expresión sympy)
        :param rho_limits: Límites de rho [rho_min, rho_max]
        :param theta_limits: Límites de theta [theta_min, theta_max]
        :param phi_limits: Límites de phi [phi_min, phi_max]
        :return: Valor de la integral
        """
        rho, theta, phi = sp.symbols('rho theta phi')
        
        # Convertir límites a funciones si son constantes
        rho_min, rho_max = rho_limits
        theta_min, theta_max = theta_limits
        phi_min, phi_max = phi_limits
        
        # Factor de Jacobiano para coordenadas esféricas: rho^2 * sin(phi)
        jacobiano = rho**2 * sp.sin(phi)
        integral_con_jacobiano = f * jacobiano
        
        integral = sp.integrate(integral_con_jacobiano, 
                                (phi, phi_min, phi_max), 
                                (theta, theta_min, theta_max), 
                                (rho, rho_min, rho_max))
        
        return integral
