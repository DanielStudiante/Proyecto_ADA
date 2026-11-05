"""
Módulo de Verificación de Optimalidad Exacta (Fuerza Bruta / DP)
Proyecto Semestral 2026-B - Subproyecto 2 (Parte 1)

Proporciona un solver exacto alternativo mediante Programación Dinámica
para contrastar y demostrar computacionalmente que el Algoritmo Voraz
alcanza exactamente el óptimo global en instancias pequeñas.
"""

from typing import List, Dict, Tuple
from src.core.models import FederatedNode


class DynamicProgrammingBudgetAllocator:
    """
    Resuelve el problema de reparto discreto mediante Programación Dinámica exacta.
    
    Estado: DP[i][b] = máxima utilidad repartiendo b unidades entre los primeros i nodos.
    Recurrencia: DP[i][b] = max_{0 <= x <= b} { DP[i-1][b - x] + u_i(x) }
    Complejidad: O(N * B^2)
    """

    @staticmethod
    def allocate(
        nodes: List[FederatedNode],
        total_budget: int
    ) -> Tuple[Dict[int, int], float]:
        """
        Calcula la asignación óptima global mediante programación dinámica.
        
        :param nodes: Lista de nodos participantes.
        :param total_budget: Presupuesto total discreto B.
        :return: (diccionario de asignaciones {node_id: x_i}, utilidad_óptima)
        """
        num_nodes = len(nodes)
        if num_nodes == 0 or total_budget == 0:
            return {n.node_id: 0 for n in nodes}, 0.0

        # Tabla DP: (num_nodes + 1) x (total_budget + 1)
        dp = [[0.0] * (total_budget + 1) for _ in range(num_nodes + 1)]
        # Tabla para reconstruir las decisiones: choice[i][b] = x_i
        choice = [[0] * (total_budget + 1) for _ in range(num_nodes + 1)]

        for i in range(1, num_nodes + 1):
            node = nodes[i - 1]
            for b in range(total_budget + 1):
                best_val = -1.0
                best_x = 0
                for x in range(b + 1):
                    val = dp[i - 1][b - x] + node.utility_func.evaluate(x)
                    if val > best_val:
                        best_val = val
                        best_x = x
                dp[i][b] = best_val
                choice[i][b] = best_x

        # Reconstrucción de la asignación óptima hacia atrás
        allocations: Dict[int, int] = {}
        curr_b = total_budget
        for i in range(num_nodes, 0, -1):
            node = nodes[i - 1]
            x_assigned = choice[i][curr_b]
            allocations[node.node_id] = x_assigned
            curr_b -= x_assigned

        return allocations, dp[num_nodes][total_budget]

