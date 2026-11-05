"""
Módulo Generador de Instancias Sintéticas Reproducibles
Proyecto Semestral 2026-B - Subproyecto 2

Genera instancias controladas con semillas fijas para permitir la contrastación
experimental requerida en el proyecto (al menos 5 tamaños crecientes).
"""

import random
from typing import List, Tuple
from src.core.models import FederatedNode, ConcaveUtilityFunction, NetworkGraph


class SyntheticInstanceGenerator:
    """
    Genera instancias sintéticas del problema de Red Federada con parámetros controlados.
    """

    @staticmethod
    def generate_nodes(
        num_nodes: int,
        universe_size: int = 100,
        avg_elements_per_node: int = 15,
        min_cost: float = 1.0,
        max_cost: float = 10.0,
        default_noise_budget: int = 500,
        seed: int = 42
    ) -> List[FederatedNode]:
        """
        Genera una lista de N nodos con funciones de utilidad cóncavas y coberturas de datos.
        
        :param num_nodes: Cantidad N de nodos candidatos.
        :param universe_size: Tamaño |U| = m del universo total de datos/reglas.
        :param avg_elements_per_node: Cantidad esperada de elementos de U cubiertos por cada nodo.
        :param min_cost: Costo mínimo de participación c_i.
        :param max_cost: Costo máximo de participación c_i.
        :param default_noise_budget: Presupuesto total de ruido inicial por nodo.
        :param seed: Semilla para reproducibilidad estricta.
        :return: Lista de FederatedNode.
        """
        rng = random.Random(seed)
        nodes: List[FederatedNode] = []

        for i in range(num_nodes):
            # Parametrización de funciones de utilidad cóncavas heterogéneas
            alpha = rng.uniform(8.0, 20.0)
            beta = rng.uniform(0.5, 2.5)
            func_type = "log" if (i % 2 == 0) else "sqrt"
            utility_func = ConcaveUtilityFunction(alpha=alpha, beta=beta, func_type=func_type)

            # Generación de elementos cubiertos de U
            num_elements = max(1, min(universe_size, int(rng.gauss(avg_elements_per_node, avg_elements_per_node / 3))))
            sampled_elements = set(rng.sample(range(universe_size), num_elements))

            # Creación de la máscara de bits (bitset)
            mask = 0
            for elem in sampled_elements:
                mask |= (1 << elem)

            # Costo de participación heterogéneo (para Variante 1)
            cost = round(rng.uniform(min_cost, max_cost), 1)

            # Probabilidad de desconexión/falla (para Variante 2)
            fail_prob = rng.uniform(0.02, 0.15)

            node = FederatedNode(
                node_id=i,
                utility_func=utility_func,
                coverage_mask=mask,
                coverage_elements=sampled_elements,
                participation_cost=cost,
                failure_probability=fail_prob,
                noise_budget_total=default_noise_budget
            )
            nodes.append(node)

        return nodes

    @staticmethod
    def generate_graph(
        num_nodes: int,
        edge_probability: float = 0.1,
        graph_type: str = "erdos_renyi",
        seed: int = 42
    ) -> NetworkGraph:
        """
        Genera un grafo sintético de interconexión entre nodos.
        
        :param num_nodes: Cantidad N de nodos.
        :param edge_probability: Probabilidad de enlace p en modelo Erdos-Renyi.
        :param graph_type: Tipo de topología ('erdos_renyi' o 'ring').
        :param seed: Semilla aleatoria.
        :return: Instancia de NetworkGraph.
        """
        rng = random.Random(seed)
        graph = NetworkGraph(num_nodes)

        if graph_type == "ring":
            for i in range(num_nodes):
                graph.add_edge(i, (i + 1) % num_nodes)
        else:
            # Modelo Erdos-Renyi G(N, p)
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if rng.random() < edge_probability:
                        graph.add_edge(i, j)

        return graph

