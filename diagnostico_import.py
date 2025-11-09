"""
DIAGNÓSTICO DE IMPORTACIÓN
Verifica qué hay realmente en integral_calculator.py
"""

import sys
import os

print("="*70)
print("DIAGNÓSTICO DE MÓDULO integral_calculator")
print("="*70)

try:
    import integral_calculator
    print("\n✅ Módulo importado correctamente")
    print(f"   Ubicación: {integral_calculator.__file__}")
except Exception as e:
    print(f"\n❌ Error importando módulo: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("CONTENIDO DEL MÓDULO")
print("="*70)

contenido = dir(integral_calculator)
print(f"\nTotal de elementos: {len(contenido)}")
print("\nElementos disponibles:")
for item in sorted(contenido):
    if not item.startswith('_'):
        obj = getattr(integral_calculator, item)
        print(f"  • {item}: {type(obj).__name__}")

print("\n" + "="*70)
print("BÚSQUEDA DE IntegralCalculator")
print("="*70)

if hasattr(integral_calculator, 'IntegralCalculator'):
    print("✅ IntegralCalculator ENCONTRADA")
    IntCalc = getattr(integral_calculator, 'IntegralCalculator')
    print(f"   Tipo: {type(IntCalc)}")
    print(f"   Métodos:")
    for method in dir(IntCalc):
        if not method.startswith('_'):
            print(f"     - {method}")
else:
    print("❌ IntegralCalculator NO ENCONTRADA")
    print("\nClases disponibles:")
    for item in contenido:
        obj = getattr(integral_calculator, item)
        if isinstance(obj, type):
            print(f"  • {item}")

print("\n" + "="*70)
print("SOLUCIÓN")
print("="*70)

print("""
Si IntegralCalculator NO está en el módulo:

OPCIÓN 1: Agregar exportación en integral_calculator.py
   Al final del archivo, agregar:
   
   __all__ = ['IntegralCalculator']

OPCIÓN 2: Si está dentro de una función, necesitas moverla al nivel superior

OPCIÓN 3: El archivo integral_calculator.py no tiene la clase

Revisa que integral_calculator.py tenga:
   class IntegralCalculator:
       @staticmethod
       def integral_rectangular(...):
""")