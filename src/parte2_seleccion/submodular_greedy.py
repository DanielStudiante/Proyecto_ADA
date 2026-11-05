"""
Módulo de Selección de Participantes - Algoritmo Voraz Submodular
Proyecto Semestral 2026-B - Subproyecto 2 (Parte 2)

Implementa el algoritmo voraz para maximización submodular con restricción de cardinalidad k.
Garantía Teórica: f(A_k) >= (1 - 1/e) * f(A*) aprox 63.2% de la utilidad óptima (Nemhauser et al., 1978).

Complejidad Temporal Teórica:
T(N, k, tau) = O(N * k * tau)
donde tau es el costo de evaluación de la ganancia marginal. Con representación
en vector de bits (bitset de enteros nativos), tau = O(ceil(m / 64)).
"""

from typing import List, Set, Tuple
from dataclasses import dataclass
from src.core.models import FederatedNode


@dataclass
class SelectionResult:
    """Resultado de la selección voraz submodular."""
    selected_node_ids: List[int]       # IDs de los k nodos seleccionados en orden de elección
    total_coverage_utility: int        # Cardinalidad de la unión |bigcup_{i in A} S_i|
    marginal_gains: List[int]          # Ganancia marginal aportada en cada uno de los k pasos
    evaluations_count: int             # Número total de evaluaciones de la función submodular


class SubmodularGreedySelector:
    """
    Selector voraz submodular para el problema de cobertura de datos en Aprendizaje Federado.
    """

    @staticmethod
    def select_participants(
        candidates: List[FederatedNode],
        k: int
    ) -> SelectionResult:
        """
        Selecciona un subconjunto de tamaño k de nodos candidatos para maximizar la cobertura conjunta.
        
        :param candidates: Lista de N nodos disponibles.
        :param k: Cupo máximo de nodos a seleccionar (1 <= k <= N).
        :return: SelectionResult con los nodos seleccionados y estadísticas.
        """
        num_candidates = len(candidates)
        if k <= 0 or num_candidates == 0:
            return SelectionResult(
                selected_node_ids=[],
                total_coverage_utility=0,
                marginal_gains=[],
                evaluations_count=0
            )

        k = min(k, num_candidates)
        selected_nodes: List[int] = []
        selected_indices_set: Set[int] = set()
        current_combined_mask: int = 0
        current_utility: int = 0

        marginal_gains_list: List[int] = []
        total_evaluations: int = 0

        # Mapeo de índice a nodo para acceso rápido
        nodes_list = list(candidates)

        for step in range(k):
            best_gain = -1
            best_candidate_idx = -1
            best_new_mask = current_combined_mask

            for idx in range(num_candidates):
                if idx in selected_indices_set:
                    continue

                node = nodes_list[idx]
                candidate_mask = node.coverage_mask

                # Unión lógica a nivel de bits: O(1) operaciones máquina
                union_mask = current_combined_mask | candidate_mask
                # int.bit_count() calcula el número de bits en 1 en tiempo de instrucción POPCNT O(1)
                new_utility = union_mask.bit_count()
                marginal_gain = new_utility - current_utility

                total_evaluations += 1

                if marginal_gain > best_gain:
                    best_gain = marginal_gain
                    best_candidate_idx = idx
                    best_new_mask = union_mask

            if best_candidate_idx == -1:
                # No quedan candidatos que aporten ganancia
                break

            # Confirmar la selección del mejor candidato
            selected_indices_set.add(best_candidate_idx)
            chosen_node = nodes_list[best_candidate_idx]
            selected_nodes.append(chosen_node.node_id)
            current_combined_mask = best_new_mask
            current_utility = current_combined_mask.bit_count()
            marginal_gains_list.append(best_gain)

        return SelectionResult(
            selected_node_ids=selected_nodes,
            total_coverage_utility=current_utility,
            marginal_gains=marginal_gains_list,
            evaluations_count=total_evaluations
        )

