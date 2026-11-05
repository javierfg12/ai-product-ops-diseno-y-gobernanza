import streamlit as st
from utils.reporting import generate_sdd_markdown, markdown_to_pdf_bytes

st.title("Auditoría & Reporte (Entregable)")
st.subheader("Resumen de diseño (lo que se va a exportar)")
pipeline = st.session_state.get("pipeline_ordered", [])
roles = st.session_state.get("roles", {})
metrics = st.session_state.get("metrics", {})
guardrails = st.session_state.get("guardrails", {})

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Pipeline")
    st.write(pipeline if pipeline else "(no definido)")
    st.markdown("### Roles")
    st.json(roles)
with col2:
    st.markdown("### Métricas")
    st.json(metrics)
    st.markdown("### Guardrails")
    st.json(guardrails)

required_roles = {
    "kill_switch_owner": "Responsable del Kill Switch",
    "data_policy_owner": "Responsable de política de datos",
    "service_owner": "Service Owner",
    "sre_owner": "SRE Owner",
    "data_steward": "Data Steward",
}
required_metrics = {
    "outcome": "Métrica de valor",
    "efficiency": "Métrica de coste",
    "safety": "Métrica de riesgo",
}
missing = [label for key, label in required_roles.items() if not str(roles.get(key, "")).strip()]
missing += [label for key, label in required_metrics.items() if not str(metrics.get(key, "")).strip()]
if not pipeline:
    missing.append("Al menos un componente del pipeline")
try:
    if float(guardrails.get("slo_latencia_s", 0)) <= 0:
        missing.append("SLO de latencia p95 mayor que cero")
except (TypeError, ValueError):
    missing.append("SLO de latencia p95 válido")
try:
    if not 0 <= float(guardrails.get("max_halluc_rate", -1)) <= 1:
        missing.append("Umbral de alucinación entre 0 y 1")
except (TypeError, ValueError):
    missing.append("Umbral de alucinación válido")

st.divider()
st.markdown("## Generar especificación (SDD)")
if missing:
    st.error("No se puede descargar el SDD como entregable final. Completa primero:")
    for item in missing:
        st.markdown(f"- {item}")
else:
    st.success("Validación mínima superada. Puedes descargar el SDD.")

security_gaps = [
    label for component, label in [
        ("Validación Humana", "Validación humana (HITL)"),
        ("Filtro PII", "Filtro de datos personales (PII)"),
        ("Auditoría", "Auditoría y trazabilidad"),
    ] if component not in pipeline
]
if security_gaps:
    st.warning("Controles recomendados que faltan en el pipeline: " + ", ".join(security_gaps))

md = generate_sdd_markdown(st.session_state)
st.code(md, language="markdown")
c1, c2 = st.columns(2)
with c1:
    st.download_button(
        "Descargar SDD (.md)", data=md.encode("utf-8"),
        file_name="sdd_ai_product_ops.md", mime="text/markdown",
        use_container_width=True, disabled=bool(missing),
    )
with c2:
    pdf_bytes = markdown_to_pdf_bytes(md)
    st.download_button(
        "Descargar SDD (.pdf)", data=pdf_bytes,
        file_name="sdd_ai_product_ops.pdf", mime="application/pdf",
        use_container_width=True, disabled=bool(missing),
    )
st.caption("El PDF usa render básico; el Markdown es la fuente editable. El simulador no incluye todos los costes de operación.")
