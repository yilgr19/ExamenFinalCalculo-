# Calculadora de Integrales Triples

## Descripción
Esta aplicación permite calcular integrales triples en diferentes sistemas de coordenadas:
- Coordenadas rectangulares
- Coordenadas cilíndricas
- Coordenadas esféricas

## Requisitos
- Python 3.8+
- Tkinter (generalmente incluido con Python)
- SymPy
- NumPy

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu_usuario/calculadora-integrales-triples.git
cd calculadora-integrales-triples
```

2. Crear un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecutar la aplicación:
```bash
python app.py
```

### Instrucciones de Uso

1. Selecciona el sistema de coordenadas (rectangular, cilíndrico o esférico)
2. Introduce la función a integrar
3. Define los límites de integración
4. Haz clic en "Calcular Integral"

## Ejemplos de Funciones

### Coordenadas Rectangulares
- `x*y*z`
- `x**2 + y**2 + z**2`

### Coordenadas Cilíndricas
- `r**2 * sin(theta)`
- `r * cos(theta)`

### Coordenadas Esféricas
- `rho**2 * sin(phi)`
- `rho * cos(theta) * sin(phi)`

## Notas
- Usa la sintaxis de SymPy para funciones matemáticas
- Asegúrate de usar los símbolos correctos según el sistema de coordenadas
- Los límites deben ser números o expresiones válidas

## Licencia
[Especificar la licencia]
