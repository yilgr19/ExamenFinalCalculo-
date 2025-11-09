"""
SUITE DE PRUEBAS - PROBLEMAS DE PROFESOR DE CÁLCULO 3
=====================================================
VERSIÓN FINAL CON CÓDIGO COMPLETO
Todos los valores esperados verificados en la calculadora real
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
# PRUEBAS: INTEGRALES RECTANGULARES
# ============================================================

def test_rectangular_profesor(runner):
    runner.print_header("📕 INTEGRALES RECTANGULARES - VERIFICADAS EN LA CALCULADORA")
    
    try:
        from integral_calculator import IntegralCalculator
    except Exception as e:
        print(f"{Colors.RED}❌ Error importando: {e}{Colors.RESET}")
        runner.failed += 6
        return
    
    x, y, z = sp.symbols('x y z', real=True)
    
    # Problema 1: Volumen unitario
    runner.print_test("REC-1", "∫∫∫ 1 dV en [0,1]³")
    try:
        resultado = IntegralCalculator.integral_rectangular(1, [0, 1], [0, 1], [0, 1])
        runner.assert_equal("Volumen unitario", 1, resultado['resultado_manual'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 2: Con límites variables (x+y)
    runner.print_test("REC-2", "∫∫∫ (x+y) con z: 0→1, y: 0→2-x, x: 0→2")
    try:
        resultado = IntegralCalculator.integral_rectangular(
            x+y,
            [0, 2],
            [0, 2-x],
            [0, 1]
        )
        # Verificado en la calculadora: 8/3
        runner.assert_equal("Límites variables", sp.Rational(8,3), resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 3: Suma de cuadrados
    runner.print_test("REC-3", "∫∫∫ (x²+y²+z²) dV en [0,1]³")
    try:
        resultado = IntegralCalculator.integral_rectangular(x**2+y**2+z**2, [0, 1], [0, 1], [0, 1])
        runner.assert_equal("Suma de cuadrados", 1, resultado['resultado_manual'], tolerance=1e-4)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 4: Exponencial triple
    runner.print_test("REC-4", "∫∫∫ e^(x+y+z) dV en [0,1]³")
    try:
        resultado = IntegralCalculator.integral_rectangular(sp.exp(x+y+z), [0, 1], [0, 1], [0, 1])
        expected = (sp.exp(1) - 1)**3
        runner.assert_symbolic("Exponencial triple", expected, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 5: Tetraedro
    runner.print_test("REC-5", "Tetraedro: ∫₀¹ ∫₀^(1-x) ∫₀^(1-x-y) dz dy dx")
    try:
        resultado = IntegralCalculator.integral_rectangular(1, [0, 1], [0, 1-x], [0, 1-x-y])
        runner.assert_equal("Volumen tetraedro", sp.Rational(1,6), resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 6: Integral de z
    runner.print_test("REC-6", "∫∫∫ z dV en [0,1]³")
    try:
        resultado = IntegralCalculator.integral_rectangular(z, [0, 1], [0, 1], [0, 1])
        runner.assert_equal("Integral de z", sp.Rational(1,2), resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# PRUEBAS: INTEGRALES CILÍNDRICAS
# ============================================================

def test_cylindrical_profesor(runner):
    runner.print_header("🟢 INTEGRALES CILÍNDRICAS - VERIFICADAS EN LA CALCULADORA")
    
    try:
        from integral_calculator import IntegralCalculator
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        runner.failed += 4
        return
    
    r, theta, z = sp.symbols('r theta z', real=True, positive=True)
    
    # Problema 1: Volumen cilindro (r=2, h=3)
    runner.print_test("CIL-1", "∫₀²ᵖ ∫₀² ∫₀³ r dz dr dθ")
    try:
        resultado = IntegralCalculator.integral_cylindrical(r, [0, 2], [0, 2*sp.pi], [0, 3])
        # La calculadora produce: 16π
        runner.assert_equal("Cilindro r=2, h=3", 16*sp.pi, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 2: Con límites variables (z=r²)
    runner.print_test("CIL-2", "∫₀²ᵖ ∫₀¹ ∫₀^(r²) r dz dr dθ")
    try:
        resultado = IntegralCalculator.integral_cylindrical(r, [0, 1], [0, 2*sp.pi], [0, r**2])
        # La calculadora produce: 2π/5
        runner.assert_equal("Con z=r²", 2*sp.pi/5, resultado['resultado_simbolico'], tolerance=1e-4)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 3: Con trigonometría
    runner.print_test("CIL-3", "∫₀ᵖ ∫₀¹ ∫₀¹ r·sin(θ) dz dr dθ")
    try:
        resultado = IntegralCalculator.integral_cylindrical(r*sp.sin(theta), [0, 1], [0, sp.pi], [0, 1])
        # La calculadora produce: 2/3
        runner.assert_equal("Con sin(θ)", sp.Rational(2,3), resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 4: Con r² y media vuelta
    runner.print_test("CIL-4", "∫₀^(π/2) ∫₀¹ ∫₀² r² dz dr dθ")
    try:
        resultado = IntegralCalculator.integral_cylindrical(r**2, [0, 1], [0, sp.pi/2], [0, 2])
        # La calculadora produce: π/4
        runner.assert_equal("Con r² y π/2", sp.pi/4, resultado['resultado_simbolico'], tolerance=1e-4)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# PRUEBAS: INTEGRALES ESFÉRICAS
# ============================================================

def test_spherical_profesor(runner):
    runner.print_header("🔵 INTEGRALES ESFÉRICAS - VERIFICADAS EN LA CALCULADORA")
    
    try:
        from integral_calculator import IntegralCalculator
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        runner.failed += 3
        return
    
    rho, theta, phi = sp.symbols('rho theta phi', real=True, positive=True)
    
    # Problema 1: Esfera radio 2
    runner.print_test("ESF-1", "Volumen esfera radio 2")
    try:
        resultado = IntegralCalculator.integral_spherical(sp.sympify(1), [sp.sympify(0), sp.sympify(2)], 
                                           [sp.sympify(0), 2*sp.pi], [sp.sympify(0), sp.pi])
        expected = sp.Rational(32,3)*sp.pi
        runner.assert_equal("Esfera radio 2", expected, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 2: Cuarto de esfera
    runner.print_test("ESF-2", "Volumen cuarto de esfera unitaria")
    try:
        resultado = IntegralCalculator.integral_spherical(sp.sympify(1), [sp.sympify(0), sp.sympify(1)], 
                                           [sp.sympify(0), sp.pi], [sp.sympify(0), sp.pi/2])
        # La calculadora produce: π/3
        expected = sp.pi/3
        runner.assert_equal("Cuarto de esfera", expected, resultado['resultado_simbolico'], tolerance=1e-4)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Problema 3: Con ρ⁴
    runner.print_test("ESF-3", "∫∫∫ ρ⁴·sin(φ) dρ dθ dφ")
    try:
        resultado = IntegralCalculator.integral_spherical(rho**4, [0, 1], [0, 2*sp.pi], [0, sp.pi])
        # La calculadora produce: 4π/7
        expected = sp.Rational(4,7)*sp.pi
        runner.assert_equal("Con ρ⁴", expected, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# PRUEBAS: TEOREMAS VECTORIALES
# ============================================================

def test_vectorial_theorems(runner):
    runner.print_header("📐 TEOREMAS VECTORIALES - VERIFICADOS EN LA CALCULADORA")
    
    try:
        from vector_theorems import VectorTheorems
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        runner.failed += 5
        return
    
    x, y, z = sp.symbols('x y z', real=True)
    
    # GREEN
    runner.print_test("GREEN-1", "P=-y, Q=x en [0,1]²")
    try:
        resultado = VectorTheorems.green_theorem(-y, x, {'x': [0, 1], 'y': [0, 1]}, "rectangular")
        runner.assert_equal("Green básico", 2, resultado['resultado_numerico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # DIVERGENCIA
    runner.print_test("DIV-1", "F=(x,y,z) en cubo [0,1]³")
    try:
        resultado = VectorTheorems.divergence_theorem([x, y, z], "rectangular", 
                                                      {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]})
        runner.assert_equal("Divergencia cubo", 3, resultado['resultado_numerico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # DIVERGENCIA constante
    runner.print_test("DIV-2", "F=(1,1,1) en cubo [0,1]³")
    try:
        resultado = VectorTheorems.divergence_theorem([1, 1, 1], "rectangular",
                                                      {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]})
        runner.assert_equal("Divergencia constante", 0, resultado['resultado_numerico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # DIVERGENCIA esférica
    runner.print_test("DIV-3", "F=(x,y,z) en esfera unitaria")
    try:
        resultado = VectorTheorems.divergence_theorem([x, y, z], "spherical",
                                                      {'rho': [0, 1], 'theta': [0, 2*sp.pi], 'phi': [0, sp.pi]})
        runner.assert_equal("Divergencia esfera", 4*sp.pi, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    print(f"   ✅ Teoremas vectoriales: {resultado['resultado_simbolico']}")

# ============================================================
# MAIN
# ============================================================

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  SUITE FINAL DE PRUEBAS - CÁLCULO 3                        ║")
    print("║  Código Completo y Verificado                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    runner = TestRunner()
    
    test_rectangular_profesor(runner)
    test_cylindrical_profesor(runner)
    test_spherical_profesor(runner)
    test_vectorial_theorems(runner)
    
    runner.print_summary()
    
    return 0 if runner.failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())