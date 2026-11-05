# Variante 2: Repetición en T Rondas con Nodos que Fallan entre Rondas
## Subproyecto 2 — Reparto de Presupuesto y Selección de Participantes

---

## 1. Descripción del Escenario Multi-Ronda

En el entrenamiento colaborativo real, el aprendizaje no ocurre en un solo instante, sino a lo largo de un horizonte temporal finito de $T$ rondas. Durante este proceso:
1. **Fallas Estocásticas:** En cada ronda $t \in \{1, \dots, T\}$, cada nodo $i \in V$ sufre desconexión o falla de comunicación de forma independiente con probabilidad $q \in [0, 1)$ (modelo Bernoulli $X_{i,t} \sim \text{Bernoulli}(1-q)$).
2. **Presupuesto Finito Acumulado:** Cada nodo tiene un presupuesto de ruido total $B_i^{\text{total}}$ para todo el proyecto. Si agota su presupuesto en rondas tempranas, queda inhabilitado para aportar en rondas futuras.

---

## 2. Deducción de la Función de Complejidad Temporal del Flujo

En cada una de las $T$ rondas se realizan tres etapas secuenciales:
1. **Filtrado de Disponibilidad:** Evaluar la condición de falla y el presupuesto restante para los $N$ nodos candidatos:
   $$T_1 = O(N)$$
2. **Selección Voraz Submodular:** De entre los nodos disponibles ($N_{\text{disp}} \le N$), seleccionar los $k$ más representativos maximizando la cobertura con Bitsets:
   $$T_2 = O(N \cdot k \cdot \tau) = O\left( N \cdot k \cdot \left\lceil \frac{m}{64} \right\rceil \right)$$
3. **Reparto Óptimo del Presupuesto de la Ronda:** Repartir el presupuesto $B_t$ de la ronda entre los $k$ nodos elegidos mediante Max-Heap:
   $$T_3 = O(k + B_t \log k) \subseteq O(N + B_t \log N)$$

Sumando las tres fases a lo largo de las $T$ rondas:
$$T_{\text{total}} = \sum_{t=1}^T \left[ O(N) + O(N \cdot k \cdot \tau) + O(N + B_t \log N) \right]$$
Dado que $\sum_{t=1}^T B_t = B_{\text{total}}$, la cota asintótica consolidada exigida por el enunciado es:
$$T(T, N, k, B, \tau) = O\left( T \cdot (N \cdot k \cdot \tau + N) + B_{\text{total}} \log N \right) \subseteq O\left( T \cdot (N \cdot k \cdot \tau + N + B \log N) \right)$$

---

## 3. Políticas de Gasto de Presupuesto

El módulo compara experimentalmente dos políticas fundamentales de distribución del presupuesto $B$:

| Política | Definición de $B_t$ | Ventajas | Riesgos |
|----------|---------------------|----------|---------|
| **Uniforme** | $B_t = \lfloor B_{\text{total}} / T \rfloor$ | Gasto predecible y balanceado en todo el horizonte. | Si un nodo clave falla en rondas intermedias, se desaprovechan sus datos iniciales. |
| **Front-Loaded (Decaimiento)** | $B_t \propto \alpha^t$ ($\alpha < 1$) | Maximiza las ganancias iniciales cuando el modelo aprende más rápido y los nodos aún no han fallado. | Menor presupuesto disponible para refinamiento en rondas tardías. |

---

## 4. Modo de Uso

```python
from src.core.data_generator import SyntheticInstanceGenerator
from src.variantes.v2_multi_ronda_fallas.multi_round_sim import MultiRoundSimulator

nodes = SyntheticInstanceGenerator.generate_nodes(num_nodes=60, default_noise_budget=200, seed=42)

# Simular con Política Uniforme
res_uniform = MultiRoundSimulator.run_simulation(
    nodes=nodes,
    total_rounds=15,
    k=10,
    total_budget=600,
    failure_prob=0.1,
    policy="uniform",
    seed=101
)

# Simular con Política Front-Loaded (concentrado al inicio)
res_front = MultiRoundSimulator.run_simulation(
    nodes=nodes,
    total_rounds=15,
    k=10,
    total_budget=600,
    failure_prob=0.1,
    policy="front_loaded",
    seed=101
)

print(f"Utilidad Final Uniforme: {res_uniform.cumulative_utility_per_round[-1]:.2f}")
print(f"Utilidad Final Front-Loaded: {res_front.cumulative_utility_per_round[-1]:.2f}")
```

