import unittest

from utils.reporting import generate_sdd_markdown, markdown_to_pdf_bytes


class ReportingTests(unittest.TestCase):
    def valid_state(self):
        return {
            "pipeline_ordered": ["Auth", "RAG", "Filtro PII", "Inferencia", "Validación Humana", "Auditoría"],
            "roles": {
                "kill_switch_owner": "SRE",
                "data_policy_owner": "CISO",
                "service_owner": "Ana",
                "sre_owner": "Luis",
                "data_steward": "Marta",
            },
            "metrics": {
                "outcome": "FCR",
                "efficiency": "€/ticket",
                "safety": "Errores críticos",
            },
            "guardrails": {"slo_latencia_s": 2.0, "max_halluc_rate": 0.02},
            "sim": {
                "preset": "Base",
                "eur_por_1k_tokens": 0.8,
                "fcr": 0.75,
                "tickets": 1000,
                "tokens_por_ticket": 800,
                "coste_ti": 640.0,
                "coste_operativo": 1500.0,
                "coste_total": 2140.0,
            },
        }

    def test_sdd_includes_pipeline_roles_and_partial_cost_note(self):
        md = generate_sdd_markdown(self.valid_state())
        self.assertIn("1. Auth", md)
        self.assertIn("Service Owner", md)
        self.assertIn("Coste Total estimado", md)
        self.assertIn("estimación parcial", md)

    def test_missing_role_is_not_reported_as_complete(self):
        state = self.valid_state()
        state["roles"]["sre_owner"] = "   "
        md = generate_sdd_markdown(state)
        self.assertIn("- [ ] SRE Owner asignado", md)
        self.assertIn("- [ ] RBAC/roles mínimos completos", md)

    def test_missing_security_components_are_flagged(self):
        state = self.valid_state()
        state["pipeline_ordered"] = ["Auth", "Inferencia"]
        md = generate_sdd_markdown(state)
        self.assertIn("- [ ] Auditoría/Logs activados", md)
        self.assertIn("- [ ] Validación humana (HITL)", md)
        self.assertIn("- [ ] Filtro PII", md)

    def test_pdf_export_returns_pdf_bytes(self):
        pdf = markdown_to_pdf_bytes("# SDD de prueba\n\n- Primer punto\n- Segundo punto")
        self.assertTrue(pdf.startswith(b"%PDF"))
        self.assertGreater(len(pdf), 500)


if __name__ == "__main__":
    unittest.main()
