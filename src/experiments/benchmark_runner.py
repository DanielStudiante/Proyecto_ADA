"""
Módulo de Benchmarking y Validación Experimental
Proyecto Semestral 2026-B - Subproyecto 2

Ejecuta mediciones reproducibles de tiempo real de ejecución en al menos 5 tamaños
crecientes de n (N y B para Parte 1; N y k para Parte 2), midiendo con time.perf_counter
sobre múltiples repeticiones, y contrasta los resultados contra las funciones teóricas T(n).
"""

import time
import math
from typing import List, Dict, Tuple, Any
from src.core.models import FederatedNode
from src.core.data_generator import SyntheticInstanceGenerator
from src.parte1_reparto.greedy_budget import GreedyBudgetAllocator
from src.parte1_reparto.brute_force_budget import DynamicProgrammingBudgetAllocator
from src.parte2_seleccion.submodular_greedy import SubmodularGreedySelector
from src.parte2_seleccion.brute_force_selection import BruteForceSelector
from src.variantes.v1_costos_distintos.khuller_greedy import KhullerBudgetedSelector
from src.variantes.v2_multi_ronda_fallas.multi_round_sim import MultiRoundSimulator
from src.variantes.v3_nodos_relacionados.network_effects import NetworkEffectsModeler


class BenchmarkRunner:
    """
    Motor de pruebas experimentales y verificación de cotas asintóticas.
    """

    @staticmethod
    def benchmark_parte1_reparto(
        n_sizes: List[int] = None,
        b_multiplier: int = 5,
        repetitions: int = 5,
        seed: int = 42
    ) -> Dict[str, Any]:
        """
        Ejecuta benchmarks de la Parte 1 para valores crecientes de N y B.
        Verifica que el tiempo empírico sigue la función teórica T(N, B) = O(N + B * log N).
        """
        if n_sizes is None:
            n_sizes = [50, 100, 200, 400, 800, 1600]

        results = {
            "n_values": [],
            "b_values": [],
            "theoretical_terms": [],  # N + B * log2(N)
            "mean_times_seconds": [],
            "std_times_seconds": [],
            "operations_counts": []
        }

        for n in n_sizes:
            b = n * b_multiplier
            nodes = SyntheticInstanceGenerator.generate_nodes(num_nodes=n, seed=seed)

            times = []
            ops = 0
            for rep in range(repetitions):
                t_start = time.perf_counter()
                alloc_res = GreedyBudgetAllocator.allocate(nodes, b)
                t_end = time.perf_counter()
                times.append(t_end - t_start)
                ops = alloc_res.heap_operations_count

            mean_t = sum(times) / len(times)
            variance = sum((t - mean_t) ** 2 for t in times) / len(times)
            std_t = math.sqrt(variance)

            theor_term = n + b * math.log2(max(2, n))

            results["n_values"].append(n)
            results["b_values"].append(b)
            results["theoretical_terms"].append(theor_term)
            results["mean_times_seconds"].append(mean_t)
            results["std_times_seconds"].append(std_t)
            results["operations_counts"].append(ops)

        return results

    @staticmethod
    def benchmark_parte2_seleccion(
        n_sizes: List[int] = None,
        k_ratio: float = 0.1,
        universe_size: int = 150,
        repetitions: int = 5,
        seed: int = 42
    ) -> Dict[str, Any]:
        """
        Ejecuta benchmarks de la Parte 2 para valores crecientes de N y k.
        Verifica que el tiempo empírico sigue la función teórica T(N, k) = O(N * k).
        """
        if n_sizes is None:
            n_sizes = [50, 100, 200, 400, 800, 1600]

        results = {
            "n_values": [],
            "k_values": [],
            "theoretical_terms": [],  # N * k
            "mean_times_seconds": [],
            "std_times_seconds": [],
            "evaluations_counts": []
        }

        for n in n_sizes:
            k = max(2, int(n * k_ratio))
            nodes = SyntheticInstanceGenerator.generate_nodes(
                num_nodes=n,
                universe_size=universe_size,
                seed=seed
            )

            times = []
            evals = 0
            for rep in range(repetitions):
                t_start = time.perf_counter()
                sel_res = SubmodularGreedySelector.select_participants(nodes, k)
                t_end = time.perf_counter()
                times.append(t_end - t_start)
                evals = sel_res.evaluations_count

            mean_t = sum(times) / len(times)
            variance = sum((t - mean_t) ** 2 for t in times) / len(times)
            std_t = math.sqrt(variance)

            theor_term = n * k

            results["n_values"].append(n)
            results["k_values"].append(k)
            results["theoretical_terms"].append(theor_term)
            results["mean_times_seconds"].append(mean_t)
            results["std_times_seconds"].append(std_t)
            results["evaluations_counts"].append(evals)

        return results

    @staticmethod
    def verify_optimality_parte1(num_nodes: int = 6, budget: int = 20, seed: int = 42) -> Dict[str, Any]:
        """
        Contrasta el Algoritmo Voraz contra Programación Dinámica exacta en Parte 1.
        """
        nodes = SyntheticInstanceGenerator.generate_nodes(num_nodes=num_nodes, seed=seed)
        
        # Algoritmo Voraz
        greedy_res = GreedyBudgetAllocator.allocate(nodes, budget)
        
        # Programación Dinámica
        dp_alloc, dp_util = DynamicProgrammingBudgetAllocator.allocate(nodes, budget)

        abs_diff = abs(greedy_res.total_utility - dp_util)
        is_exact = abs_diff < 1e-6

        return {
            "num_nodes": num_nodes,
            "budget": budget,
            "greedy_utility": greedy_res.total_utility,
            "dp_utility": dp_util,
            "absolute_difference": abs_diff,
            "is_exact_optimal": is_exact,
            "greedy_allocations": greedy_res.allocations,
            "dp_allocations": dp_alloc
        }

    @staticmethod
    def verify_submodular_ratio_parte2(
        num_instances: int = 8,
        n: int = 14,
        k: int = 4,
        universe_size: int = 30,
        base_seed: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Calcula el ratio empírico f(A_voraz) / f(A*) contrastándolo contra la cota
        teórica (1 - 1/e) aprox 0.63212 en múltiples instancias sintéticas.
        """
        verification_records = []
        nemhauser_bound = 1.0 - (1.0 / math.e)  # aprox 0.6321205588

        for idx in range(num_instances):
            current_seed = base_seed + idx * 7
            nodes = SyntheticInstanceGenerator.generate_nodes(
                num_nodes=n,
                universe_size=universe_size,
                avg_elements_per_node=6,
                seed=current_seed
            )

            # Solución Voraz
            voraz_res = SubmodularGreedySelector.select_participants(nodes, k)
            f_voraz = voraz_res.total_coverage_utility

            # Solución Óptima por Fuerza Bruta C(N, k)
            _, f_opt, total_combos = BruteForceSelector.find_optimal(nodes, k)

            ratio = (f_voraz / f_opt) if f_opt > 0 else 1.0
            satisfies_bound = (ratio >= nemhauser_bound - 1e-9)

            verification_records.append({
                "instance_id": idx + 1,
                "n": n,
                "k": k,
                "combinations_evaluated": total_combos,
                "f_greedy": f_voraz,
                "f_optimal": f_opt,
                "empirical_ratio": ratio,
                "nemhauser_bound": nemhauser_bound,
                "satisfies_bound": satisfies_bound
            })

        return verification_records

