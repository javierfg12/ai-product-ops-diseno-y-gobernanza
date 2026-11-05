import unittest

from utils.economics import CostInputs, compute_costs


class ComputeCostsTests(unittest.TestCase):
    def test_cost_breakdown_uses_expected_assumptions(self):
        result = compute_costs(CostInputs(
            tickets=1000,
            tokens_por_ticket=800,
            eur_por_1k_tokens=0.80,
            fcr=0.75,
            coste_hora_agente=24.0,
            aht_min=15.0,
        ))
        self.assertEqual(result["tokens_total"], 800000)
        self.assertAlmostEqual(result["coste_ti"], 640.0)
        self.assertAlmostEqual(result["coste_ticket_humano"], 6.0)
        self.assertAlmostEqual(result["coste_operativo"], 1500.0)
        self.assertAlmostEqual(result["coste_total"], 2140.0)

    def test_rejects_fcr_outside_zero_and_one(self):
        with self.assertRaises(ValueError):
            CostInputs(100, 500, 0.8, 1.2, 25.0, 15.0)

    def test_rejects_negative_cost(self):
        with self.assertRaises(ValueError):
            CostInputs(100, 500, -0.1, 0.7, 25.0, 15.0)

    def test_rejects_zero_tickets(self):
        with self.assertRaises(ValueError):
            CostInputs(0, 500, 0.8, 0.7, 25.0, 15.0)


if __name__ == "__main__":
    unittest.main()
