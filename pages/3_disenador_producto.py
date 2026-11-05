import streamlit as st
import pandas as pd

st.title("Diseñador de Producto (Wizard)")
steps = ["1) Flujo", "2) Roles", "3) Métricas & Guardrails"]
step = st.radio("Paso", steps, horizontal=True)

if step == steps[0]:
    st.subheader("Paso 1 — Definir el flujo (Process & Tech)")
    available = ["Auth", "RAG", "Inferencia", "Validación Humana", "Filtro PII", "Auditoría"]
    selected = st.multiselect(
        "Selecciona componentes del pipeline",
        options=available,
        default=st.session_state.get("pipeline_selected", ["Auth", "RAG", "Inferencia", "Auditoría"]),
    )
    st.session_state["pipeline_selected"] = selected
    st.markdown("#### Ordena el pipeline (edita la columna **Orden**)")
    df = pd.DataFrame({"Paso": selected, "Orden": list(range(1, len(selected) + 1))})
    edited = st.data_editor(
        df, hide_index=True, use_container_width=True, num_rows="fixed",
        column_config={
            "Paso": st.column_config.TextColumn("Paso", disabled=True),
            "Orden": st.column_config.NumberColumn(
                "Orden", min_value=1, max_value=max(len(selected), 1), step=1, format="%d"
            ),
        },
    )
    order_values = pd.to_numeric(edited["Orden"], errors="coerce")
    valid_order = (
        len(edited) == len(selected)
        and edited["Paso"].isin(selected).all()
        and edited["Paso"].nunique() == len(selected)
        and order_values.notna().all()
        and (order_values % 1 == 0).all()
        and sorted(order_values.astype(int).tolist()) == list(range(1, len(selected) + 1))
    )
    if valid_order:
        st.session_state["pipeline_ordered"] = (
            edited.assign(_orden=order_values.astype(int)).sort_values("_orden")["Paso"].tolist()
        )
    elif selected:
        st.warning("Orden no válido: usa una posición única y consecutiva para cada componente. Se conserva el último orden válido.")
    else:
        st.session_state["pipeline_ordered"] = []
        st.info("Selecciona al menos un componente para definir el pipeline.")
    if "Validación Humana" not in selected:
        st.warning("Peligro: falta Human-in-the-loop (Validación Humana).")
    if "Auditoría" not in selected:
        st.warning("Peligro: falta trazabilidad (Auditoría).")
    if "Filtro PII" not in selected:
        st.warning("Revisa la protección de datos: falta un Filtro PII.")

elif step == steps[1]:
    st.subheader("Paso 2 — Asignación de roles (People)")
    roles = st.session_state["roles"]
    col1, col2 = st.columns(2)
    with col1:
        kill_options = ["", "SRE", "Product Owner", "Dev Lead"]
        policy_options = ["", "Legal", "Data Steward", "CISO"]
        kill_current = roles.get("kill_switch_owner", "")
        policy_current = roles.get("data_policy_owner", "")
        roles["kill_switch_owner"] = st.selectbox(
            "¿Quién pulsa el Kill Switch?", options=kill_options,
            index=kill_options.index(kill_current if kill_current in kill_options else ""),
        )
        roles["data_policy_owner"] = st.selectbox(
            "¿Quién define política de datos?", options=policy_options,
            index=policy_options.index(policy_current if policy_current in policy_options else ""),
        )
    with col2:
        roles["service_owner"] = st.text_input("Service Owner (nombre)", value=roles.get("service_owner", ""))
        roles["sre_owner"] = st.text_input("SRE Owner (nombre)", value=roles.get("sre_owner", ""))
        roles["data_steward"] = st.text_input("Data Steward (nombre)", value=roles.get("data_steward", ""))
    st.session_state["roles"] = roles
    if any(not str(value).strip() for value in roles.values()):
        st.warning("Quedan responsabilidades sin asignar.")
    else:
        st.success("Todos los roles mínimos tienen responsable asignado.")

else:
    st.subheader("Paso 3 — Métricas y Guardrails (Data & Policy)")
    metrics = st.session_state["metrics"]
    guardrails = st.session_state["guardrails"]
    guide = pd.DataFrame([
        {"Tipo": "Outcome (Valor)", "Ejemplo": "FCR, CSAT, tiempo a resolución"},
        {"Tipo": "Efficiency (Coste)", "Ejemplo": "€/ticket, tokens/ticket, % escalados"},
        {"Tipo": "Safety (Riesgo)", "Ejemplo": "tasa alucinación, fuga PII, errores críticos"},
    ])
    st.table(guide)
    metrics["outcome"] = st.text_input("Métrica de Valor (Outcome)", value=metrics.get("outcome", ""))
    metrics["efficiency"] = st.text_input("Métrica de Coste (Efficiency)", value=metrics.get("efficiency", ""))
    metrics["safety"] = st.text_input("Métrica de Riesgo (Safety)", value=metrics.get("safety", ""))
    guardrails["slo_latencia_s"] = st.number_input(
        "SLO Latencia p95 (seg)", min_value=0.1,
        value=float(guardrails.get("slo_latencia_s", 2.0)), step=0.1,
    )
    guardrails["max_halluc_rate"] = st.number_input(
        "Umbral alucinación (0..1)", min_value=0.0, max_value=1.0,
        value=float(guardrails.get("max_halluc_rate", 0.02)), step=0.01,
    )
    st.session_state["metrics"] = metrics
    st.session_state["guardrails"] = guardrails
    if any(not str(value).strip() for value in metrics.values()):
        st.warning("Completa las tres métricas obligatorias: valor, coste y riesgo.")
    else:
        st.success("Las tres métricas están definidas.")
    st.info("Mínimo exigible: 3 métricas (valor/coste/riesgo) + 1 SLO con umbral numérico.")
