"""
Módulo de Reparto Óptimo de Presupuesto - Algoritmo Voraz Exacto
Proyecto Semestral 2026-B - Subproyecto 2 (Parte 1)

Implementa el algoritmo voraz óptimo basado en cola de prioridad (Max-Heap)
para funciones de utilidad cóncavas y monótonas crecientes.

Complejidad Temporal Teórica:
T(N, B) = O(N + B * log N)
- Construcción inicial del heap (heapify): O(N)
- B asignaciones de presupuesto: B * O(log N) = O(B log N)
"""

import heapq
from typing import List, Dict, Tuple
from dataclasses import dataclass
from src.core.models import FederatedNode, ConcaveUtilityFunction


@dataclass
class AllocationResult:
    """Resultado del reparto de presupuesto."""
    allocations: Dict[int, int]  # Mapeo node_id -> unidades de presupuesto asignadas
    total_utility: float         # Utilidad agregada total sum u_i(x_i)
    heap_operations_count: int   # Contador de operaciones elementales en el heap
    marginal_gains_history: List[float]  # Historial de ganancias marginales asignadas paso a paso


class GreedyBudgetAllocator:
    """
    Algoritmo voraz óptimo para maximizar sum_{i=1}^N u_i(x_i) sujeto a sum x_i <= B, x_i in N_0.
    """

    @staticmethod
    def allocate(
        nodes: List[FederatedNode],
        total_budget: int
    ) -> AllocationResult:
        """
        Ejecuta el reparto óptimo de las B unidades de presupuesto entre los N nodos.
        
        :param nodes: Lista de nodos participantes (N = len(nodes)).
        :param total_budget: Presupuesto total discreto B (unidades enteras >= 0).
        :return: AllocationResult con las asignaciones y métricas de complejidad.
        """
        if total_budget < 0:
            raise ValueError(f"El presupuesto debe ser no negativo, recibido: {total_budget}")
        
        num_nodes = len(nodes)
        if num_nodes == 0 or total_budget == 0:
            return AllocationResult(
                allocations={node.node_id: 0 for node in nodes},
                total_utility=0.0,
                heap_operations_count=0,
                marginal_gains_history=[]
            )

        # Vector de asignaciones iniciales x_i = 0
        allocations: Dict[int, int] = {node.node_id: 0 for node in nodes}
        heap_operations = 0

        # Construcción inicial de la cola de prioridad (Max-Heap)
        # Python heapq es un Min-Heap por defecto; invertimos el signo de delta para simular Max-Heap
        heap: List[Tuple[float, int, FederatedNode]] = []
        for node in nodes:
            delta = node.utility_func.marginal_gain(0)
            # Entrada: (-ganancia_marginal, node_id, objeto_nodo)
            heap.append((-delta, node.node_id, node))

        # build_heap (heapify lineal): O(N) operaciones
        heapq.heapify(heap)
        heap_operations += num_nodes

        gains_history: List[float] = []

        # Bucle de asignación voraz: se asignan exactamente total_budget unidades
        for _ in range(total_budget):
            # Extraer el nodo con mayor ganancia marginal disponible: O(log N)
            neg_delta, node_id, node = heapq.heappop(heap)
            heap_operations += 1

            best_delta = -neg_delta
            gains_history.append(best_delta)

            # Asignar la unidad de presupuesto al nodo
            allocations[node_id] += 1
            curr_x = allocations[node_id]

            # Calcular la nueva ganancia marginal para la siguiente unidad potencial
            next_delta = node.utility_func.marginal_gain(curr_x)

            # Reinsertar en el heap con la ganancia actualizada: O(log N)
            heapq.heappush(heap, (-next_delta, node_id, node))
            heap_operations += 1

        # Calcular la utilidad total final obtenida
        total_utility = sum(
            node.utility_func.evaluate(allocations[node.node_id])
            for node in nodes
        )

        return AllocationResult(
            allocations=allocations,
            total_utility=total_utility,
            heap_operations_count=heap_operations,
            marginal_gains_history=gains_history
        )

