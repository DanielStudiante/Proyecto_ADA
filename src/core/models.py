"""
Módulo de Modelos de Dominio (Domain Models)
Proyecto Semestral 2026-B - Subproyecto 2
Reparto de Presupuesto y Selección de Participantes (Proyecto Red)

Este archivo define las entidades y estructuras de datos fundamentales para representar
nodos federados, funciones de utilidad cóncavas discretas, grafos de red y configuraciones
del problema.
"""

from dataclasses import dataclass, field
from typing import List, Set, Dict, Optional, Callable
import math


class ConcaveUtilityFunction:
    """
    Representa una función de utilidad cóncava y monótona creciente discreta u_i(x).
    
    Por definición de concavidad discreta:
    u_i(x + 1) >= u_i(x) para todo x >= 0 (Monotonía creciente)
    u_i(x + 1) - u_i(x) >= u_i(x + 2) - u_i(x + 1) (Ganancia marginal decreciente)
    """

    def __init__(self, alpha: float = 10.0, beta: float = 1.0, func_type: str = "log"):
        """
        Inicializa la función de utilidad cóncava.
        
        :param alpha: Parámetro de escala de utilidad (> 0)
        :param beta: Parámetro de sensibilidad / curvatura (> 0)
        :param func_type: Tipo de función: 'log' para alpha * ln(1 + beta * x),
                          'sqrt' para alpha * sqrt(1 + beta * x) - alpha
        """
        if alpha <= 0 or beta <= 0:
            raise ValueError("Los parámetros alpha y beta deben ser estrictamente positivos.")
        self.alpha = alpha
        self.beta = beta
        self.func_type = func_type

    def evaluate(self, x: int) -> float:
        """Calcula el valor de utilidad u_i(x) para una asignación entera x >= 0."""
        if x < 0:
            raise ValueError(f"La asignación de presupuesto debe ser no negativa, recibido: {x}")
        if x == 0:
            return 0.0
        
        if self.func_type == "log":
            return self.alpha * math.log(1.0 + self.beta * x)
        elif self.func_type == "sqrt":
            return self.alpha * (math.sqrt(1.0 + self.beta * x) - 1.0)
        else:
            # Función cóncava genérica con decaimiento armónico de derivadas
            return self.alpha * math.log(1.0 + self.beta * x)

    def marginal_gain(self, current_x: int) -> float:
        """
        Calcula la ganancia marginal discreta de asignar la siguiente unidad:
        Delta u_i(current_x) = u_i(current_x + 1) - u_i(current_x).
        """
        return self.evaluate(current_x + 1) - self.evaluate(current_x)

    def __repr__(self) -> str:
        return f"ConcaveUtilityFunction({self.func_type}, alpha={self.alpha:.2f}, beta={self.beta:.2f})"


@dataclass
class FederatedNode:
    """
    Representa un nodo cliente participante en la red de Aprendizaje Federado.
    """
    node_id: int
    utility_func: ConcaveUtilityFunction
    coverage_mask: int  # Máscara de bits (bitset) que representa los datos/características cubiertos en U
    coverage_elements: Set[int] = field(default_factory=set)  # Conjunto explícito para verificación
    participation_cost: float = 1.0  # Costo de participación c_i (para Variante 1)
    failure_probability: float = 0.05  # Probabilidad de desconexión q_i (para Variante 2)
    noise_budget_total: int = 100  # Presupuesto total de ruido acumulado a lo largo de T rondas
    noise_budget_spent: int = 0  # Presupuesto de ruido consumido hasta el momento

    @property
    def remaining_noise_budget(self) -> int:
        """Presupuesto de ruido disponible que no ha sido consumido."""
        return max(0, self.noise_budget_total - self.noise_budget_spent)

    def consume_budget(self, units: int) -> None:
        """Registra el consumo de unidades de presupuesto de ruido en una ronda."""
        if units < 0:
            raise ValueError("No se puede consumir una cantidad negativa de presupuesto.")
        self.noise_budget_spent += units

    def reset_budget(self) -> None:
        """Reinicia el contador de presupuesto consumido."""
        self.noise_budget_spent = 0


class NetworkGraph:
    """
    Representa la topología de red G = (V, E) que interconecta los nodos participantes.
    Se utiliza fundamentalmente en la Variante 3 (Efectos de Red Aditivos y Competitivos).
    """

    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.adjacency: Dict[int, Set[int]] = {i: set() for i in range(num_nodes)}

    def add_edge(self, u: int, v: int) -> None:
        """Añade una arista no dirigida entre los nodos u y v."""
        if u != v and 0 <= u < self.num_nodes and 0 <= v < self.num_nodes:
            self.adjacency[u].add(v)
            self.adjacency[v].add(u)

    def neighbors(self, node_id: int) -> Set[int]:
        """Retorna el conjunto de vecinos inmediatos N(i) del nodo."""
        return self.adjacency.get(node_id, set())

    def degree(self, node_id: int) -> int:
        """Retorna el grado deg(i) del nodo en el grafo."""
        return len(self.adjacency.get(node_id, set()))

    @property
    def total_edges(self) -> int:
        """Retorna el número total de aristas en el grafo |E|."""
        return sum(len(neighbors) for neighbors in self.adjacency.values()) // 2


@dataclass
class RoundState:
    """
    Estado de una ronda individual de entrenamiento federado.
    """
    round_number: int
    selected_nodes: List[int] = field(default_factory=list)
    budget_allocations: Dict[int, int] = field(default_factory=dict)
    round_coverage_utility: float = 0.0
    round_budget_utility: float = 0.0
    failed_nodes: Set[int] = field(default_factory=set)

