"""
Módulo Generador de Gráficas Experimentales
Proyecto Semestral 2026-B - Subproyecto 2

Genera figuras gráficas profesionales de alta resolución en formato PNG,
contrastando los tiempos reales medidos contra las curvas teóricas T(n) deducidas.
"""

import os
from typing import Dict, List, Any
import numpy as np
import matplotlib.pyplot as plt


class PlotGenerator:
    """
    Genera y almacena las gráficas experimentales para el informe técnico.
    """

    @staticmethod
    def _ensure_dir(output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)

    @classmethod
    def plot_parte1_empirical_vs_theory(
        cls,
        benchmark_data: Dict[str, Any],
        output_path: str = "results/figures/part1_time_vs_theory.png"
    ) -> str:
        """
        Grafica el tiempo medido en Parte 1 vs la curva teórica c * (N + B * log N).
        """
        cls._ensure_dir(os.path.dirname(output_path))

        n_vals = np.array(benchmark_data["n_values"])
        b_vals = np.array(benchmark_data["b_values"])
        times = np.array(benchmark_data["mean_times_seconds"])
        std_devs = np.array(benchmark_data["std_times_seconds"])
        theor_terms = np.array(benchmark_data["theoretical_terms"])

        # Ajuste de regresión lineal simple a través del origen: y = c * x
        # c = sum(x * y) / sum(x^2)
        c_fit = np.sum(theor_terms * times) / np.sum(theor_terms ** 2)
        fitted_curve = c_fit * theor_terms

        # Coeficiente de determinación R^2
        ss_res = np.sum((times - fitted_curve) ** 2)
        ss_tot = np.sum((times - np.mean(times)) ** 2)
        r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0

        plt.figure(figsize=(9, 5.5), dpi=200)
        
        # Puntos experimentales con barras de error
        plt.errorbar(
            n_vals,
            times * 1000.0,  # En milisegundos
            yerr=std_devs * 1000.0,
            fmt='o',
            color='#1F77B4',
            ecolor='#AEC7E8',
            elinewidth=2,
            capsize=4,
            label='Tiempo Experimental Medido'
        )

        # Curva de ajuste teórico continuo
        n_dense = np.linspace(n_vals.min(), n_vals.max(), 200)
        # B escala como 5 * N en este benchmark
        b_dense = n_dense * 5.0
        theor_dense = n_dense + b_dense * np.log2(np.maximum(2.0, n_dense))
        curve_dense = c_fit * theor_dense * 1000.0

        plt.plot(
            n_dense,
            curve_dense,
            '--',
            color='#D62728',
            linewidth=2,
            label=f'Curva Teórica Ajustada $O(N + B \\log N)$ ($R^2 = {r_squared:.4f}$)'
        )

        plt.title('Parte 1: Validación Experimental del Reparto Voraz Óptimo\nTiempo Real vs Predicción Teórica', fontsize=12, fontweight='bold', pad=12)
        plt.xlabel('Tamaño de Entrada N (Número de Nodos, B = 5N)', fontsize=10)
        plt.ylabel('Tiempo de Ejecución (ms)', fontsize=10)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend(frameon=True, facecolor='white', framealpha=0.9)
        plt.tight_layout()

        plt.savefig(output_path)
        plt.close()
        return output_path

    @classmethod
    def plot_parte2_empirical_vs_theory(
        cls,
        benchmark_data: Dict[str, Any],
        output_path: str = "results/figures/part2_time_vs_theory.png"
    ) -> str:
        """
        Grafica el tiempo medido en Parte 2 vs la curva teórica c * (N * k).
        """
        cls._ensure_dir(os.path.dirname(output_path))

        n_vals = np.array(benchmark_data["n_values"])
        k_vals = np.array(benchmark_data["k_values"])
        times = np.array(benchmark_data["mean_times_seconds"])
        std_devs = np.array(benchmark_data["std_times_seconds"])
        theor_terms = np.array(benchmark_data["theoretical_terms"])

        c_fit = np.sum(theor_terms * times) / np.sum(theor_terms ** 2)
        fitted_curve = c_fit * theor_terms

        ss_res = np.sum((times - fitted_curve) ** 2)
        ss_tot = np.sum((times - np.mean(times)) ** 2)
        r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0

        plt.figure(figsize=(9, 5.5), dpi=200)

        plt.errorbar(
            n_vals,
            times * 1000.0,
            yerr=std_devs * 1000.0,
            fmt='s',
            color='#2CA02C',
            ecolor='#98DF8A',
            elinewidth=2,
            capsize=4,
            label='Tiempo Experimental Medido'
        )

        n_dense = np.linspace(n_vals.min(), n_vals.max(), 200)
        k_dense = np.maximum(2.0, n_dense * 0.1)
        theor_dense = n_dense * k_dense
        curve_dense = c_fit * theor_dense * 1000.0

        plt.plot(
            n_dense,
            curve_dense,
            '--',
            color='#9467BD',
            linewidth=2,
            label=f'Curva Teórica Ajustada $O(N \\cdot k)$ ($R^2 = {r_squared:.4f}$)'
        )

        plt.title('Parte 2: Validación Experimental de Selección Submodular\nTiempo Real vs Predicción Teórica', fontsize=12, fontweight='bold', pad=12)
        plt.xlabel('Tamaño de Entrada N (Nodos Candidatos, k = 0.1N)', fontsize=10)
        plt.ylabel('Tiempo de Ejecución (ms)', fontsize=10)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend(frameon=True, facecolor='white', framealpha=0.9)
        plt.tight_layout()

        plt.savefig(output_path)
        plt.close()
        return output_path

    @classmethod
    def plot_submodular_ratio_validation(
        cls,
        verification_records: List[Dict[str, Any]],
        output_path: str = "results/figures/submodular_ratio_validation.png"
    ) -> str:
        """
        Grafica los ratios empíricos f(A_voraz) / f(A*) frente a la cota teórica (1 - 1/e).
        """
        cls._ensure_dir(os.path.dirname(output_path))

        instances = [r["instance_id"] for r in verification_records]
        ratios = [r["empirical_ratio"] for r in verification_records]
        nemhauser_bound = verification_records[0]["nemhauser_bound"]

        plt.figure(figsize=(8.5, 5), dpi=200)

        bars = plt.bar(instances, ratios, color='#4A90E2', width=0.55, edgecolor='#1C538C', label='Ratio Empírico $f(A_{\\mathrm{voraz}}) / f(A^*)$')
        
        # Línea de la cota teórica de Nemhauser (1 - 1/e)
        plt.axhline(
            y=nemhauser_bound,
            color='#E74C3C',
            linestyle='--',
            linewidth=2,
            label=f'Cota Demostrable $(1 - 1/e) \\approx {nemhauser_bound:.3f}$'
        )

        # Anotación en cada barra
        for bar, ratio in zip(bars, ratios):
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, yval + 0.015, f'{ratio:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

        plt.ylim(0.4, 1.08)
        plt.title('Parte 2: Verificación Experimental de la Razón de Aproximación Submodular', fontsize=11, fontweight='bold', pad=12)
        plt.xlabel('Instancia Sintética Evaluada (Fuerza Bruta vs Voraz)', fontsize=10)
        plt.ylabel('Razón de Aproximación', fontsize=10)
        plt.grid(axis='y', linestyle=':', alpha=0.6)
        plt.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9)
        plt.tight_layout()

        plt.savefig(output_path)
        plt.close()
        return output_path

    @classmethod
    def plot_variant2_simulation(
        cls,
        sim_uniform: Any,
        sim_front: Any,
        output_path: str = "results/figures/variant2_multi_round_policies.png"
    ) -> str:
        """
        Grafica la evolución temporal de la utilidad acumulada en T rondas (Uniforme vs Front-Loaded).
        """
        cls._ensure_dir(os.path.dirname(output_path))

        rounds = list(range(1, sim_uniform.total_rounds + 1))

        plt.figure(figsize=(9, 5), dpi=200)

        plt.plot(rounds, sim_uniform.cumulative_utility_per_round, '-o', color='#3498DB', linewidth=2, label='Política Uniforme ($B_t = B/T$)')
        plt.plot(rounds, sim_front.cumulative_utility_per_round, '-s', color='#E67E22', linewidth=2, label='Política Concentrada al Inicio (Front-Loaded / Decay)')

        plt.title('Variante 2: Dinámica Multi-Ronda bajo Fallas Estocásticas\nUtilidad Acumulada a lo Largo de T Rondas', fontsize=11, fontweight='bold', pad=12)
        plt.xlabel('Ronda de Entrenamiento t', fontsize=10)
        plt.ylabel('Utilidad Acumulada del Sistema', fontsize=10)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend(frameon=True, facecolor='white', framealpha=0.9)
        plt.tight_layout()

        plt.savefig(output_path)
        plt.close()
        return output_path

    @classmethod
    def plot_variant3_counterexample(
        cls,
        counter_res: Dict[str, Any],
        output_path: str = "results/figures/variant3_counterexample.png"
    ) -> str:
        """
        Grafica la comparativa del contraejemplo de interferencia (Voraz Miope vs Heurística vs Óptimo).
        """
        cls._ensure_dir(os.path.dirname(output_path))

        labels = ['Voraz Miope\n(Falla en Red)', 'Heurística Penalizada\n(Impacto Neto)', 'Óptimo Global\n(Exhaustivo)']
        values = [
            counter_res["greedy_miope_utility"],
            counter_res["heuristic_utility"],
            counter_res["optimal_utility"]
        ]
        colors = ['#E74C3C', '#F39C12', '#2ECC71']

        plt.figure(figsize=(7.5, 4.8), dpi=200)
        bars = plt.bar(labels, values, color=colors, width=0.45, edgecolor='#333333')

        for bar, val in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width() / 2.0, val + 0.3, f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

        plt.ylim(0, max(values) * 1.25)
        plt.title('Variante 3: Contraejemplo de Falla del Voraz bajo Interferencia\nUtilidad Total Obtenida en Grafo Estrella', fontsize=11, fontweight='bold', pad=12)
        plt.ylabel('Utilidad Neta del Sistema', fontsize=10)
        plt.grid(axis='y', linestyle=':', alpha=0.6)
        plt.tight_layout()

        plt.savefig(output_path)
        plt.close()
        return output_path

