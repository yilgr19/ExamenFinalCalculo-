"""
TEST FINAL VERIFICADO - SUITE COMPLETA DE PRUEBAS
Archivo: test_final.py
Ejecutar: python test_final.py

Este test funciona con el código correcto de integral_calculator.py
"""

import sys
import sympy as sp
from datetime import datetime

# Limpiar caché
for mod in list(sys.modules.keys()):
    if 'integral' in mod or 'vector' in mod or 'test' in mod:
        del sys.modules[mod]

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.start_time = datetime.now()
    
    def print_header(self, title):
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{title:^75}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}\n")
    
    def print_test(self, test_name, desc):
        print(f"\n{Colors.BOLD}{test_name}: {desc}{Colors.RESET}")
        print("-" * 75)
    
    def pass_test(self, msg=""):
        self.passed += 1
        print(f"   {Colors.GREEN}✅ PASS{Colors.RESET} {msg}")
    
    def fail_test(self, msg=""):
        self.failed += 1
        print(f"   {Colors.RED}❌ FAIL{Colors.RESET} {msg}")
    
    def error_test(self, msg=""):
        self.failed += 1
        print(f"   {Colors.RED}❌ ERROR{Colors.RESET}: {msg}")
    
    def print_summary(self):
        elapsed = (datetime.now() - self.start_time).total_seconds()
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}📊 RESUMEN FINAL{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}")
        print(f"{Colors.GREEN}✅ Pasadas: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}❌ Fallidas: {self.failed}{Colors.RESET}")
        print(f"📊 Total: {total}")
        print(f"📈 Éxito: {percentage:.1f}%")
        print(f"⏱️  Tiempo: {elapsed:.2f}s\n")

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔" + "="*73 + "╗")
    print("║" + " "*15 + "🧮 TEST SUITE FINAL - VERSIÓN 8.0 🧮" + " "*18 + "║")
    print("║" + " "*12 + "INTEGRALES TRIPLES Y TEOREMAS VECTORIALES" + " "*16 + "║")
    print("╚" + "="*73 + "╝")
    print(f"{Colors.RESET}\n")
    
    runner = TestRunner()
    
    # ===== CARGAR MÓDULOS =====
    print(f"{Colors.BOLD}📦 Cargando módulos...{Colors.RESET}\n")
    
    # Importar integral_calculator
    try:
        from integral_calculator import IntegralCalculator
        print(f"{Colors.GREEN}✅ IntegralCalculator importado{Colors.RESET}")
        ic_available = True
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        ic_available = False
    
    # Importar vector_theorems
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
    
    # ===== PRUEBAS INTEGRALES RECTANGULARES =====
    if ic_available:
        runner.print_header("📕 INTEGRALES RECTANGULARES")
        
        x, y, z = sp.symbols('x y z', real=True)
        
        # REC-1: Volumen unitario
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
        
        # REC-2: Límites variables
        runner.print_test("REC-2", "Límites variables (y=2-x)")
        try:
            result = IntegralCalculator.integral_rectangular(x+y, [0, 2], [0, 2-x], [0, 1])
            expected = sp.Rational(8, 3)
            diff = sp.simplify(result['resultado_simbolico'] - expected)
            if diff == 0:
                runner.pass_test(f"✓ Resultado: 8/3")
            else:
                runner.fail_test(f"Esperado 8/3, obtenido {result['resultado_simbolico']}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # REC-3: Suma de cuadrados
        runner.print_test("REC-3", "Suma de cuadrados (x² + y² + z²)")
        try:
            result = IntegralCalculator.integral_rectangular(x**2+y**2+z**2, [0, 1], [0, 1], [0, 1])
            val = float(result['resultado_manual'])
            if abs(val - 1.0) < 1e-4:
                runner.pass_test(f"✓ Resultado: {val}")
            else:
                runner.fail_test(f"Esperado 1.0, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # REC-4: Tetraedro
        runner.print_test("REC-4", "Tetraedro (1-x-y, 1-x)")
        try:
            result = IntegralCalculator.integral_rectangular(1, [0, 1], [0, 1-x], [0, 1-x-y])
            expected = sp.Rational(1, 6)
            diff = sp.simplify(result['resultado_simbolico'] - expected)
            if diff == 0:
                runner.pass_test(f"✓ Resultado: 1/6")
            else:
                runner.fail_test(f"Esperado 1/6, obtenido {result['resultado_simbolico']}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # REC-5: Exponencial
        runner.print_test("REC-5", "Exponencial (e^(x+y+z))")
        try:
            result = IntegralCalculator.integral_rectangular(sp.exp(x+y+z), [0, 1], [0, 1], [0, 1])
            expected = (sp.exp(1)-1)**3
            diff = sp.simplify(result['resultado_simbolico'] - expected)
            if diff == 0:
                runner.pass_test(f"✓ Resultado correcto")
            else:
                runner.fail_test(f"Diferencia: {diff}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # ===== INTEGRALES CILÍNDRICAS =====
        runner.print_header("🟢 INTEGRALES CILÍNDRICAS")
        
        r, theta = sp.symbols('r theta', real=True, positive=True)
        
        # CIL-1: Cilindro
        runner.print_test("CIL-1", "Cilindro (r=2, h=3)")
        try:
            result = IntegralCalculator.integral_cylindrical(r, [0, 2], [0, 2*sp.pi], [0, 3])
            expected = 16*sp.pi
            diff = sp.simplify(result['resultado_simbolico'] - expected)
            if diff == 0:
                runner.pass_test(f"✓ Resultado: 16π")
            else:
                runner.fail_test(f"Esperado 16π, obtenido {result['resultado_simbolico']}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # CIL-2: Con z=r²
        runner.print_test("CIL-2", "Límite variable (z=r²)")
        try:
            result = IntegralCalculator.integral_cylindrical(r, [0, 1], [0, 2*sp.pi], [0, r**2])
            expected = 2*sp.pi/5
            diff = sp.simplify(result['resultado_simbolico'] - expected)
            if diff == 0:
                runner.pass_test(f"✓ Resultado: 2π/5")
            else:
                runner.fail_test(f"Esperado 2π/5, obtenido {result['resultado_simbolico']}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # CIL-3: Trigonometría
        runner.print_test("CIL-3", "Trigonometría (r·sin(θ))")
        try:
            result = IntegralCalculator.integral_cylindrical(r*sp.sin(theta), [0, 1], [0, sp.pi], [0, 1])
            expected = sp.Rational(2, 3)
            diff = sp.simplify(result['resultado_simbolico'] - expected)
            if diff == 0:
                runner.pass_test(f"✓ Resultado: 2/3")
            else:
                runner.fail_test(f"Esperado 2/3, obtenido {result['resultado_simbolico']}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # ===== INTEGRALES ESFÉRICAS =====
        runner.print_header("🔵 INTEGRALES ESFÉRICAS")
        
        rho, phi = sp.symbols('rho phi', real=True, positive=True)
        
        # ESF-1: Esfera radio 2
        runner.print_test("ESF-1", "Esfera (radio=2)")
        try:
            result = IntegralCalculator.integral_spherical(1, [0, 2], [0, 2*sp.pi], [0, sp.pi])
            expected = sp.Rational(32, 3)*sp.pi
            diff = sp.simplify(result['resultado_simbolico'] - expected)
            if diff == 0:
                runner.pass_test(f"✓ Resultado: (32/3)π")
            else:
                runner.fail_test(f"Esperado (32/3)π, obtenido {result['resultado_simbolico']}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # ESF-2: Cuarto de esfera
        runner.print_test("ESF-2", "Cuarto de esfera")
        try:
            result = IntegralCalculator.integral_spherical(1, [0, 1], [0, sp.pi], [0, sp.pi/2])
            expected = sp.pi/3
            diff = sp.simplify(result['resultado_simbolico'] - expected)
            if diff == 0:
                runner.pass_test(f"✓ Resultado: π/3")
            else:
                runner.fail_test(f"Esperado π/3, obtenido {result['resultado_simbolico']}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # ESF-3: ρ⁴
        runner.print_test("ESF-3", "Potencia (ρ⁴)")
        try:
            result = IntegralCalculator.integral_spherical(rho**4, [0, 1], [0, 2*sp.pi], [0, sp.pi])
            expected = sp.Rational(4, 7)*sp.pi
            diff = sp.simplify(result['resultado_simbolico'] - expected)
            if diff == 0:
                runner.pass_test(f"✓ Resultado: (4/7)π")
            else:
                runner.fail_test(f"Esperado (4/7)π, obtenido {result['resultado_simbolico']}")
        except Exception as e:
            runner.error_test(str(e)[:60])
    
    # ===== TEOREMAS VECTORIALES =====
    if vt_available:
        runner.print_header("📐 TEOREMAS VECTORIALES")
        
        x, y, z = sp.symbols('x y z', real=True)
        u, v = sp.symbols('u v', real=True)
        
        # GREEN-1
        runner.print_test("GREEN-1", "Teorema de Green (P=-y, Q=x)")
        try:
            result = VectorTheorems.green_theorem(-y, x, {'x': [0, 1], 'y': [0, 1]}, "rectangular")
            val = float(result['resultado_numerico'])
            if abs(val - 2.0) < 1e-4:
                runner.pass_test(f"✓ Resultado: {val}")
            else:
                runner.fail_test(f"Esperado 2.0, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # STOKES-1
        runner.print_test("STOKES-1", "Teorema de Stokes")
        try:
            F = [y, -x, z]
            params = [u*sp.cos(v), u*sp.sin(v), 1-u**2]
            bounds = {'u': [0, 1], 'v': [0, 2*sp.pi]}
            result = VectorTheorems.stokes_theorem(F, params, bounds)
            if result['resultado_simbolico'] != 0:
                runner.pass_test(f"✓ Resultado: {result['resultado_simbolico']}")
            else:
                runner.fail_test("Resultado inesperado (0)")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # DIV-1
        runner.print_test("DIV-1", "Divergencia en cubo (F=(x,y,z))")
        try:
            result = VectorTheorems.divergence_theorem([x, y, z], "rectangular", 
                                                     {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]})
            val = float(result['resultado_numerico'])
            if abs(val - 3.0) < 1e-4:
                runner.pass_test(f"✓ Resultado: {val}")
            else:
                runner.fail_test(f"Esperado 3.0, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # DIV-2
        runner.print_test("DIV-2", "Divergencia - Campo constante (F=(1,1,1))")
        try:
            result = VectorTheorems.divergence_theorem([1, 1, 1], "rectangular",
                                                     {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]})
            val = float(result['resultado_numerico'])
            if abs(val - 0.0) < 1e-4:
                runner.pass_test(f"✓ Resultado: {val}")
            else:
                runner.fail_test(f"Esperado 0.0, obtenido {val}")
        except Exception as e:
            runner.error_test(str(e)[:60])
        
        # DIV-3
        runner.print_test("DIV-3", "Divergencia en esfera (F=(x,y,z))")
        try:
            result = VectorTheorems.divergence_theorem([x, y, z], "spherical",
                                                     {'rho': [0, 1], 'theta': [0, 2*sp.pi], 'phi': [0, sp.pi]})
            expected = 4*sp.pi
            diff = sp.simplify(result['resultado_simbolico'] - expected)
            if diff == 0:
                runner.pass_test(f"✓ Resultado: 4π")
            else:
                runner.fail_test(f"Esperado 4π, obtenido {result['resultado_simbolico']}")
        except Exception as e:
            runner.error_test(str(e)[:60])
    
    runner.print_summary()
    return 0 if runner.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())