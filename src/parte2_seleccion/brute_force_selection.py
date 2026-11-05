"""
Módulo de Verificación Combinatoria Exacta (Fuerza Bruta)
Proyecto Semestral 2026-B - Subproyecto 2 (Parte 2)

Calcula el óptimo global mediante la evaluación exhaustiva de los C(N, k)
subconjuntos posibles para instancias pequeñas, verificando rigurosamente
que la solución voraz respeta la cota teórica (1 - 1/e) aprox 63.2%.
"""

import itertools
from typing import List, Tuple
from src.core.models import FederatedNode


class BruteForceSelector:
    """
    Evaluador por fuerza bruta exhaustiva para selección submodular.
    """

    @staticmethod
    def find_optimal(
        candidates: List[FederatedNode],
        k: int
    ) -> Tuple[List[int], int, int]:
        """
        Encuentra el subconjunto óptimo de tamaño k explorando todas las combinaciones C(N, k).
        
        :param candidates: Lista de N nodos disponibles.
        :param k: Cupo a seleccionar.
        :return: (lista_ids_óptimos, utilidad_óptima, total_combinaciones_evaluadas)
        """
        n = len(candidates)
        if k <= 0 or n == 0:
            return [], 0, 0

        k = min(k, n)
        best_utility = -1
        best_combination: Tuple[FederatedNode, ...] = ()
        combinations_count = 0

        for combo in itertools.combinations(candidates, k):
            combinations_count += 1
            combined_mask = 0
            for node in combo:
                combined_mask |= node.coverage_mask
            
            utility = combined_mask.bit_count()
            if utility > best_utility:
                best_utility = utility
                best_combination = combo

        optimal_ids = [node.node_id for node in best_combination]
        return optimal_ids, best_utility, combinations_count

