"""
Variante 2: Repetición en T Rondas con Nodos que Fallan entre Rondas
Proyecto Semestral 2026-B - Subproyecto 2

Modela la dinámica temporal del sistema de Aprendizaje Federado a lo largo de T rondas:
1. Fallas estocásticas independientes: cada nodo falla con probabilidad q.
2. Presupuesto acumulativo de ruido por nodo.
3. Comparación experimental de dos políticas de gasto de presupuesto:
   - Política Uniforme: B_t = B_total / T en cada ronda.
   - Política Front-Loaded (Decaimiento Geométrico): asigna más presupuesto al inicio.

Complejidad Temporal Teórica Derivada:
T_total = O(T * (N * k * tau + N + B * log N))
"""

import random
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass, field
from src.core.models import FederatedNode, RoundState
from src.parte2_seleccion.submodular_greedy import SubmodularGreedySelector
from src.parte1_reparto.greedy_budget import GreedyBudgetAllocator


@dataclass
class MultiRoundSimulationResult:
    """Resultados consolidados de una simulación a lo largo de T rondas."""
    policy_name: str
    total_rounds: int
    cumulative_utility_per_round: List[float]
    round_utilities: List[float]
    round_coverages: List[int]
    total_active_participations: int
    remaining_budgets: Dict[int, int]
    round_states: List[RoundState] = field(default_factory=list)


class MultiRoundSimulator:
    """
    Simulador del proceso federado en T rondas con fallas estocásticas.
    """

    @staticmethod
    def _compute_round_budgets(
        total_budget: int,
        num_rounds: int,
        policy: str = "uniform",
        decay_factor: float = 0.85
    ) -> List[int]:
        """
        Calcula la secuencia de presupuestos [B_1, ..., B_T] según la política elegida.
        """
        if num_rounds <= 0:
            return []

        if policy == "uniform":
            base = total_budget // num_rounds
            rem = total_budget % num_rounds
            budgets = [base] * num_rounds
            for i in range(rem):
                budgets[i] += 1
            return budgets

        elif policy == "front_loaded":
            # Decaimiento geométrico: B_t proporcional a decay_factor^t
            weights = [decay_factor ** t for t in range(num_rounds)]
            sum_weights = sum(weights)
            raw_budgets = [int(total_budget * (w / sum_weights)) for w in weights]
            
            # Asegurar que la suma coincida exactamente con total_budget
            allocated = sum(raw_budgets)
            diff = total_budget - allocated
            for i in range(abs(diff)):
                idx = i % num_rounds
                if diff > 0:
                    raw_budgets[idx] += 1
                elif raw_budgets[idx] > 0:
                    raw_budgets[idx] -= 1
            return raw_budgets

        else:
            raise ValueError(f"Política desconocida: {policy}")

    @classmethod
    def run_simulation(
        cls,
        nodes: List[FederatedNode],
        total_rounds: int,
        k: int,
        total_budget: int,
        failure_prob: float = 0.1,
        policy: str = "uniform",
        seed: int = 42
    ) -> MultiRoundSimulationResult:
        """
        Ejecuta la simulación de T rondas bajo la política de gasto especificada.
        
        :param nodes: Lista de N nodos participantes.
        :param total_rounds: Número de rondas T.
        :param k: Cupo de selección por ronda.
        :param total_budget: Presupuesto total de ruido global B_total.
        :param failure_prob: Probabilidad q de que un nodo falle de forma independiente en una ronda.
        :param policy: 'uniform' o 'front_loaded'.
        :param seed: Semilla aleatoria para reproducibilidad.
        :return: MultiRoundSimulationResult.
        """
        rng = random.Random(seed)
        
        # Reiniciar presupuesto consumido de los nodos
        for node in nodes:
            node.reset_budget()

        round_budgets = cls._compute_round_budgets(total_budget, total_rounds, policy)

        cumulative_utility = 0.0
        cum_util_history: List[float] = []
        round_util_history: List[float] = []
        round_cov_history: List[int] = []
        round_states: List[RoundState] = []
        total_participations = 0

        for r in range(total_rounds):
            round_budget = round_budgets[r]
            failed_in_round: Set[int] = set()

            # 1. Simulación del modelo de fallas independientes Bernoulli(q)
            available_nodes: List[FederatedNode] = []
            for node in nodes:
                # El nodo falla si un sorteo uniforme es menor que failure_prob
                # o si ya no le queda presupuesto de ruido acumulado
                if rng.random() < failure_prob or node.remaining_noise_budget <= 0:
                    failed_in_round.add(node.node_id)
                else:
                    available_nodes.append(node)

            if not available_nodes or round_budget <= 0:
                # Ningún nodo disponible o presupuesto cero en esta ronda
                cum_util_history.append(cumulative_utility)
                round_util_history.append(0.0)
                round_cov_history.append(0)
                continue

            # 2. Selección voraz submodular de k nodos sobre los disponibles: O(N * k * tau)
            k_effective = min(k, len(available_nodes))
            selection_res = SubmodularGreedySelector.select_participants(available_nodes, k_effective)
            selected_ids = selection_res.selected_node_ids
            selected_node_objs = [n for n in available_nodes if n.node_id in selected_ids]

            # 3. Reparto óptimo del presupuesto de la ronda entre los seleccionados: O(k + B_t log k)
            allocation_res = GreedyBudgetAllocator.allocate(selected_node_objs, round_budget)

            # 4. Actualización de consumos de presupuesto y métricas
            for node in selected_node_objs:
                units = allocation_res.allocations.get(node.node_id, 0)
                node.consume_budget(units)

            # La utilidad de la ronda combina representatividad de datos y precisión del modelo
            r_utility = float(selection_res.total_coverage_utility) + allocation_res.total_utility
            cumulative_utility += r_utility

            total_participations += len(selected_ids)
            cum_util_history.append(cumulative_utility)
            round_util_history.append(r_utility)
            round_cov_history.append(selection_res.total_coverage_utility)

            round_states.append(RoundState(
                round_number=r + 1,
                selected_nodes=selected_ids,
                budget_allocations=allocation_res.allocations,
                round_coverage_utility=float(selection_res.total_coverage_utility),
                round_budget_utility=allocation_res.total_utility,
                failed_nodes=failed_in_round
            ))

        remaining_budgets = {n.node_id: n.remaining_noise_budget for n in nodes}

        return MultiRoundSimulationResult(
            policy_name=policy,
            total_rounds=total_rounds,
            cumulative_utility_per_round=cum_util_history,
            round_utilities=round_util_history,
            round_coverages=round_cov_history,
            total_active_participations=total_participations,
            remaining_budgets=remaining_budgets,
            round_states=round_states
        )

