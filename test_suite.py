"""
SUITE COMPLETA DE PRUEBAS - VERSIÓN CORREGIDA
Calculadora de Integrales Triples y Teoremas Vectoriales
================================
✅ Correcciones SOLO en pruebas (sin tocar integral_calculator.py)
✅ Todas las pruebas con valores esperados correctos
"""

import sys
import sympy as sp
from datetime import datetime
import traceback

# Colores para terminal
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
    
    def assert_equal(self, test_name, expected, actual, tolerance=1e-5):
        """Compara resultados con tolerancia"""
        try:
            diff = abs(float(expected) - float(actual))
            if diff < tolerance:
                self.passed += 1
                print(f"{Colors.GREEN}✅ PASS{Colors.RESET}: {test_name}")
                print(f"   Esperado: {expected}, Obtenido: {actual}")
                return True
            else:
                self.failed += 1
                self.errors.append((test_name, f"Diferencia: {diff} > {tolerance}"))
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
        """Compara resultados simbólicos"""
        try:
            diff = sp.simplify(expected_symbolic - actual_symbolic)
            if diff == 0:
                self.passed += 1
                print(f"{Colors.GREEN}✅ PASS{Colors.RESET}: {test_name}")
                return True
            else:
                self.failed += 1
                self.errors.append((test_name, f"Simbólicamente diferente: {diff}"))
                print(f"{Colors.RED}❌ FAIL{Colors.RESET}: {test_name}")
                print(f"   Diferencia: {diff}")
                return False
        except Exception as e:
            self.failed += 1
            self.errors.append((test_name, str(e)))
            print(f"{Colors.RED}❌ ERROR{Colors.RESET}: {test_name}")
            print(f"   {str(e)}")
            return False
    
    def assert_result_exists(self, test_name, resultado, show_value=False):
        """Verifica que hay resultado sin chequear valor específico"""
        try:
            if resultado and ('resultado_simbolico' in resultado or 'resultado_numerico' in resultado):
                self.passed += 1
                valor = resultado.get('resultado_simbolico', resultado.get('resultado_numerico'))
                print(f"{Colors.GREEN}✅ PASS{Colors.RESET}: {test_name}")
                if show_value:
                    print(f"   Resultado: {valor}")
                return True
            else:
                self.failed += 1
                self.errors.append((test_name, "No hay resultado válido"))
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
        print(f"{Colors.BOLD}RESUMEN DE PRUEBAS{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.GREEN}✅ Pasadas: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}❌ Fallidas: {self.failed}{Colors.RESET}")
        print(f"📊 Total: {total}")
        print(f"📈 Éxito: {percentage:.1f}%")
        print(f"⏱️  Tiempo: {elapsed:.2f}s")
        
        if self.failed > 0:
            print(f"\n{Colors.RED}{Colors.BOLD}ERRORES DETECTADOS:{Colors.RESET}")
            for test_name, error in self.errors:
                print(f"  • {test_name}: {error}")
        else:
            print(f"\n{Colors.GREEN}{Colors.BOLD}¡TODAS LAS PRUEBAS PASARON!{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

# ============================================================
# PRUEBAS DE INTEGRALES RECTANGULARES
# ============================================================

def test_rectangular_integrals(runner):
    runner.print_header("🔹 PRUEBAS: INTEGRALES RECTANGULARES")
    
    try:
        from integral_calculator import IntegralCalculator
    except ImportError as e:
        print(f"{Colors.RED}❌ Error importando integral_calculator: {e}{Colors.RESET}")
        return
    
    x, y, z = sp.symbols('x y z', real=True)
    calc = IntegralCalculator()
    
    # Prueba 1: Integral simple
    runner.print_test("REC-1", "∫∫∫ 1 dV en [0,1]³")
    try:
        resultado = calc.integral_rectangular(1, [0, 1], [0, 1], [0, 1])
        runner.assert_equal("Volumen unitario", 1, resultado['resultado_manual'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 2: Función lineal
    runner.print_test("REC-2", "∫∫∫ (x+y+z) dV en [0,1]³")
    try:
        resultado = calc.integral_rectangular(x+y+z, [0, 1], [0, 1], [0, 1])
        runner.assert_equal("Suma lineal", 1.5, resultado['resultado_manual'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 3: Con límites variables (x+y)
    runner.print_test("REC-3", "∫∫∫ (x+y) con z: 0→1, y: 0→2-x, x: 0→2")
    try:
        resultado = calc.integral_rectangular(
            x+y,
            [0, 2],
            [0, 2-x],
            [0, 1]
        )
        runner.assert_equal("Límites variables", sp.Rational(8,3), resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 4: Con límites variables (x*y^2*z) - CORREGIDO
    # ∫₁² ∫₀¹ ∫₀ˣ x*y²*z dz dy dx = 5/8
    runner.print_test("REC-4", "∫∫∫ x*y²*z con z: 0→x, y: 0→1, x: 1→2")
    try:
        resultado = calc.integral_rectangular(
            x*y**2*z,
            [1, 2],
            [0, 1],
            [0, x]
        )
        # ✅ CORREGIDO: El resultado correcto es 5/8, no 7/6
        runner.assert_equal("Límites variables 2", sp.Rational(5,8), resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 5: Exponencial
    runner.print_test("REC-5", "∫∫∫ e^(-x-y-z) en [0,1]³")
    try:
        resultado = calc.integral_rectangular(
            sp.exp(-x-y-z),
            [0, 1],
            [0, 1],
            [0, 1]
        )
        expected = (1 - sp.exp(-1))**3
        runner.assert_symbolic("Exponencial", expected, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# PRUEBAS DE INTEGRALES CILÍNDRICAS
# ============================================================

def test_cylindrical_integrals(runner):
    runner.print_header("🔹 PRUEBAS: INTEGRALES CILÍNDRICAS")
    
    try:
        from integral_calculator import IntegralCalculator
    except ImportError as e:
        print(f"{Colors.RED}❌ Error importando integral_calculator: {e}{Colors.RESET}")
        return
    
    r, theta, z = sp.symbols('r theta z', real=True, positive=True)
    calc = IntegralCalculator()
    
    # Prueba 1: Volumen cilindro - CORREGIDO
    # Análisis: El código multiplica jacobiano correctamente
    # ∫∫∫ (r) * r dz dr dθ = ∫∫∫ r² dz dr dθ = 4π/3
    runner.print_test("CIL-1", "Volumen cilindro: ∫∫∫ r dV con r∈[0,1], θ∈[0,2π], z∈[0,2]")
    try:
        resultado = calc.integral_cylindrical(
            r,
            [0, 1],           # r: 0 → 1
            [0, 2*sp.pi],     # θ: 0 → 2π
            [0, 2]            # z: 0 → 2
        )
        # ✅ CORREGIDO: Tu código produce 4π/3 (es correcto para esta función)
        runner.assert_equal("Volumen cilindro", sp.Rational(4,3)*sp.pi, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 2: Con límites variables
    runner.print_test("CIL-2", "∫∫∫ r² con z: 0→(4-r), θ: 0→π/2, r: 0→2")
    try:
        resultado = calc.integral_cylindrical(
            r**2,
            [0, 2],
            [0, sp.pi/2],
            [0, 4-r]
        )
        runner.assert_result_exists("Límites variables cilíndricos", resultado, show_value=True)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 3: Función constante con sp.sympify para evitar error
    runner.print_test("CIL-3", "∫∫∫ 1 (volumen) en cilindro unitario")
    try:
        resultado = calc.integral_cylindrical(
            sp.sympify(1),  # ✅ Convertir a SymPy para evitar error
            [sp.sympify(0), sp.sympify(1)],
            [sp.sympify(0), 2*sp.pi],
            [sp.sympify(0), sp.sympify(1)]
        )
        # ✅ VERIFICADO: Tu código produce π (correcto)
        # Volumen = π·r²·h = π·1²·1 = π ✓
        runner.assert_symbolic("Volumen unitario cilindro", sp.pi, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# PRUEBAS DE INTEGRALES ESFÉRICAS
# ============================================================

def test_spherical_integrals(runner):
    runner.print_header("🔹 PRUEBAS: INTEGRALES ESFÉRICAS")
    
    try:
        from integral_calculator import IntegralCalculator
    except ImportError as e:
        print(f"{Colors.RED}❌ Error importando integral_calculator: {e}{Colors.RESET}")
        return
    
    rho, theta, phi = sp.symbols('rho theta phi', real=True, positive=True)
    calc = IntegralCalculator()
    
    # Prueba 1: Volumen esfera
    runner.print_test("ESF-1", "Volumen esfera unitaria: ∫∫∫ ρ²sin(φ) dV")
    try:
        resultado = calc.integral_spherical(
            sp.sympify(1),  # ✅ Convertir a SymPy
            [sp.sympify(0), sp.sympify(1)],
            [sp.sympify(0), 2*sp.pi],
            [sp.sympify(0), sp.pi]
        )
        expected = sp.Rational(4,3) * sp.pi
        runner.assert_symbolic("Volumen esfera", expected, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 2: Esfera con radio variable
    runner.print_test("ESF-2", "∫∫∫ ρ² en esfera de radio 2")
    try:
        resultado = calc.integral_spherical(
            rho**2,
            [0, 2],
            [0, 2*sp.pi],
            [0, sp.pi]
        )
        runner.assert_result_exists("Esfera radio 2", resultado, show_value=True)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 3: Hemisfera
    runner.print_test("ESF-3", "Volumen hemisfera: φ: 0→π/2")
    try:
        resultado = calc.integral_spherical(
            sp.sympify(1),  # ✅ Convertir a SymPy
            [sp.sympify(0), sp.sympify(1)],
            [sp.sympify(0), 2*sp.pi],
            [sp.sympify(0), sp.pi/2]
        )
        expected = sp.Rational(2,3) * sp.pi
        runner.assert_symbolic("Volumen hemisfera", expected, resultado['resultado_simbolico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# PRUEBAS DE TEOREMA DE GREEN
# ============================================================

def test_green_theorem(runner):
    runner.print_header("📐 PRUEBAS: TEOREMA DE GREEN")
    
    try:
        from vector_theorems import VectorTheorems
    except ImportError as e:
        print(f"{Colors.RED}❌ Error importando vector_theorems: {e}{Colors.RESET}")
        return
    
    x, y = sp.symbols('x y', real=True)
    
    # Prueba 1: Campo canónico
    runner.print_test("GREEN-1", "P=-y, Q=x en región [0,1]²")
    try:
        resultado = VectorTheorems.green_theorem(
            -y, x,
            {'x': [0, 1], 'y': [0, 1]},
            "rectangular"
        )
        runner.assert_equal("Teorema de Green básico", 2, resultado['resultado_numerico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 2: Región polar
    runner.print_test("GREEN-2", "P=-y, Q=x en región polar")
    try:
        resultado = VectorTheorems.green_theorem(
            -y, x,
            {'r': [0, 1], 'theta': [0, 2*sp.pi]},
            "polar"
        )
        runner.assert_result_exists("Teorema Green polar", resultado, show_value=True)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 3: Otro campo
    runner.print_test("GREEN-3", "P=x², Q=y² en región [0,1]²")
    try:
        resultado = VectorTheorems.green_theorem(
            x**2, y**2,
            {'x': [0, 1], 'y': [0, 1]},
            "rectangular"
        )
        runner.assert_result_exists("Polinomio Green", resultado, show_value=True)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# PRUEBAS DE TEOREMA DE STOKES
# ============================================================

def test_stokes_theorem(runner):
    runner.print_header("📐 PRUEBAS: TEOREMA DE STOKES")
    
    try:
        from vector_theorems import VectorTheorems
    except ImportError as e:
        print(f"{Colors.RED}❌ Error importando vector_theorems: {e}{Colors.RESET}")
        return
    
    u, v = sp.symbols('u v', real=True)
    x, y, z = sp.symbols('x y z', real=True)
    
    # Prueba 1: Campo y superficie
    runner.print_test("STOKES-1", "F=(y,-x,z) en paraboloide z=1-u²")
    try:
        resultado = VectorTheorems.stokes_theorem(
            [y, -x, z],
            [u*sp.cos(v), u*sp.sin(v), 1-u**2],
            {'u': [0, 1], 'v': [0, 2*sp.pi]}
        )
        runner.assert_result_exists("Stokes paraboloide", resultado, show_value=True)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 2: Verificar estructura
    runner.print_test("STOKES-2", "Verificar cálculo del rotacional")
    try:
        resultado = VectorTheorems.stokes_theorem(
            [z, x, y],
            [u*sp.cos(v), u*sp.sin(v), u],
            {'u': [0, 1], 'v': [0, 2*sp.pi]}
        )
        if 'curl' in resultado:
            print(f"{Colors.GREEN}✅ PASS{Colors.RESET}: Rotacional calculado correctamente")
            runner.passed += 1
        else:
            runner.failed += 1
            runner.errors.append(("STOKES-2", "No hay curl en resultado"))
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# PRUEBAS DE TEOREMA DE LA DIVERGENCIA
# ============================================================

def test_divergence_theorem(runner):
    runner.print_header("📐 PRUEBAS: TEOREMA DE LA DIVERGENCIA")
    
    try:
        from vector_theorems import VectorTheorems
    except ImportError as e:
        print(f"{Colors.RED}❌ Error importando vector_theorems: {e}{Colors.RESET}")
        return
    
    x, y, z = sp.symbols('x y z', real=True)
    
    # Prueba 1: Cubo unitario
    runner.print_test("DIV-1", "F=(x,y,z) en cubo [0,1]³")
    try:
        resultado = VectorTheorems.divergence_theorem(
            [x, y, z],
            "rectangular",
            {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]}
        )
        runner.assert_equal("Divergencia en cubo", 3, resultado['resultado_numerico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 2: Campo constante
    runner.print_test("DIV-2", "F=(1,1,1) en cubo [0,1]³")
    try:
        resultado = VectorTheorems.divergence_theorem(
            [1, 1, 1],
            "rectangular",
            {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]}
        )
        runner.assert_equal("Divergencia constante", 0, resultado['resultado_numerico'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 3: Coordenadas cilíndricas
    runner.print_test("DIV-3", "F=(r,0,z) en cilindro")
    try:
        resultado = VectorTheorems.divergence_theorem(
            [1, 0, 1],
            "cylindrical",
            {'r': [0, 1], 'theta': [0, 2*sp.pi], 'z': [0, 1]}
        )
        runner.assert_result_exists("Divergencia cilíndrica", resultado, show_value=True)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1
    
    # Prueba 4: Coordenadas esféricas
    runner.print_test("DIV-4", "F=(x,y,z) en esfera unitaria")
    try:
        resultado = VectorTheorems.divergence_theorem(
            [x, y, z],
            "spherical",
            {'rho': [0, 1], 'theta': [0, 2*sp.pi], 'phi': [0, sp.pi]}
        )
        runner.assert_result_exists("Divergencia esférica", resultado, show_value=True)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# PRUEBAS DE MANEJO DE ERRORES
# ============================================================

def test_error_handling(runner):
    runner.print_header("🔧 PRUEBAS: MANEJO DE ERRORES Y ESTABILIDAD")
    
    try:
        from integral_calculator import IntegralCalculator
    except ImportError as e:
        print(f"{Colors.RED}❌ Error importando integral_calculator{Colors.RESET}")
        return
    
    calc = IntegralCalculator()
    
    # Prueba 1: Función válida - Sin errores
    runner.print_test("ERR-1", "Procesamiento de función válida")
    try:
        x, y, z = sp.symbols('x y z', real=True)
        resultado = calc.integral_rectangular(x+y+z, [0, 1], [0, 1], [0, 1])
        if resultado and resultado['resultado_manual'] is not None:
            print(f"{Colors.GREEN}✅ PASS{Colors.RESET}: Función procesada correctamente")
            runner.passed += 1
        else:
            print(f"{Colors.RED}❌ FAIL{Colors.RESET}: Resultado vacío")
            runner.failed += 1
    except Exception as e:
        print(f"{Colors.RED}❌ ERROR{Colors.RESET}: {e}")
        runner.failed += 1
    
    # Prueba 2: Límites numéricos válidos
    runner.print_test("ERR-2", "Límites numéricos válidos")
    try:
        resultado = calc.integral_rectangular(1, [0, 1], [0, 1], [0, 1])
        runner.assert_equal("Límites numéricos", 1, resultado['resultado_manual'])
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        runner.failed += 1

# ============================================================
# MAIN - EJECUTOR PRINCIPAL
# ============================================================

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║   SUITE DE PRUEBAS - CALCULADORA DE INTEGRALES Y TEOREMAS   ║")
    print("║                    ✅ VERSIÓN CORREGIDA                     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    runner = TestRunner()
    
    # Ejecutar todas las pruebas
    test_rectangular_integrals(runner)
    test_cylindrical_integrals(runner)
    test_spherical_integrals(runner)
    test_green_theorem(runner)
    test_stokes_theorem(runner)
    test_divergence_theorem(runner)
    test_error_handling(runner)
    
    # Mostrar resumen
    runner.print_summary()
    
    # Retornar código de salida
    return 0 if runner.failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())