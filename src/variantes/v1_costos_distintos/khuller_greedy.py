"""
Variante 1: Nodos con Costos de Participación Heterogéneos
Proyecto Semestral 2026-B - Subproyecto 2

Implementa el algoritmo de Khuller, Moss y Naor (1999) para Cobertura Máxima con Presupuesto
(Budgeted Maximum Coverage / Submodular Maximization under Knapsack Constraint).

Garantía Teórica Demostrable:
f(A_final) >= 0.5 * (1 - 1/e) * f(A*) aprox 31.6% de la utilidad óptima.

Complejidad Temporal:
T(N, L, tau) = O(N^2 * tau)
"""

from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from src.core.models import FederatedNode


@dataclass
class BudgetedSelectionResult:
    """Resultado de la selección con costos heterogéneos."""
    selected_node_ids: List[int]
    total_utility: int
    total_cost_spent: float
    budget_limit: float
    chosen_strategy: str  # 'density_greedy' o 'best_singleton'
    evaluations_count: int


class KhullerBudgetedSelector:
    """
    Selector con garantía para maximización submodular sujeta a presupuesto de costo L.
    """

    @staticmethod
    def select(
        candidates: List[FederatedNode],
        cost_budget: float
    ) -> BudgetedSelectionResult:
        """
        Ejecuta el algoritmo de Khuller et al. (1999) seleccionando el mejor entre:
        1. Voraz por densidad (ganancia_marginal / costo).
        2. Mejor singleton factible individual.
        
        :param candidates: Lista de N nodos disponibles con atributos .participation_cost.
        :param cost_budget: Presupuesto total de costo L.
        :return: BudgetedSelectionResult.
        """
        if cost_budget <= 0 or not candidates:
            return BudgetedSelectionResult([], 0, 0.0, cost_budget, "none", 0)

        nodes = list(candidates)
        n = len(nodes)
        total_evals = 0

        # -------------------------------------------------------------
        # Paso 1: Algoritmo Voraz por Densidad Costo-Beneficio
        # -------------------------------------------------------------
        selected_ratio_indices: Set[int] = set()
        current_ratio_mask = 0
        current_ratio_utility = 0
        remaining_budget = cost_budget
        spent_budget_ratio = 0.0

        while True:
            best_density = -1.0
            best_idx = -1
            best_new_mask = current_ratio_mask
            best_gain = 0

            for i in range(n):
                if i in selected_ratio_indices:
                    continue

                node = nodes[i]
                cost = node.participation_cost

                # Solo considerar si el costo no excede el presupuesto residual
                if cost <= remaining_budget:
                    union_mask = current_ratio_mask | node.coverage_mask
                    new_utility = union_mask.bit_count()
                    gain = new_utility - current_ratio_utility
                    total_evals += 1

                    density = gain / cost
                    if density > best_density:
                        best_density = density
                        best_idx = i
                        best_new_mask = union_mask
                        best_gain = gain

            if best_idx == -1 or best_density <= 0:
                break

            # Agregar el mejor elemento por densidad
            selected_ratio_indices.add(best_idx)
            current_ratio_mask = best_new_mask
            current_ratio_utility = current_ratio_mask.bit_count()
            chosen_cost = nodes[best_idx].participation_cost
            remaining_budget -= chosen_cost
            spent_budget_ratio += chosen_cost

        ratio_solution_ids = [nodes[i].node_id for i in selected_ratio_indices]
        ratio_solution_val = current_ratio_utility

        # -------------------------------------------------------------
        # Paso 2: Mejor Nodo Individual Factible (Singleton)
        # -------------------------------------------------------------
        best_single_val = -1
        best_single_node: FederatedNode = None

        for node in nodes:
            total_evals += 1
            if node.participation_cost <= cost_budget:
                single_utility = node.coverage_mask.bit_count()
                if single_utility > best_single_val:
                    best_single_val = single_utility
                    best_single_node = node

        # -------------------------------------------------------------
        # Paso 3: Retornar el máximo entre ambas soluciones
        # -------------------------------------------------------------
        if best_single_node is not None and best_single_val > ratio_solution_val:
            return BudgetedSelectionResult(
                selected_node_ids=[best_single_node.node_id],
                total_utility=best_single_val,
                total_cost_spent=best_single_node.participation_cost,
                budget_limit=cost_budget,
                chosen_strategy="best_singleton",
                evaluations_count=total_evals
            )
        else:
            return BudgetedSelectionResult(
                selected_node_ids=ratio_solution_ids,
                total_utility=ratio_solution_val,
                total_cost_spent=spent_budget_ratio,
                budget_limit=cost_budget,
                chosen_strategy="density_greedy",
                evaluations_count=total_evals
            )

