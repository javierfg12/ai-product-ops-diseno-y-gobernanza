# AI Product Ops — De modelo a sistema

Aplicación didáctica desarrollada con Streamlit para diseñar y evaluar sistemas de IA desde una perspectiva de producto y operación.

## Qué permite hacer
- Explorar un framework de diseño basado en People, Process, Data, Tech y Policy.
- Simular el equilibrio entre coste de inferencia (TI) y coste de retrabajo humano (SI).
- Diseñar un pipeline de componentes y ordenar su ejecución.
- Asignar responsables de operación, seguridad y datos.
- Definir métricas de valor, eficiencia y riesgo, además de guardrails.
- Generar una especificación de diseño (SDD) en Markdown y PDF.

## Requisitos y ejecución
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Validaciones y supuestos
- El pipeline solo acepta componentes disponibles y posiciones únicas y consecutivas.
- El SDD final solo se puede descargar cuando están definidos los cinco responsables mínimos, las tres métricas, el pipeline y los umbrales válidos.
- La checklist de RBAC comprueba cada responsable; no basta con que exista un diccionario de roles.
- El simulador estima coste de tokens y coste humano de los tickets que la IA no resuelve, suponiendo que cada uno consume el AHT completo.
- El coste total es parcial: no incluye configuración, licencias, mantenimiento, supervisión ni otros costes indirectos.

## Pruebas
Ejecuta las pruebas unitarias de economía desde la raíz del proyecto:
```bash
python -m unittest discover -s tests -v
```

## Alcance
Es un prototipo educativo de apoyo a decisiones. No conecta con servicios de IA ni despliega infraestructura real. Los resultados dependen de los supuestos introducidos y deben validarse con datos operativos antes de utilizarlos en decisiones de producción.
