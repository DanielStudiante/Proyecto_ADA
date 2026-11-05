# Variante 1: Nodos con Costos de Participación Heterogéneos
## Subproyecto 2 — Reparto de Presupuesto y Selección de Participantes

---

## 1. Motivación y Planteamiento del Problema

En la Parte 2 estándar, la selección de nodos participantes opera bajo una restricción de cardinalidad uniforme $|A| \le k$ (todos los nodos "cuestan" 1 cupo). En un entorno real de Aprendizaje Federado, los dispositivos participantes presentan costos de operación dispares:
- Teléfonos móviles con batería limitada frente a servidores locales con energía constante.
- Nodos con anchos de banda restringidos frente a conexiones de fibra óptica.

Formalmente, cada nodo $i \in V$ tiene un costo de participación asociado $c_i > 0$ y se dispone de un presupuesto operativo total $L$:
$$\max_{A \subseteq V} f(A) \quad \text{sujeto a} \quad \sum_{i \in A} c_i \le L$$
donde $f(A) = |\bigcup_{i \in A} S_i|$ es una función monótona y submodular. Este problema se conoce como **Budgeted Maximum Coverage** o **Maximización Submodular bajo Restricción de Mochila (Knapsack)**.

---

## 2. Por qué Falla el Voraz Simple

1. **Voraz por Ganancia Absoluta:** Si solo evaluamos $f(A \cup \{v\}) - f(A)$, el algoritmo puede elegir un nodo con ganancia marginal ligeramente superior pero con un costo $c_i = L$, impidiendo seleccionar decenas de otros nodos que colectivamente aportarían una utilidad mucho mayor. La razón de aproximación puede ser arbitrariamente mala ($1/N$).
2. **Voraz por Densidad Puro:** Si solo evaluamos $\frac{\Delta f(v)}{c_v}$, consideremos una instancia con dos tipos de elementos:
   - Un nodo de "bajo costo": $c_1 = \epsilon$, ganancia marginal $2\epsilon$. Densidad = 2.
   - Un nodo de "alto costo": $c_2 = L$, ganancia marginal $L$. Densidad = 1.
   Con presupuesto $L$, el voraz por densidad elige el elemento 1 (utilidad $2\epsilon$) y si no hay más elementos pequeños, se detiene con $2\epsilon$, mientras que el óptimo elige el elemento 2 con utilidad $L$. Para $\epsilon \to 0$, el ratio $2\epsilon / L \to 0$.

---

## 3. Algoritmo de Khuller, Moss y Naor (1999)

Para resolver este dilema, Khuller et al. demostraron que combinando el voraz por densidad con el mejor elemento unitario se restaura una garantía de aproximación estricta:

1. **Paso 1:** Ejecutar el voraz por densidad eligiendo en cada paso el elemento factible que maximice $\frac{f(A \cup \{v\}) - f(A)}{c_v}$. Sea $A_{\text{ratio}}$ la solución resultante.
2. **Paso 2:** Encontrar el nodo individual factible con mayor utilidad:
   $$v^* = \arg\max_{i \in V, c_i \le L} f(\{i\})$$
3. **Paso 3:** Retornar $A_{\text{final}} = \arg\max \{ f(A_{\text{ratio}}), f(\{v^*\}) \}$.

### Garantía Teórica Demostrable
$$f(A_{\text{final}}) \ge \frac{1}{2} \left( 1 - \frac{1}{e} \right) f(A^*) \approx 0.316 \cdot f(A^*)$$

---

## 4. Complejidad Temporal

- Bucle de densidad: A lo sumo $N$ selecciones, cada una evaluando a lo sumo $N$ candidatos restantes $\implies O(N^2 \cdot \tau)$.
- Búsqueda del mejor singleton: $N$ evaluaciones $\implies O(N \cdot \tau)$.
- Complejidad Total:
  $$T(N, L, \tau) = O(N^2 \cdot \tau) = O\left( N^2 \cdot \left\lceil \frac{m}{64} \right\rceil \right)$$

---

## 5. Modo de Uso

```python
from src.core.data_generator import SyntheticInstanceGenerator
from src.variantes.v1_costos_distintos.khuller_greedy import KhullerBudgetedSelector

# Generar candidatos con costos heterogéneos
nodes = SyntheticInstanceGenerator.generate_nodes(num_nodes=50, universe_size=100, seed=42)

# Ejecutar el selector de Khuller con presupuesto de costo L = 25.0
result = KhullerBudgetedSelector.select(candidates=nodes, cost_budget=25.0)

print(f"Estrategia elegida: {result.chosen_strategy}")
print(f"Nodos seleccionados: {result.selected_node_ids}")
print(f"Utilidad alcanzada: {result.total_utility}")
print(f"Costo invertido: {result.total_cost_spent} / {result.budget_limit}")
```

