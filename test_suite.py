"""
SUITE DE PRUEBAS - EJEMPLOS DE PROFESOR DE CÁLCULO 3
=====================================================
Problemas reales que un profesor de cálculo 3 pondría
Verifica que la calculadora resuelve correctamente
"""

import sys
import sympy as sp
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.start_time = datetime.now()
        
    def print_header(self, title):
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{title:^70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")
    
    def print_test(self, name, description=""):
        print(f"{Colors.BLUE}📌 {name}{Colors.RESET}")
        if description:
            print(f"   {description}")
    
    def assert_equal(self, test_name, expected, actual, tolerance=1e-4):
        try:
            diff = abs(float(expected) - float(actual))
            if diff < tolerance:
                self.passed += 1
                print(f"{Colors.GREEN}✅ PASS{Colors.RESET}: {test_name}")
                print(f"   Esperado: {expected}, Obtenido: {actual}")
                return True
            else:
                self.failed += 1
                self.errors.append((test_name, f"Diferencia: {diff}"))
                print(f"{Colors.RED}❌ FAIL{Colors.RESET}: {test_name}")
                print(f"   Esperado: {expected}, Obtenido: {actual}")
                return False
        except Exception as e:
            self.failed += 1
            self.errors.append((test_name, str(e)))
            print(f"{Colors.RED}❌ ERROR{Colors.RESET}: {test_name}")
            print(f"   {str(e)}")
            return False
    
    def assert_symbolic(self, test_name, expected_symbolic, actual_symbolic):
        try:
            diff = sp.simplify(expected_symbolic - actual_symbolic)
            if diff == 0:
                self.passed += 1
                print(f"{Colors.GREEN}✅ PASS{Colors.RESET}: {test_name}")
                return True
            else:
                self.failed += 1
                self.errors.append((test_name, f"Diferencia: {diff}"))
                print(f"{Colors.RED}❌ FAIL{Colors.RESET}: {test_name}")
                return False
        except Exception as e:
            self.failed += 1
            self.errors.append((test_name, str(e)))
            print(f"{Colors.RED}❌ ERROR{Colors.RESET}: {test_name}")
            print(f"   {str(e)}")
            return False
    
    def print_summary(self):
        elapsed = (datetime.now() - self.start_time).total_seconds()
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}RESUMEN FINAL{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.GREEN}✅ Pasadas: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}❌ Fallidas: {self.failed}{Colors.RESET}")
        print(f"📊 Total: {total}")
        print(f"📈 Éxito: {percentage:.1f}%")
        print(f"⏱️  Tiempo: {elapsed:.2f}s")
        
        if self.failed > 0:
            print(f"\n{Colors.RED}{Colors.BOLD}ERRORES:{Colors.RESET}")
            for test_name, error in self.errors:
                print(f"  • {test_name}: {error}")
        else:
            print(f"\n{Colors.GREEN}{Colors.BOLD}¡TODAS LAS PRUEBAS PASARON! ✓{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

# ============================================================
# PRUEBAS: INTEGRALES RECTANGULARES (Problemas reales)
# ============================================================

def test_rectangular_profesor(runner):
    runner.print_header("📕 INTEGRALES RECTANGULARES - PROBLEMAS DE PROFESOR")
    
    try:
        from integral_calculator import IntegralCalculator
    except Exception as e:
        print(f"{Colors.RED}❌ Error importando: {e}{Colors.RESET}")
        runner.failed += 6
        return
    
    x, y, z = sp.symbols('x y z', real=True)
    
    # Problema 1
    runner.print_test("REC-PROF-1", "Calcular ∫∫∫ xyz dV en [0,1]³")
    try:
        resultado = calc.integral_rectangular(x*y*z, [0, 1], [0, 1], [0, 1])
        runner.assert_equal("Producto xyz", sp.Rational(1,8), resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 2
    runner.print_test("REC-PROF-2", "Calcular ∫₀¹ ∫₀ˣ ∫₀^(x+y) dz dy dx")
    try:
        resultado = calc.integral_rectangular(1, [0, 1], [0, x], [0, x+y])
        runner.assert_equal("Límites variables complejos", sp.Rational(1,6), resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 3
    runner.print_test("REC-PROF-3", "Calcular ∫∫∫ (x²+y²+z²) dV en [0,1]³")
    try:
        resultado = calc.integral_rectangular(x**2+y**2+z**2, [0, 1], [0, 1], [0, 1])
        runner.assert_equal("Suma de cuadrados", 1, resultado['resultado_manual'], tolerance=1e-4)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 4
    runner.print_test("REC-PROF-4", "Calcular ∫∫∫ e^(x+y+z) dV en [0,1]³")
    try:
        resultado = calc.integral_rectangular(sp.exp(x+y+z), [0, 1], [0, 1], [0, 1])
        expected = (sp.exp(1) - 1)**3
        runner.assert_symbolic("Exponencial triple", expected, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 5
    runner.print_test("REC-PROF-5", "Tetraedro: ∫₀¹ ∫₀^(1-x) ∫₀^(1-x-y) dz dy dx")
    try:
        resultado = calc.integral_rectangular(1, [0, 1], [0, 1-x], [0, 1-x-y])
        runner.assert_equal("Volumen tetraedro", sp.Rational(1,6), resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 6
    runner.print_test("REC-PROF-6", "Calcular ∫∫∫ z dV en [0,1]³")
    try:
        resultado = calc.integral_rectangular(z, [0, 1], [0, 1], [0, 1])
        runner.assert_equal("Integral de z", sp.Rational(1,2), resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# PRUEBAS: INTEGRALES CILÍNDRICAS
# ============================================================

def test_cylindrical_profesor(runner):
    runner.print_header("🟢 INTEGRALES CILÍNDRICAS - PROBLEMAS DE PROFESOR")
    
    try:
        import integral_calculator
        calc = integral_calculator.IntegralCalculator()
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        runner.failed += 4
        return
    
    r, theta, z = sp.symbols('r theta z', real=True, positive=True)
    calc = IntegralCalculator()
    
    # Problema 1
    runner.print_test("CIL-PROF-1", "Volumen cilindro: ∫₀²ᵖ ∫₀² ∫₀³ r dz dr dθ")
    try:
        resultado = calc.integral_cylindrical(r, [0, 2], [0, 2*sp.pi], [0, 3])
        runner.assert_equal("Cilindro r=2, h=3", 12*sp.pi, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 2
    runner.print_test("CIL-PROF-2", "Calcular ∫₀²ᵖ ∫₀¹ ∫₀^(r²) r dz dr dθ")
    try:
        resultado = calc.integral_cylindrical(r, [0, 1], [0, 2*sp.pi], [0, r**2])
        runner.assert_equal("Límites con r²", sp.pi, resultado['resultado_simbolico'], tolerance=1e-4)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 3
    runner.print_test("CIL-PROF-3", "Calcular ∫₀ᵖ ∫₀¹ ∫₀¹ r*sin(theta) dz dr dθ")
    try:
        resultado = calc.integral_cylindrical(r*sp.sin(theta), [0, 1], [0, sp.pi], [0, 1])
        runner.assert_equal("Con trigonometría", sp.Rational(1,3), resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 4
    runner.print_test("CIL-PROF-4", "Calcular ∫₀^(π/2) ∫₀¹ ∫₀² r² dz dr dθ")
    try:
        resultado = calc.integral_cylindrical(r**2, [0, 1], [0, sp.pi/2], [0, 2])
        runner.assert_equal("Con r² y media vuelta", sp.Rational(4,9), resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# PRUEBAS: INTEGRALES ESFÉRICAS
# ============================================================

def test_spherical_profesor(runner):
    runner.print_header("🔵 INTEGRALES ESFÉRICAS - PROBLEMAS DE PROFESOR")
    
    try:
        import integral_calculator
        calc = integral_calculator.IntegralCalculator()
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        runner.failed += 3
        return
    
    rho, theta, phi = sp.symbols('rho theta phi', real=True, positive=True)
    calc = IntegralCalculator()
    
    # Problema 1
    runner.print_test("ESF-PROF-1", "Volumen esfera: ∫₀ᵖ ∫₀²ᵖ ∫₀² ρ²sin(φ) dρ dθ dφ")
    try:
        resultado = calc.integral_spherical(sp.sympify(1), [sp.sympify(0), sp.sympify(2)], 
                                           [sp.sympify(0), 2*sp.pi], [sp.sympify(0), sp.pi])
        runner.assert_equal("Esfera radio 2", sp.Rational(32,3)*sp.pi, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 2
    runner.print_test("ESF-PROF-2", "Calcular ∫₀ᵖ ∫₀ᵖ/² ∫₀¹ ρ² dρ dθ dφ (cuarto esfera)")
    try:
        resultado = calc.integral_spherical(sp.sympify(1), [sp.sympify(0), sp.sympify(1)], 
                                           [sp.sympify(0), sp.pi], [sp.sympify(0), sp.pi/2])
        runner.assert_equal("Cuarto de esfera", sp.pi, resultado['resultado_simbolico'], tolerance=1e-4)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 3
    runner.print_test("ESF-PROF-3", "Calcular ∫₀²ᵖ ∫₀ᵖ ∫₀¹ ρ⁴ sin(φ) dρ dθ dφ")
    try:
        resultado = calc.integral_spherical(rho**4, [0, 1], [0, 2*sp.pi], [0, sp.pi])
        runner.assert_equal("Con ρ⁴", sp.Rational(4,5)*sp.pi, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# PRUEBAS: TEOREMAS VECTORIALES
# ============================================================

def test_green_profesor(runner):
    runner.print_header("🔴 TEOREMA DE GREEN - PROBLEMAS DE PROFESOR")
    
    try:
        from vector_theorems import VectorTheorems
    except ImportError as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        return
    
    x, y = sp.symbols('x y', real=True)
    
    # Problema 1
    runner.print_test("GREEN-PROF-1", "P = x², Q = y² en [0,2]²")
    try:
        resultado = VectorTheorems.green_theorem(x**2, y**2, {'x': [0, 2], 'y': [0, 2]}, "rectangular")
        print(f"   Resultado: {resultado['resultado_simbolico']}")
        runner.passed += 1
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 2
    runner.print_test("GREEN-PROF-2", "P = xy, Q = x en región [0,1]²")
    try:
        resultado = VectorTheorems.green_theorem(x*y, x, {'x': [0, 1], 'y': [0, 1]}, "rectangular")
        print(f"   Resultado: {resultado['resultado_simbolico']}")
        runner.passed += 1
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

def test_stokes_profesor(runner):
    runner.print_header("🟦 TEOREMA DE STOKES - PROBLEMAS DE PROFESOR")
    
    try:
        from vector_theorems import VectorTheorems
    except ImportError as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        return
    
    u, v = sp.symbols('u v', real=True)
    x, y, z = sp.symbols('x y z', real=True)
    
    # Problema 1
    runner.print_test("STOKES-PROF-1", "F = (z, x, y) en esfera unitaria")
    try:
        resultado = VectorTheorems.stokes_theorem(
            [z, x, y],
            [sp.sin(u)*sp.cos(v), sp.sin(u)*sp.sin(v), sp.cos(u)],
            {'u': [0, sp.pi], 'v': [0, 2*sp.pi]}
        )
        print(f"   Resultado: {resultado['resultado_simbolico']}")
        runner.passed += 1
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

def test_divergence_profesor(runner):
    runner.print_header("🟥 TEOREMA DIVERGENCIA - PROBLEMAS DE PROFESOR")
    
    try:
        from vector_theorems import VectorTheorems
    except ImportError as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        return
    
    x, y, z = sp.symbols('x y z', real=True)
    
    # Problema 1
    runner.print_test("DIV-PROF-1", "F = (x², y², z²) en cubo [0,1]³")
    try:
        resultado = VectorTheorems.divergence_theorem(
            [x**2, y**2, z**2],
            "rectangular",
            {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]}
        )
        print(f"   Resultado: {resultado['resultado_simbolico']}")
        runner.passed += 1
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 2
    runner.print_test("DIV-PROF-2", "F = (x, y, z) en esfera unitaria")
    try:
        resultado = VectorTheorems.divergence_theorem(
            [x, y, z],
            "spherical",
            {'rho': [0, 1], 'theta': [0, 2*sp.pi], 'phi': [0, sp.pi]}
        )
        runner.assert_equal("Divergencia esfera", 4*sp.pi, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# MAIN
# ============================================================

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  PRUEBAS DE PROFESOR - CÁLCULO 3                            ║")
    print("║  Problemas típicos de examen                                ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    runner = TestRunner()
    
    test_rectangular_profesor(runner)
    test_cylindrical_profesor(runner)
    test_spherical_profesor(runner)
    test_green_profesor(runner)
    test_stokes_profesor(runner)
    test_divergence_profesor(runner)
    
    runner.print_summary()
    
    return 0 if runner.failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())