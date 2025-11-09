"""
TEST FINAL VERIFICADO - SUITE COMPLETA DE PRUEBAS v10.0
Archivo: test_final_v10.py
Ejecutar: python test_final_v10.py

Suite extendida con ejemplos AVANZADOS de teoremas vectoriales
Enfoque en detectar qué funcionalidades faltan en el programa
"""

import sys
import sympy as sp
from datetime import datetime
import math

# Limpiar caché
for mod in list(sys.modules.keys()):
    if 'integral' in mod or 'vector' in mod or 'test' in mod:
        del sys.modules[mod]

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    ORANGE = '\033[38;5;208m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.start_time = datetime.now()
    
    def print_header(self, title):
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{title:^80}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")
    
    def print_test(self, test_name, desc):
        print(f"\n{Colors.BOLD}{test_name}: {desc}{Colors.RESET}")
        print("-" * 80)
    
    def pass_test(self, msg=""):
        self.passed += 1
        print(f"   {Colors.GREEN}✅ PASS{Colors.RESET} {msg}")
    
    def fail_test(self, msg=""):
        self.failed += 1
        print(f"   {Colors.RED}❌ FAIL{Colors.RESET} {msg}")
    
    def error_test(self, msg=""):
        self.failed += 1
        print(f"   {Colors.RED}❌ ERROR{Colors.RESET}: {msg}")
    
    def skip_test(self, msg=""):
        self.skipped += 1
        print(f"   {Colors.YELLOW}⏭️  SKIP{Colors.RESET} {msg}")
    
    def print_summary(self):
        elapsed = (datetime.now() - self.start_time).total_seconds()
        total = self.passed + self.failed + self.skipped
        percentage = (self.passed / (self.passed + self.failed) * 100) if (self.passed + self.failed) > 0 else 0
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}📊 RESUMEN FINAL{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
        print(f"{Colors.GREEN}✅ Pasadas: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}❌ Fallidas: {self.failed}{Colors.RESET}")
        print(f"{Colors.YELLOW}⏭️  Saltadas: {self.skipped}{Colors.RESET}")
        print(f"📊 Total: {total}")
        print(f"📈 Éxito: {percentage:.1f}%")
        print(f"⏱️  Tiempo: {elapsed:.2f}s\n")

def close_enough(val1, val2, tolerance=1e-3):
    """Verifica si dos valores están lo suficientemente cerca"""
    if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
        return abs(val1 - val2) < tolerance
    return False

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔" + "="*78 + "╗")
    print("║" + " "*10 + "🧮 TEST SUITE FINAL - VERSIÓN 10.0 AVANZADA 🧮" + " "*15 + "║")
    print("║" + " "*8 + "INTEGRALES TRIPLES Y TEOREMAS VECTORIALES - CASOS COMPLEJOS" + " "*8 + "║")
    print("╚" + "="*78 + "╝")
    print(f"{Colors.RESET}\n")
    
    runner = TestRunner()
    
    # ===== CARGAR MÓDULOS =====
    print(f"{Colors.BOLD}📦 Cargando módulos...{Colors.RESET}\n")
    
    try:
        from integral_calculator import IntegralCalculator
        print(f"{Colors.GREEN}✅ IntegralCalculator importado{Colors.RESET}")
        ic_available = True
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        ic_available = False
    
    try:
        from vector_theorems import VectorTheorems
        print(f"{Colors.GREEN}✅ VectorTheorems importado{Colors.RESET}\n")
        vt_available = True
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}\n")
        vt_available = False
    
    if not ic_available and not vt_available:
        print(f"{Colors.RED}❌ No se pueden cargar los módulos{Colors.RESET}")
        return 1
    
    x, y, z = sp.symbols('x y z', real=True)
    u, v = sp.symbols('u v', real=True)
    rho, theta, phi = sp.symbols('rho theta phi', real=True, positive=True)
    
    # ===== INTEGRALES BÁSICAS =====
    if ic_available:
        runner.print_header("📕 INTEGRALES RECTANGULARES - VERIFICACIÓN BÁSICA")
        
        runner.print_test("REC-1", "Volumen unitario")
        try:
            result = IntegralCalculator.integral_rectangular(1, [0, 1], [0, 1], [0, 1])
            val = float(result['resultado_manual'])
            if abs(val - 1.0) < 1e-4:
                runner.pass_test(f"✓ Resultado: {val}")
            else:
                runner.fail_test(f"Esperado 1.0, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
    
    # ===== TEOREMA DE LA DIVERGENCIA - CASOS BÁSICOS =====
    if vt_available:
        runner.print_header("📐 TEOREMA DE LA DIVERGENCIA - NIVEL 1: BÁSICO")
        
        # DIV-B1: Campo radial simple
        runner.print_test("DIV-B1", "Campo radial F=(x,y,z) en cubo [0,1]³")
        try:
            result = VectorTheorems.divergence_theorem([x, y, z], "rectangular", 
                                                     {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]})
            val = float(result['resultado_numerico'])
            if close_enough(val, 3.0):
                runner.pass_test(f"✓ Resultado: {val} (div=3, vol=1)")
            else:
                runner.fail_test(f"Esperado 3.0, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # DIV-B2: Campo constante
        runner.print_test("DIV-B2", "Campo constante F=(1,1,1) en cubo [0,1]³")
        try:
            result = VectorTheorems.divergence_theorem([1, 1, 1], "rectangular",
                                                     {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]})
            val = float(result['resultado_numerico'])
            if close_enough(val, 0.0):
                runner.pass_test(f"✓ Resultado: {val} (divergencia nula)")
            else:
                runner.fail_test(f"Esperado 0.0, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # DIV-B3: Campo radial en esfera
        runner.print_test("DIV-B3", "Campo radial F=(x,y,z) en esfera unidad")
        try:
            result = VectorTheorems.divergence_theorem([x, y, z], "spherical",
                                                     {'rho': [0, 1], 'theta': [0, 2*sp.pi], 'phi': [0, sp.pi]})
            val = float(result['resultado_numerico'])
            expected = 4*math.pi
            if close_enough(val, expected, tolerance=0.1):
                runner.pass_test(f"✓ Resultado: {val} ≈ 4π")
            else:
                runner.fail_test(f"Esperado ≈12.566, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        runner.print_header("📐 TEOREMA DE LA DIVERGENCIA - NIVEL 2: TÉRMINOS CRUZADOS")
        
        # DIV-A1: Campo con términos cruzados
        runner.print_test("DIV-A1", "Campo cruzado F=(xy,yz,zx) en cubo [0,1]³")
        try:
            result = VectorTheorems.divergence_theorem([x*y, y*z, z*x], "rectangular",
                                                     {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]})
            val = float(result['resultado_numerico'])
            if close_enough(val, 1.5):  # ∫(x+y+z)dV = 3/2
                runner.pass_test(f"✓ Resultado: {val} (esperado 1.5)")
            else:
                runner.fail_test(f"Esperado 1.5, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # DIV-A2: Campo polinómico 3D
        runner.print_test("DIV-A2", "Campo polinómico F=(x²z,xy²,yz²) en cubo [0,1]³")
        try:
            result = VectorTheorems.divergence_theorem([x**2*z, x*y**2, y*z**2], "rectangular",
                                                     {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]})
            val = float(result['resultado_numerico'])
            if close_enough(val, 1.5):  # ∫(2xz+2xy+2yz)dV = 3/2
                runner.pass_test(f"✓ Resultado: {val} (esperado 1.5)")
            else:
                runner.fail_test(f"Esperado 1.5, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # DIV-A3: Campo cuadrático simétrico
        runner.print_test("DIV-A3", "Campo cuadrático F=(x²,y²,z²) en cubo [-1,1]³")
        try:
            result = VectorTheorems.divergence_theorem([x**2, y**2, z**2], "rectangular",
                                                     {'x': [-1, 1], 'y': [-1, 1], 'z': [-1, 1]})
            val = float(result['resultado_numerico'])
            if close_enough(val, 0.0, tolerance=1e-2):
                runner.pass_test(f"✓ Resultado: {val} (simetría → 0)")
            else:
                runner.fail_test(f"Esperado 0.0, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # DIV-A4: Campo asimétrico
        runner.print_test("DIV-A4", "Campo asimétrico F=(x+y,y+z,z+x) en cubo [0,1]³")
        try:
            result = VectorTheorems.divergence_theorem([x+y, y+z, z+x], "rectangular",
                                                     {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]})
            val = float(result['resultado_numerico'])
            if close_enough(val, 3.0):
                runner.pass_test(f"✓ Resultado: {val} (div=3, vol=1)")
            else:
                runner.fail_test(f"Esperado 3.0, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        runner.print_header("📐 TEOREMA DE LA DIVERGENCIA - NIVEL 3: CASOS ESPECIALES")
        
        # DIV-E1: Campo exponencial
        runner.print_test("DIV-E1", "Campo exponencial F=(eˣ,eʸ,eᶻ) en cubo [0,1]³")
        try:
            result = VectorTheorems.divergence_theorem([sp.exp(x), sp.exp(y), sp.exp(z)], "rectangular",
                                                     {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]})
            val = float(result['resultado_numerico'])
            expected = 3*(math.e - 1)  # 3(e-1) ≈ 5.154
            if close_enough(val, expected, tolerance=0.1):
                runner.pass_test(f"✓ Resultado: {val} ≈ 3(e-1)")
            else:
                runner.fail_test(f"Esperado ≈5.154, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # DIV-E2: Campo monopolo - CORREGIDO
        runner.print_test("DIV-E2", "Campo radial decaimiento F=(x/r³,y/r³,z/r³) en anillo esférico [1,2]")
        try:
            # ✅ CORRECCIÓN: Usar la función especializada para monopolos
            result = VectorTheorems.divergence_monopole_field(1, 2)
            val = float(result['resultado_numerico'])
            
            # El campo monopolo tiene divergencia 0 en r ≠ 0
            if close_enough(val, 0.0):
                runner.pass_test(f"✓ Resultado: {val} (div F = 0 para r > 0)")
            else:
                runner.fail_test(f"Esperado 0.0, obtenido {val}")
        except AttributeError:
            # Si la función no existe, intentar con divergence_theorem normal
            try:
                r_sym = sp.sqrt(x**2 + y**2 + z**2)
                result = VectorTheorems.divergence_theorem(
                    [x/r_sym**3, y/r_sym**3, z/r_sym**3], 
                    "spherical",
                    {'rho': [1, 2], 'theta': [0, 2*sp.pi], 'phi': [0, sp.pi]}
                )
                val = float(result['resultado_numerico'])
                if close_enough(val, 0.0):
                    runner.pass_test(f"✓ Resultado: {val} (div F = 0)")
                else:
                    runner.fail_test(f"Esperado 0.0, obtenido {val}")
            except Exception as e2:
                runner.error_test(f"Función divergence_monopole_field no encontrada. {str(e2)[:40]}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # DIV-E3: Campo escalado
        runner.print_test("DIV-E3", "Campo escalado F=(2x,2y,2z) en esfera unidad")
        try:
            result = VectorTheorems.divergence_theorem([2*x, 2*y, 2*z], "spherical",
                                                     {'rho': [0, 1], 'theta': [0, 2*sp.pi], 'phi': [0, sp.pi]})
            val = float(result['resultado_numerico'])
            expected = 8*math.pi
            if close_enough(val, expected, tolerance=0.1):
                runner.pass_test(f"✓ Resultado: {val} ≈ 8π")
            else:
                runner.fail_test(f"Esperado ≈25.133, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        runner.print_header("🔄 TEOREMA DE STOKES - NIVEL 1: BASICO")
        
        # STOKES-1: Disco plano
        runner.print_test("STOKES-1", "Campo F=(-y,x,0) en disco r≤1, z=0")
        try:
            F = [-y, x, 0]
            params = [u*sp.cos(v), u*sp.sin(v), 0]
            bounds = {'u': [0, 1], 'v': [0, 2*sp.pi]}
            result = VectorTheorems.stokes_theorem(F, params, bounds)
            val = float(result['resultado_numerico'])
            expected = 2*math.pi
            if close_enough(val, expected, tolerance=0.1):
                runner.pass_test(f"✓ Resultado: {val} ≈ 2π")
            else:
                runner.fail_test(f"Esperado ≈6.283, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        runner.print_header("🔄 TEOREMA DE STOKES - NIVEL 2: ROTACIONAL VARIABLE")
        
        # STOKES-2: Campo con rotacional constante (variante)
        runner.print_test("STOKES-2", "Campo F=(-y+z,x,0) en disco z=0, r≤1")
        try:
            F = [-y+z, x, 0]
            params = [u*sp.cos(v), u*sp.sin(v), 0]
            bounds = {'u': [0, 1], 'v': [0, 2*sp.pi]}
            result = VectorTheorems.stokes_theorem(F, params, bounds)
            val = float(result['resultado_numerico'])
            expected = 2*math.pi  # rot F = (0,0,2)
            if close_enough(val, expected, tolerance=0.1):
                runner.pass_test(f"✓ Resultado: {val} ≈ 2π")
            else:
                runner.fail_test(f"Esperado ≈6.283, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # STOKES-3: Paraboloide
        runner.print_test("STOKES-3", "Campo F=(-y,x,z) en paraboloide z=1-u²")
        try:
            F = [-y, x, z]
            params = [u*sp.cos(v), u*sp.sin(v), 1-u**2]
            bounds = {'u': [0, 1], 'v': [0, 2*sp.pi]}
            result = VectorTheorems.stokes_theorem(F, params, bounds)
            val = float(result['resultado_numerico'])
            expected = 2*math.pi
            if close_enough(val, expected, tolerance=0.1):
                runner.pass_test(f"✓ Resultado: {val} ≈ 2π")
            else:
                runner.fail_test(f"Esperado ≈6.283, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # STOKES-4: Campo cuadrático
        runner.print_test("STOKES-4", "Campo F=(-y²,x²,0) en disco z=0")
        try:
            F = [-y**2, x**2, 0]
            params = [u*sp.cos(v), u*sp.sin(v), 0]
            bounds = {'u': [0, 1], 'v': [0, 2*sp.pi]}
            result = VectorTheorems.stokes_theorem(F, params, bounds)
            val = float(result['resultado_numerico'])
            # rot F = (0,0,2x+2y), integra a 0 por simetría
            if close_enough(val, 0.0, tolerance=0.1):
                runner.pass_test(f"✓ Resultado: {val} (simetría → 0)")
            else:
                runner.fail_test(f"Esperado 0.0, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        runner.print_header("🟣 TEOREMA DE GREEN - NIVEL 1: BASICO")
        
        # GREEN-1: Campo clásico
        runner.print_test("GREEN-1", "Campo F=(-y,x) en círculo unidad")
        try:
            result = VectorTheorems.green_theorem(-y, x, {'r': [0, 1], 'theta': [0, 2*sp.pi]}, "polar")
            val = float(result['resultado_numerico'])
            expected = 2*math.pi
            if close_enough(val, expected, tolerance=0.1):
                runner.pass_test(f"✓ Resultado: {val} ≈ 2π")
            else:
                runner.fail_test(f"Esperado ≈6.283, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        runner.print_header("🟣 TEOREMA DE GREEN - NIVEL 2: CASOS ESPECIALES")
        
        # GREEN-2: Sin rotacional
        runner.print_test("GREEN-2", "Campo F=(x²,y²) en cuadrado [-1,1]²")
        try:
            result = VectorTheorems.green_theorem(x**2, y**2, {'x': [-1, 1], 'y': [-1, 1]}, "rectangular")
            val = float(result['resultado_numerico'])
            if close_enough(val, 0.0, tolerance=1e-2):
                runner.pass_test(f"✓ Resultado: {val} (rotacional nulo)")
            else:
                runner.fail_test(f"Esperado 0.0, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # GREEN-3: Trigonométrico
        runner.print_test("GREEN-3", "Campo F=(-y·cos(x),sin(x)) en cuadrado [0,π]²")
        try:
            result = VectorTheorems.green_theorem(-y*sp.cos(x), sp.sin(x), 
                                                 {'x': [0, sp.pi], 'y': [0, sp.pi]}, "rectangular")
            val = float(result['resultado_numerico'])
            if close_enough(val, 0.0, tolerance=0.1):
                runner.pass_test(f"✓ Resultado: {val} ≈ 0")
            else:
                runner.fail_test(f"Esperado 0.0, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # GREEN-4: Exponencial
        runner.print_test("GREEN-4", "Campo F=(eˣ·sin(y),eˣ·cos(y)) en rect [0,1]×[0,π/2]")
        try:
            result = VectorTheorems.green_theorem(sp.exp(x)*sp.sin(y), sp.exp(x)*sp.cos(y),
                                                 {'x': [0, 1], 'y': [0, sp.pi/2]}, "rectangular")
            val = float(result['resultado_numerico'])
            if close_enough(val, 0.0, tolerance=0.1):
                runner.pass_test(f"✓ Resultado: {val} ≈ 0")
            else:
                runner.fail_test(f"Esperado 0.0, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # GREEN-5: Rotacional constante
        runner.print_test("GREEN-5", "Campo F=(-2y,3x) en círculo unidad")
        try:
            result = VectorTheorems.green_theorem(-2*y, 3*x, {'r': [0, 1], 'theta': [0, 2*sp.pi]}, "polar")
            val = float(result['resultado_numerico'])
            expected = 5*math.pi  # rotacional = 5, área = π
            if close_enough(val, expected, tolerance=0.1):
                runner.pass_test(f"✓ Resultado: {val} ≈ 5π")
            else:
                runner.fail_test(f"Esperado ≈15.708, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
    
    runner.print_summary()
    return 0 if runner.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())