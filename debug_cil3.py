from integral_calculator import IntegralCalculator
import sympy as sp

print("\n" + "="*80)
print("DIAGNÓSTICO DE CIL-3 - VOLUMEN UNITARIO CILINDRO")
print("="*80)

calc = IntegralCalculator()

print("\n📌 Parámetros de entrada:")
print("   Función: 1 (constante)")
print("   r: [0, 1]")
print("   θ: [0, 2π]")
print("   z: [0, 1]")

print("\n" + "="*80)
print("EJECUTANDO...")
print("="*80)

resultado = calc.integral_cylindrical(
    sp.sympify(1),
    [sp.sympify(0), sp.sympify(1)],
    [sp.sympify(0), 2*sp.pi],
    [sp.sympify(0), sp.sympify(1)]
)

print("\n" + "="*80)
print("RESULTADO FINAL")
print("="*80)
print(f"\n✓ Resultado simbólico: {resultado['resultado_simbolico']}")
print(f"✓ Resultado numérico: {resultado['resultado_manual']}")

print("\n" + "="*80)
print("PASOS DETALLADOS")
print("="*80)
print(resultado['pasos'])

print("\n" + "="*80)
print("ANÁLISIS")
print("="*80)

resultado_simbolico = resultado['resultado_simbolico']
esperado = sp.pi

print(f"\nEsperado: {esperado}")
print(f"Obtenido: {resultado_simbolico}")
print(f"¿Son iguales? {resultado_simbolico == esperado}")

if resultado_simbolico == 2*sp.pi:
    print("\n⚠️  TU CÓDIGO PRODUCE 2π EN LUGAR DE π")
    print("    Esto significa que está integrando z de 0 a 2, no de 0 a 1")
    print("    O hay un Jacobiano extra multiplicando")
elif resultado_simbolico == sp.pi:
    print("\n✅ TU CÓDIGO PRODUCE π (CORRECTO)")
else:
    print(f"\n❓ TU CÓDIGO PRODUCE: {resultado_simbolico}")
    print(f"   Diferencia con π: {float(resultado_simbolico) - float(sp.pi)}")
    