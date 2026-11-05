# Proyecto Semestral 2026-B: Análisis y Diseño de Algoritmos (ADA)
## Subproyecto 2 — Reparto de Presupuesto y Selección de Participantes (Proyecto Red)

Este repositorio contiene la inicialización completa, formalización matemática, código estructurado en capas por objetos, demostraciones teóricas, análisis de complejidad asintótica, implementación de variantes obligatorias, gráficos vectoriales XML y guion para video explicativo (KLM) correspondientes al **Subproyecto 2**.

---

## 1. Estructura del Repositorio

```
ADA/
├── docs/
│   ├── DESGLOSE_ENTREGABLES.md      # Desglose exhaustivo de qué entregar, rúbrica (Tabla 5.2) y cronograma
│   ├── DOCUMENTACION_TEORICA.md     # Base teórica completa: definiciones, deducciones T(n), demostraciones formales
│   ├── arquitectura_problema.xml    # Gráfico y diagrama de flujo en XML estándar (abrible en draw.io)
│   └── guion_video_klm.md           # Guion y prompts escena por escena preparados para producción en KLM
├── src/
│   ├── core/                        # Capa de dominio y generación de datos sintéticos
│   │   ├── models.py                # Clases: FederatedNode, ConcaveUtilityFunction, NetworkGraph, RoundState
│   │   └── data_generator.py        # Generador determinista con semillas de instancias sintéticas reproducibles
│   ├── parte1_reparto/              # Capa Parte 1: Reparto óptimo exacto
│   │   ├── greedy_budget.py         # Voraz con Max-Heap O(N + B log N)
│   │   └── brute_force_budget.py    # Verificación exacta por Programación Dinámica
│   ├── parte2_seleccion/            # Capa Parte 2: Selección submodular de participantes
│   │   ├── submodular_greedy.py     # Voraz submodular con aceleración bitset O(N * k * tau)
│   │   └── brute_force_selection.py # Fuerza bruta combinatorial C(N, k) para verificar cota (1 - 1/e)
│   ├── variantes/                   # Carpetas independientes por variante obligatoria
│   │   ├── v1_costos_distintos/     # Khuller et al. (1999) con costos heterogéneos y presupuesto L
│   │   │   ├── khuller_greedy.py
│   │   │   └── README.md
│   │   ├── v2_multi_ronda_fallas/   # T rondas con fallas independientes (probabilidad q)
│   │   │   ├── multi_round_sim.py
│   │   │   └── README.md
│   │   └── v3_nodos_relacionados/   # Red de nodos con efectos aditivos vs competitivos
│   │       ├── network_effects.py
│   │       └── README.md
│   └── experiments/                 # Benchmarking y visualización científica
│       ├── benchmark_runner.py      # Medición de tiempos reales en >= 5 tamaños crecientes
│       └── plot_generator.py        # Generación de curvas empíricas vs curvas teóricas T(n)
├── results/
│   └── figures/                     # Gráficas generadas automáticamente en alta resolución
│       ├── part1_time_vs_theory.png
│       ├── part2_time_vs_theory.png
│       ├── submodular_ratio_validation.png
│       ├── variant2_multi_round_policies.png
│       └── variant3_counterexample.png
├── scripts/
│   └── run_all.py                   # Script maestro que ejecuta todo el flujo de inicio a fin
├── requirements.txt                 # Dependencias (numpy, matplotlib)
└── README.md                        # Esta guía
```

---

## 2. Requisitos y Ejecución Rápida

### Requisitos Previos
- Python 3.10+ con `numpy` y `matplotlib`.

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar Suite Completa (Validación, Benchmarks y Gráficas)
Para ejecutar la verificación de optimalidad, la prueba de la cota $(1 - 1/e)$, los benchmarks de tiempo en 6 tamaños de entrada, las 3 variantes y generar las gráficas:
```bash
python scripts/run_all.py
```

---

## 3. Resumen de Entregables Generados

1. **Desglose de Entregables (`docs/DESGLOSE_ENTREGABLES.md`):**
   - Análisis pormenorizado de las exigencias del enunciado.
   - Ponderación de calificaciones (Tabla 5.2): Formalización 10%, Reducción NP 10%, Deducción $T(n)$ 10%, Algoritmo aproximado 15%, Validación experimental 10%, Sustentación 45%.
   - Cronograma de 13 semanas y lista de chequeo (checklist).

2. **Base de la Documentación Teórica (`docs/DOCUMENTACION_TEORICA.md`):**
   - Definición formal del tamaño de entrada $n$.
   - Deducción analítica de $T(N, B) = O(N + B \log N)$ y justificación de pseudo-polinomialidad frente al caso continuo (*water-filling*).
   - Demostración de optimalidad por argumento de intercambio (*exchange argument*) para la Parte 1.
   - Demostración formal de reducción polinomial desde *Maximum Coverage* para probar la NP-dureza de la Parte 2.
   - Demostración matemática paso a paso de la cota $(1 - 1/e) \approx 63.2\%$ de Nemhauser et al. (1978).
   - Análisis y deducción de complejidades para las 3 variantes obligatorias.

3. **Gráfico Arquitectural en XML (`docs/arquitectura_problema.xml`):**
   - Archivo XML estándar de diagramación para draw.io / diagrams.net.
   - Representa el macro-nivel (Selección submodular), el micro-nivel (Reparto voraz cóncavo), las estructuras de datos (*Bitsets* y *Max-Heap*), las 3 variantes y el pipeline experimental.

4. **Guion Audiovisual para KLM (`docs/guion_video_klm.md`):**
   - Guion técnico escena por escena con tiempos estimados, prompts visuales para generación por IA, locución en español formal, fórmulas KaTeX superpuestas y demostración en código.

5. **Código Fuente Modular y en Capas (`src/`):**
   - Arquitectura limpia con POO, tipado estático y docstrings explicativos.
   - Módulos independientes para cada parte y cada variante con su respectivo `README.md`.

