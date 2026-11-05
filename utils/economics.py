from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class CostInputs:
    tickets: int
    tokens_por_ticket: int
    eur_por_1k_tokens: float
    fcr: float  # 0..1
    coste_hora_agente: float
    aht_min: float

    def __post_init__(self):
        if isinstance(self.tickets, bool) or not isinstance(self.tickets, int) or self.tickets < 1:
            raise ValueError("tickets debe ser un entero mayor o igual que 1")
        if isinstance(self.tokens_por_ticket, bool) or not isinstance(self.tokens_por_ticket, int) or self.tokens_por_ticket < 0:
            raise ValueError("tokens_por_ticket debe ser un entero no negativo")
        numeric_values = {
            "eur_por_1k_tokens": self.eur_por_1k_tokens,
            "fcr": self.fcr,
            "coste_hora_agente": self.coste_hora_agente,
            "aht_min": self.aht_min,
        }
        for name, value in numeric_values.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
                raise ValueError(f"{name} debe ser un número finito")
        if self.eur_por_1k_tokens < 0:
            raise ValueError("eur_por_1k_tokens no puede ser negativo")
        if not 0 <= self.fcr <= 1:
            raise ValueError("fcr debe estar entre 0 y 1")
        if self.coste_hora_agente < 0 or self.aht_min < 0:
            raise ValueError("Los costes y tiempos no pueden ser negativos")

def compute_costs(x: CostInputs) -> dict:
    """
    Estimación simplificada: tokens * precio + tickets no resueltos por IA
    * AHT completo * coste/hora. No incluye configuración, mantenimiento,
    licencias, supervisión ni otros costes de operación.
    """
    tokens_total = x.tickets * x.tokens_por_ticket
    coste_ti = (tokens_total / 1000.0) * x.eur_por_1k_tokens

    coste_ticket_humano = (x.aht_min / 60.0) * x.coste_hora_agente
    coste_operativo = x.tickets * (1.0 - x.fcr) * coste_ticket_humano

    return {
        "tokens_total": tokens_total,
        "coste_ti": coste_ti,
        "coste_ticket_humano": coste_ticket_humano,
        "coste_operativo": coste_operativo,
        "coste_total": coste_ti + coste_operativo,
    }
