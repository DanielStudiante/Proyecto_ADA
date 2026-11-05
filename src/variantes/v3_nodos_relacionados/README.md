# Variante 3: Nodos Relacionados entre Sí en un Grafo G
## Subproyecto 2 — Reparto de Presupuesto y Selección de Participantes

---

## 1. Motivación y Modelado en Grafo

En una topología distribuida de nodos interconectados $G = (V, E)$, la asignación de presupuesto $x_i$ a un nodo no opera en el vacío: genera externalidades sobre sus vecinos $N(i) = \{j \in V : (i, j) \in E\}$. El enunciado distingue dos casos con propiedades algorítmicas radicalmente diferentes:

---

## 2. Caso Aditivo (Sinergias y Cooperación Vecinal)

### Formulación
La utilidad de cada nodo $i$ se incrementa con la actividad de sus vecinos:
$$\tilde{u}_i(x_i, \mathbf{x}_{N(i)}) = u_i(x_i) + \gamma \sum_{j \in N(i)} h(x_j)$$
donde $\gamma \ge 0$ es la tasa de sinergia y $h(x)$ es una función cóncava y monótona creciente.

### Demostración Formal de Optimalidad del Voraz
Calculamos la función objetivo global sumando sobre todos los nodos $i \in V$:
$$U_{\text{total}}(\mathbf{x}) = \sum_{i=1}^N \left( u_i(x_i) + \gamma \sum_{j \in N(i)} h(x_j) \right) = \sum_{i=1}^N u_i(x_i) + \gamma \sum_{i=1}^N \sum_{j \in N(i)} h(x_j)$$

Al intercambiar el orden de sumatoria en el término de vecindad:
$$\sum_{i=1}^N \sum_{j \in N(i)} h(x_j) = \sum_{j=1}^N \left( \sum_{i \in N(j)} 1 \right) h(x_j) = \sum_{j=1}^N \deg(j) \cdot h(x_j)$$

Renombrando la variable muda $j$ por $i$:
$$U_{\text{total}}(\mathbf{x}) = \sum_{i=1}^N \left[ u_i(x_i) + \gamma \cdot \deg(i) \cdot h(x_i) \right]$$

Definiendo la función de utilidad efectiva del nodo $i$:
$$w_i(x_i) \equiv u_i(x_i) + \gamma \cdot \deg(i) \cdot h(x_i)$$

Dado que la suma ponderada de funciones cóncavas y monótonas crecientes con pesos no negativos ($\gamma \deg(i) \ge 0$) es **estrictamente cóncava y monótona creciente**, la utilidad total es:
$$U_{\text{total}}(\mathbf{x}) = \sum_{i=1}^N w_i(x_i)$$
la cual es **perfectamente separable nodo por nodo**.

**Conclusión:** El algoritmo voraz por ganancia marginal con Max-Heap sobre las funciones efectivas $w_i(x)$ **es matemáticamente óptimo**. Complejidad: $T(N, B) = O(N + B \log N)$.

---

## 3. Caso Competitivo (Interferencia y Congestión de Canal)

### Formulación
Cuando varios nodos vecinos intentan transmitir gradientes simultáneamente a través de canales compartidos, sufren congestión e interferencia mutua:
$$\tilde{u}_i(\mathbf{x}) = u_i(x_i) \left( 1 - \frac{\gamma}{B} \sum_{j \in N(i)} x_j \right)$$
La utilidad total del sistema incorpora términos bilineales cruzados no separables:
$$U_{\text{total}}(\mathbf{x}) = \sum_{i=1}^N u_i(x_i) - \frac{\gamma}{B} \sum_{(i, j) \in E} [u_i(x_i) x_j + u_j(x_j) x_i]$$

### Contraejemplo Computable: Por qué el Voraz Clásico Falla
Consideremos un grafo estrella de 3 nodos:
- Nodo 0: Hub Central conectado al Nodo 1 y al Nodo 2.
- $B = 2$ unidades de presupuesto.
- Parámetro de interferencia $\gamma = 0.9$.
- $u_0(x) = 15 \ln(1 + x)$, mientras que $u_1(x) = u_2(x) = 14 \ln(1 + x)$.

1. **Voraz Miope:** En el paso 1, evalúa solo $\Delta u_i(0)$: el nodo 0 tiene mayor ganancia (10.4 vs 9.7). Le asigna al nodo 0. Al final produce asignación $(1, 1, 0)$ o $(2, 0, 0)$. Debido a la congestión destructiva generada por el hub sobre ambas hojas, su utilidad neta es significativamente inferior.
2. **Asignación Óptima:** Asignar $x = (0, 1, 1)$ a las dos hojas independientes. Como no están conectadas entre sí, no generan congestión mutua ($\sum x_j = 0$), alcanzando una utilidad total de $19.4$, estrictamente superior a la solución voraz.

### Heurística Voraz Penalizada por Impacto Marginal Neto
En lugar de mirar únicamente la ganancia individual $\Delta u_i$, nuestra heurística calcula en cada paso el impacto marginal neto sobre el sistema completo:
$$\Delta_{\text{neto}}(i) = U_{\text{sistema}}(\mathbf{x} + \mathbf{e}_i) - U_{\text{sistema}}(\mathbf{x})$$
y asigna la siguiente unidad al nodo con mayor $\Delta_{\text{neto}}(i)$.

**Complejidad:** En cada paso $b = 1 \dots B$, evaluar los $N$ nodos toma tiempo $O(N + |E|)$. Complejidad total:
$$T(N, B, |E|) = O(B \cdot (N + |E|))$$

