# Arquitectura y decisiones — AI Product Ops

## Objetivo

Mantener una separación sencilla entre interfaz, estado de sesión, reglas económicas y generación de documentación. La aplicación es un prototipo local; no existe backend persistente.

## Componentes

| Componente | Responsabilidad |
|---|---|
| `app.py` | Inicializa estado compartido y navegación multipágina |
| `pages/1_home_framework.py` | Marco de diseño del producto |
| `pages/2_simulador_ti_vs_si.py` | Comparación económica TI/SI |
| `pages/3_disenador_producto.py` | Pipeline, roles, métricas y guardrails |
| `pages/4_auditoria_reporte.py` | Checklist y exportación |
| `utils/economics.py` | Validación y cálculos económicos |
| `utils/reporting.py` | Construcción del SDD y PDF |
| `tests/` | Pruebas unitarias de reglas y reporting |

## Flujo de datos

1. El usuario introduce parámetros en una página Streamlit.
2. Los datos de trabajo se almacenan en `st.session_state`.
3. Las funciones de economía validan entradas y calculan estimaciones.
4. El diseñador valida componentes, orden, responsables, métricas y guardrails.
5. El generador construye un SDD a partir del estado de sesión.
6. La exportación produce Markdown o PDF.

## Decisiones de diseño

- **Streamlit:** permite iterar rápidamente sobre un prototipo de flujo de trabajo sin construir una API y un frontend separados.
- **Estado de sesión:** mantiene los datos durante la navegación multipágina, pero no ofrece persistencia entre sesiones.
- **Reglas puras en utilidades:** facilita pruebas sin levantar la interfaz.
- **SDD como artefacto:** hace explícitas decisiones, supuestos y controles para revisión posterior.
- **Coste parcial explícito:** evita presentar como ROI neto una estimación que no descuenta todos los costes.

## Límites conocidos y evolución

- Persistir especificaciones y auditoría en una base de datos.
- Añadir autenticación y autorización reales; los campos de responsable no equivalen a RBAC implementado.
- Incorporar evaluación de calidad del modelo, conjuntos de prueba y métricas observadas.
- Añadir costes de licencias, configuración, mantenimiento, supervisión y fallback humano.
- Exportar un registro versionado de cambios y aprobaciones.
- Añadir pruebas de integración de Streamlit y validación de accesibilidad.
