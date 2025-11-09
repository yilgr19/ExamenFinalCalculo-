"""
REPARADOR AUTOMÁTICO - integral_calculator.py
Envuelve el código en la clase IntegralCalculator
"""

import os
import re

print("="*70)
print("REPARADOR: Agregando clase IntegralCalculator")
print("="*70)

# Leer el archivo
try:
    with open('integral_calculator.py', 'r', encoding='utf-8') as f:
        contenido = f.read()
    print("\n✅ Archivo leído")
except FileNotFoundError:
    print("\n❌ Error: integral_calculator.py no encontrado")
    exit(1)

# Verificar si ya tiene clase
if 'class IntegralCalculator' in contenido:
    print("✅ Ya tiene la clase")
    exit(0)

# Crear backup
with open('integral_calculator.py.backup', 'w', encoding='utf-8') as f:
    f.write(contenido)
print("✅ Backup: integral_calculator.py.backup")

# Separar en secciones
lineas = contenido.split('\n')

# Encontrar donde comienzan los métodos @staticmethod
inicio_clase = 0
for i, linea in enumerate(lineas):
    if '@staticmethod' in linea:
        inicio_clase = i
        break

print(f"\n📍 Inicio de métodos: línea {inicio_clase}")

# Encontrar donde termina la clase (before if __name__)
fin_clase = len(lineas)
for i, linea in enumerate(lineas):
    if 'if __name__' in linea:
        fin_clase = i
        break

print(f"📍 Fin de métodos: línea {fin_clase}")

# Construir el nuevo archivo
nuevo = []

# Agregar imports y cosas antes de la clase
nuevo.extend(lineas[:inicio_clase])

# Agregar la definición de clase
nuevo.append('class IntegralCalculator:')
nuevo.append('    """Calculadora de integrales triples"""')
nuevo.append('    ')

# Indentar todos los métodos
for i in range(inicio_clase, fin_clase):
    linea = lineas[i]
    if linea.strip():  # Si no está vacía
        nuevo.append('    ' + linea)
    else:
        nuevo.append('')

# Agregar el código después (if __name__)
nuevo.append('')
nuevo.extend(lineas[fin_clase:])

# Escribir el archivo
contenido_nuevo = '\n'.join(nuevo)

with open('integral_calculator.py', 'w', encoding='utf-8') as f:
    f.write(contenido_nuevo)

print("✅ Archivo reparado")

# Verificar que funciona
print("\n🔍 Verificando importación...")
try:
    # Recargar el módulo
    import importlib
    import sys
    if 'integral_calculator' in sys.modules:
        del sys.modules['integral_calculator']
    
    import integral_calculator
    
    if hasattr(integral_calculator, 'IntegralCalculator'):
        cls = integral_calculator.IntegralCalculator
        metodos = [m for m in dir(cls) if not m.startswith('_')]
        print(f"\n✅ ¡Éxito! Clase encontrada")
        print(f"   Métodos: {metodos}")
    else:
        print("❌ Clase no encontrada")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("✅ REPARACIÓN COMPLETA")
print("="*70)
print("\nAhora ejecuta:")
print("  python test_suite.py")
print("="*70)