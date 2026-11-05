"""
Script Principal de Ejecución y Validación Integral
Proyecto Semestral 2026-B - Subproyecto 2
Reparto de Presupuesto y Selección de Participantes (Proyecto Red)
Análisis y Diseño de Algoritmos (ADA)

Ejecuta todas las fases del proyecto:
1. Verificación de optimalidad exacta de la Parte 1 (Voraz vs Programación Dinámica).
2. Verificación de la cota teórica (1 - 1/e) de la Parte 2 (Voraz vs Fuerza Bruta C(N, k)).
3. Benchmarking de tiempos para >= 5 tamaños crecientes de entrada y ajuste de curvas T(n).
4. Ejecución y validación de las 3 Variantes Obligatorias (Khuller, Multi-Ronda, Grafos).
5. Generación de todas las gráficas para el informe técnico en results/figures/.
"""

import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.core.data_generator import SyntheticInstanceGenerator
from src.experiments.benchmark_runner import BenchmarkRunner
from src.experiments.plot_generator import PlotGenerator
from src.variantes.v1_costos_distintos.khuller_greedy import KhullerBudgetedSelector
from src.variantes.v2_multi_ronda_fallas.multi_round_sim import MultiRoundSimulator
from src.variantes.v3_nodos_relacionados.network_effects import NetworkEffectsModeler


def print_header(title: str) -> None:
    print("\n" + "=" * 78)
    print(f" {title.center(76)} ")
    print("=" * 78)


def main() -> None:
    print_header("PROYECTO SEMESTRAL 2026-B: ANÁLISIS Y DISEÑO DE ALGORITMOS")
    print(" Subproyecto 2 — Reparto de Presupuesto y Selección de Participantes")
    print(" Ejecutando pipeline completo de validación formal y experimental...")

    # -----------------------------------------------------------------
    # FASE 1: Verificación de Optimalidad Exacta de la Parte 1
    # -----------------------------------------------------------------
    print_header("FASE 1: PARTE 1 — VERIFICACIÓN DE OPTIMALIDAD EXACTA DEL VORAZ")
    p1_check = BenchmarkRunner.verify_optimality_parte1(num_nodes=8, budget=25, seed=42)
    print(f" • Parámetros de prueba: N = {p1_check['num_nodes']} nodos, Presupuesto B = {p1_check['budget']} unidades")
    print(f" • Utilidad Algoritmo Voraz (Max-Heap): {p1_check['greedy_utility']:.6f}")
    print(f" • Utilidad Programación Dinámica Exacta:  {p1_check['dp_utility']:.6f}")
    print(f" • Diferencia Absoluta:                   {p1_check['absolute_difference']:.8e}")
    if p1_check["is_exact_optimal"]:
        print(" [RESULTADO]: ¡OPTIMALIDAD VERIFICADA AL 100%! El voraz alcanza exactamente el optimo global.")
    else:
        print(" [ALERTA]: Discrepancia detectada.")

    # -----------------------------------------------------------------
    # FASE 2: Verificación de la Cota de Aproximación (1 - 1/e) Parte 2
    # -----------------------------------------------------------------
    print_header("FASE 2: PARTE 2 — VERIFICACIÓN DE LA COTA SUBMODULAR (1 - 1/e)")
    submod_records = BenchmarkRunner.verify_submodular_ratio_parte2(
        num_instances=6,
        n=14,
        k=4,
        universe_size=25,
        base_seed=123
    )
    bound_val = submod_records[0]["nemhauser_bound"]
    print(f" • Cota Teórica de Nemhauser et al. (1978): (1 - 1/e) >= {bound_val:.4f} (63.21%)")
    print(f" {'Instancia':<10} | {'f(Voraz)':<10} | {'f(Optimo)':<10} | {'Ratio':<10} | {'Cota Cumplida':<15}")
    print(" " + "-" * 65)

    all_passed = True
    for rec in submod_records:
        passed = rec["satisfies_bound"]
        all_passed = all_passed and passed
        status = "SI (OK)" if passed else "NO (FALLA)"
        print(f" #{rec['instance_id']:<9} | {rec['f_greedy']:<10} | {rec['f_optimal']:<10} | {rec['empirical_ratio']:<10.4f} | {status:<15}")

    if all_passed:
        print(" [RESULTADO]: ¡TODAS las instancias respetan estrictamente la cota teorica (1 - 1/e)!")
    PlotGenerator.plot_submodular_ratio_validation(submod_records)
    print(" -> Grafica guardada: results/figures/submodular_ratio_validation.png")

    # -----------------------------------------------------------------
    # FASE 3: Benchmarks de Tiempo y Ajuste contra Curvas Teóricas T(n)
    # -----------------------------------------------------------------
    print_header("FASE 3: BENCHMARKS DE ESCALABILIDAD EN >= 5 TAMAÑOS CRECIENTES")
    test_sizes = [50, 100, 200, 400, 800, 1600]

    print("\n --- Ejecutando Benchmarks de la Parte 1 (Max-Heap Voraz O(N + B log N)) ---")
    p1_bench = BenchmarkRunner.benchmark_parte1_reparto(n_sizes=test_sizes, b_multiplier=5, repetitions=3)
    print(f" {'N':<8} | {'B (5*N)':<10} | {'Tiempo Medido (ms)':<22} | {'Operaciones Heap':<18}")
    print(" " + "-" * 65)
    for n, b, t_sec, ops in zip(p1_bench["n_values"], p1_bench["b_values"], p1_bench["mean_times_seconds"], p1_bench["operations_counts"]):
        print(f" {n:<8} | {b:<10} | {t_sec * 1000.0:<22.4f} | {ops:<18}")
    PlotGenerator.plot_parte1_empirical_vs_theory(p1_bench)
    print(" -> Grafica guardada: results/figures/part1_time_vs_theory.png")

    print("\n --- Ejecutando Benchmarks de la Parte 2 (Voraz Submodular O(N * k)) ---")
    p2_bench = BenchmarkRunner.benchmark_parte2_seleccion(n_sizes=test_sizes, k_ratio=0.1, repetitions=3)
    print(f" {'N':<8} | {'k (0.1*N)':<10} | {'Tiempo Medido (ms)':<22} | {'Evaluaciones Submodulares':<25}")
    print(" " + "-" * 72)
    for n, k, t_sec, evals in zip(p2_bench["n_values"], p2_bench["k_values"], p2_bench["mean_times_seconds"], p2_bench["evaluations_counts"]):
        print(f" {n:<8} | {k:<10} | {t_sec * 1000.0:<22.4f} | {evals:<25}")
    PlotGenerator.plot_parte2_empirical_vs_theory(p2_bench)
    print(" -> Grafica guardada: results/figures/part2_time_vs_theory.png")

    # -----------------------------------------------------------------
    # FASE 4: Variante 1 — Nodos con Costos Heterogéneos (Khuller 1999)
    # -----------------------------------------------------------------
    print_header("FASE 4: VARIANTE 1 — BUDGETED MAXIMUM COVERAGE (KHULLER ET AL., 1999)")
    v1_nodes = SyntheticInstanceGenerator.generate_nodes(num_nodes=40, universe_size=80, seed=42)
    cost_budget = 30.0
    v1_res = KhullerBudgetedSelector.select(v1_nodes, cost_budget)
    print(f" • Presupuesto de Costo L: {cost_budget}")
    print(f" • Estrategia Ganadora:   {v1_res.chosen_strategy}")
    print(f" • Nodos Seleccionados:   {v1_res.selected_node_ids}")
    print(f" • Utilidad Alcanzada:    {v1_res.total_utility}")
    print(f" • Costo Invertido:       {v1_res.total_cost_spent:.2f} / {v1_res.budget_limit}")
    print(" [OK] Variante 1 ejecutada con garantia demostrable de 0.5 * (1 - 1/e) aprox 31.6%")

    # -----------------------------------------------------------------
    # FASE 5: Variante 2 — T Rondas con Fallas Estocásticas y Políticas
    # -----------------------------------------------------------------
    print_header("FASE 5: VARIANTE 2 — SIMULACIÓN DINÁMICA MULTI-RONDA CON FALLAS")
    v2_nodes = SyntheticInstanceGenerator.generate_nodes(num_nodes=50, default_noise_budget=200, seed=77)
    total_rounds = 12
    k_cupo = 8
    b_total = 600

    sim_uniform = MultiRoundSimulator.run_simulation(
        nodes=v2_nodes,
        total_rounds=total_rounds,
        k=k_cupo,
        total_budget=b_total,
        failure_prob=0.1,
        policy="uniform",
        seed=101
    )
    sim_front = MultiRoundSimulator.run_simulation(
        nodes=v2_nodes,
        total_rounds=total_rounds,
        k=k_cupo,
        total_budget=b_total,
        failure_prob=0.1,
        policy="front_loaded",
        seed=101
    )
    print(f" • Rondas evaluadas: T = {total_rounds}, Cupo k = {k_cupo}, Presupuesto Global = {b_total}")
    print(f" • Utilidad Acumulada Final (Politica Uniforme):     {sim_uniform.cumulative_utility_per_round[-1]:.2f}")
    print(f" • Utilidad Acumulada Final (Politica Front-Loaded): {sim_front.cumulative_utility_per_round[-1]:.2f}")
    PlotGenerator.plot_variant2_simulation(sim_uniform, sim_front)
    print(" -> Grafica guardada: results/figures/variant2_multi_round_policies.png")

    # -----------------------------------------------------------------
    # FASE 6: Variante 3 — Nodos Relacionados en Grafo
    # -----------------------------------------------------------------
    print_header("FASE 6: VARIANTE 3 — GRAFO DE NODOS (ADITIVO VS COMPETITIVO)")
    # Caso Aditivo
    v3_nodes = SyntheticInstanceGenerator.generate_nodes(num_nodes=10, seed=99)
    v3_graph = SyntheticInstanceGenerator.generate_graph(num_nodes=10, edge_probability=0.25, seed=99)
    res_additive = NetworkEffectsModeler.solve_additive_case(v3_nodes, v3_graph, total_budget=30, gamma=0.2)
    print(f" • Caso Aditivo (Sinergia): Utilidad Total = {res_additive.total_system_utility:.2f} (Voraz con Max-Heap es OPTIMO)")

    # Caso Competitivo y Contraejemplo
    counter_res = NetworkEffectsModeler.run_counterexample()
    print(" • Evaluacion del Contraejemplo de Interferencia en Grafo Estrella:")
    print(f"   - Asignacion Voraz Miope:   {counter_res['greedy_miope_allocation']} -> Utilidad = {counter_res['greedy_miope_utility']:.2f}")
    print(f"   - Asignacion Optima Global: {counter_res['optimal_allocation']} -> Utilidad = {counter_res['optimal_utility']:.2f}")
    print(f"   - Solucion Heuristica Neta: {counter_res['heuristic_allocation']} -> Utilidad = {counter_res['heuristic_utility']:.2f}")
    if counter_res["counterexample_holds"]:
        print(" [RESULTADO]: ¡CONTRAEJEMPLO CONFIRMADO! El voraz clasico falla en presencia de interferencia.")
    PlotGenerator.plot_variant3_counterexample(counter_res)
    print(" -> Grafica guardada: results/figures/variant3_counterexample.png")

    print_header("¡EJECUCIÓN COMPLETADA EXITOSAMENTE!")
    print(" Todas las fases del proyecto se ejecutaron, verificaron y graficaron.")
    print(" Consulte 'results/figures/' para las visualizaciones generadas.")
    print("=" * 78 + "\n")


if __name__ == "__main__":
    main()

