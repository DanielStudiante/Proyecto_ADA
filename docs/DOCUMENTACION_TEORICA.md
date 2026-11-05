# BASE DE DOCUMENTACIÓN TÉCNICA Y MARCO TEÓRICO FORMAL
## Proyecto Semestral 2026-B: Análisis y Diseño de Algoritmos
### Subproyecto 2 — Reparto de Presupuesto y Selección de Participantes (Proyecto Red)

---

## 1. Formalización del Problema y Definición del Tamaño de Entrada

### 1.1 Contexto del Escenario: Aprendizaje Federado con Privacidad Diferencial
En un sistema de inteligencia artificial distribuido, una red de $N$ nodos clientes entrena de forma colaborativa un modelo global a lo largo de $T$ rondas. Por motivos de privacidad y seguridad, los datos locales nunca abandonan el dispositivo del nodo; en su lugar, cada participante calcula actualizaciones de gradientes locales y las ofusca mediante la inyección de ruido calibrado (mecanismo gaussiano o laplaciano de Privacidad Diferencial).

Existe una tensión fundamental:
- **Mayor ruido inyectado** $\implies$ mayor nivel de privacidad garantizada ($\epsilon$ más bajo), pero **menor utilidad** de la actualización para el modelo global.
- **Menor ruido inyectado** (mayor gasto de presupuesto de privacidad) $\implies$ **mayor utilidad**, pero consume el cupo de privacidad finito asignado al nodo.

En cada ronda $t \in \{1, \dots, T\}$, el orquestador central se enfrenta a dos decisiones acopladas:
1. **Selección de Participantes (Macro-decisión):** Elegir un subconjunto $A \subseteq \{1, \dots, N\}$ de tamaño a lo sumo $k$ ($k < N$) que aporte la mayor diversidad y representatividad de datos, minimizando la redundancia de información.
2. **Reparto Óptimo de Presupuesto (Micro-decisión):** Habiendo seleccionado el subconjunto de nodos, distribuir un presupuesto total de ruido/actualización $B$ entre ellos de manera que la ganancia de utilidad total sea máxima.

---

### 1.2 Formalización de la Parte 1 — Reparto Óptimo del Presupuesto

#### Definición de la Entrada y Salida
- **Parámetros de Entrada:**
  - $N \in \mathbb{N}$: Número de nodos seleccionados para participar en la ronda actual.
  - $B \in \mathbb{N}$: Presupuesto total a repartir, medido en unidades enteras discretas.
  - $\{u_i(x)\}_{i=1}^N$: Para cada nodo $i \in \{1, \dots, N\}$, una función de utilidad $u_i: \mathbb{N}_0 \to \mathbb{R}_{\ge 0}$ que modela la ganancia aportada en función de las $x$ unidades de presupuesto asignadas.
- **Propiedades de las Funciones de Utilidad:**
  1. **Monotonía creciente:** $u_i(x + 1) \ge u_i(x)$ para todo $x \ge 0$ (asignar más presupuesto no perjudica la utilidad).
  2. **Concavidad discreta (rendimientos marginales decrecientes):**
     $$\Delta u_i(x) = u_i(x + 1) - u_i(x)$$
     satisface que $\Delta u_i(x)$ es no creciente, es decir:
     $$\Delta u_i(x) \ge \Delta u_i(x + 1), \quad \forall x \ge 0$$
- **Salida requerida:**
  - Un vector de asignaciones enteras $\mathbf{x}^* = (x_1^*, x_2^*, \dots, x_N^*) \in \mathbb{N}_0^N$.
- **Objetivo formal:**
  $$\max_{\mathbf{x}} \sum_{i=1}^N u_i(x_i) \quad \text{sujeto a} \quad \sum_{i=1}^N x_i \le B, \quad x_i \in \mathbb{N}_0$$

#### Definición Precisa del Tamaño de Entrada para la Parte 1
- **Dimensión estructural:** $N$, el número de nodos.
- **Dimensión numérica:** $B$, la cantidad de unidades de presupuesto a asignar.
- **Justificación de la medida:** La entrada puede representarse mediante una lista de $N$ descriptores de funciones de utilidad y el entero $B$. El número de variables de decisión es exactamente $N$, y el número de pasos de asignación unitaria está acotado por $B$.

---

### 1.3 Formalización de la Parte 2 — Selección de Nodos Participantes

#### Definición de la Entrada y Salida
- **Parámetros de Entrada:**
  - $V = \{1, 2, \dots, N\}$: Conjunto de nodos candidatos disponibles.
  - $k \in \mathbb{N}$: Cupo máximo de nodos a seleccionar en la ronda actual ($k < N$).
  - $f: 2^V \to \mathbb{R}_{\ge 0}$: Función de utilidad conjunta que asigna a cada subconjunto $A \subseteq V$ un valor de utilidad global.
- **Propiedades de la Función Conjunta $f$:**
  1. **Normalizada:** $f(\emptyset) = 0$.
  2. **Monótona creciente:** Para todo $A \subseteq B \subseteq V$, se cumple $f(A) \le f(B)$.
  3. **Submodularidad:** Para todo $A \subseteq B \subseteq V$ y para cualquier elemento $v \in V \setminus B$:
     $$f(A \cup \{v\}) - f(A) \ge f(B \cup \{v\}) - f(B)$$
     *Intuición:* Agregar un nuevo nodo a un subconjunto pequeño aporta una ganancia marginal mayor o igual que agregarlo a un subconjunto más grande que ya cubre parte de esa información.
- **Salida requerida:**
  - Un subconjunto $A^* \subseteq V$ con $|A^*| \le k$.
- **Objetivo formal:**
  $$\max_{A \subseteq V, |A| \le k} f(A)$$

#### Definición Precisa del Tamaño de Entrada para la Parte 2
- **Dimensión del dominio:** $N = |V|$, el número total de nodos candidatos.
- **Dimensión de la restricción:** $k$, el tamaño del subconjunto a elegir.
- **Dimensión del oráculo/representación:** Sea $U$ el universo de características, temas o particiones de datos cubiertas por los nodos, con $|U| = m$. Si cada nodo $i$ cubre un subconjunto $S_i \subseteq U$, la entrada consiste en los $N$ conjuntos $S_1, \dots, S_N$, y el tamaño de la entrada codificada en bits es $O(N \cdot |U| + \log k)$.

---

## 2. Parte 1: Reparto Óptimo del Presupuesto (Algoritmo Voraz Exacto)

### 2.1 Especificación del Algoritmo con Max-Heap
El algoritmo voraz por ganancia marginal aprovecha la concavidad de las funciones de utilidad: la ganancia marginal de la $x$-ésima unidad asignada a un nodo es siempre superior a la de la $(x+1)$-ésima unidad asignada al mismo nodo.

```
Algoritmo 1: Reparto Voraz Óptimo por Ganancia Marginal
Entrada: Nodos {1, ..., N}, funciones de utilidad u_i(x), presupuesto total B
Salida: Asignación óptima x = (x_1, ..., x_N)

1. Para cada nodo i = 1 hasta N:
2.     x_i <- 0
3.     delta_i <- u_i(1) - u_i(0)
4. Inicializar Max-Heap H con las tuplas (-delta_i, i) para todo i in {1, ..., N}   // O(N)
5. Para paso = 1 hasta B:                                                         // B iteraciones
6.     (neg_delta, i) <- ExtraerMaximo(H)                                          // O(log N)
7.     x_i <- x_i + 1
8.     nuevo_delta <- u_i(x_i + 1) - u_i(x_i)
9.     Insertar en H (-nuevo_delta, i)                                            // O(log N)
10. Retornar x
```

---

### 2.2 Deducción Paso a Paso de la Función de Eficiencia $T(N, B)$

Analizamos el costo computacional contando operaciones elementales:

1. **Paso de inicialización (Líneas 1-3):**
   - Para cada uno de los $N$ nodos, se evalúa $u_i(1) - u_i(0)$ y se inicializa $x_i = 0$.
   - Costo: $N$ evaluaciones de utilidad $\implies c_1 \cdot N$ operaciones.
2. **Construcción del Max-Heap (Línea 4):**
   - Utilizando el algoritmo clásico de construcción de montículos (*heapify* o `build_heap`), el costo de organizar un arreglo de $N$ elementos en un heap binario es lineal:
     $$T_{\text{heapify}}(N) = \sum_{h=0}^{\lfloor \log_2 N \rfloor} \left\lceil \frac{N}{2^{h+1}} \right\rceil O(h) = O(N)$$
3. **Bucle de asignación voraz (Líneas 5-9):**
   - El bucle se repite exactamente $B$ veces (una iteración por cada unidad de presupuesto a repartir).
   - En cada iteración:
     - `ExtraerMaximo(H)`: Requiere eliminar la raíz del heap y reestructurar hacia abajo (*sift-down*), con costo a lo sumo $\lceil \log_2 N \rceil$ comparaciones e intercambios.
     - Incremento de variable: $O(1)$.
     - Cálculo de la nueva ganancia marginal: $\Delta u_i(x_i + 1) = u_i(x_i + 1) - u_i(x_i)$, costo $O(1)$ (asumiendo evaluación de la función en tiempo constante).
     - Inserción en el heap: Insertar el nuevo elemento y restaurar hacia arriba (*sift-up*), costo a lo sumo $\lceil \log_2 N \rceil$.
   - Costo total por iteración: $2 \log_2 N + O(1)$.
   - Costo del bucle: $\sum_{j=1}^B (2 \log_2 N + O(1)) = 2 B \log_2 N + O(B)$.

Sumando todas las fases:
$$T(N, B) = c_1 N + c_2 N + 2 B \log_2 N + c_3 B = O(N + B \log N)$$

#### Justificación de la Pseudo-Polinomialidad
La complejidad $O(N + B \log N)$ depende directamente del **valor numérico** de $B$, no de la longitud de su representación binaria $L = \lceil \log_2(B + 1) \rceil$.
Dado que $B = 2^L$, la complejidad expresada en función del tamaño físico de la entrada en bits es:
$$T(N, L) = O(N + 2^L \cdot \log N)$$
la cual es exponencial en $L$. Por lo tanto, el algoritmo es **pseudo-polinomial** (exactamente análogo al algoritmo de programación dinámica para el problema de la Mochila 0/1). Si $B$ es moderado (escala polinomial en $N$, e.g., $B \le N^2$), el algoritmo es extremadamente rápido y eficiente.

---

### 2.3 Demostración Formal de Optimalidad por Argumento de Intercambio (Exchange Argument)

**Teorema 1 (Optimalidad del Voraz Discreto para Funciones Cóncavas).**
*Sea $\mathbf{x} = (x_1, \dots, x_N)$ la asignación producida por el Algoritmo Voraz al agotar $B$ unidades de presupuesto. Entonces $\mathbf{x}$ maximiza $\sum_{i=1}^N u_i(x_i)$ sobre todas las asignaciones factibles $\mathbf{y} \in \mathbb{N}_0^N$ con $\sum_{i=1}^N y_i = B$.*

*Demostración.*
Sea $\mathbf{x}^* = (x_1^*, \dots, x_N^*)$ una asignación óptima arbitraria que difiere de $\mathbf{x}$. Sin pérdida de generalidad, asumimos que ambas asignaciones consumen exactamente $\sum_{i=1}^N x_i = \sum_{i=1}^N x_i^* = B$ (ya que las funciones $u_i$ son monótonas crecientes, una solución que gaste estrictamente menos de $B$ puede mejorarse asignando las unidades restantes).

Dado que $\mathbf{x} \neq \mathbf{x}^*$ y la suma de sus componentes es idéntica ($B$), deben existir al menos dos nodos distintos $j$ y $k$ tales que:
$$x_j > x_j^* \quad \text{y} \quad x_k < x_k^*$$

Consideremos la última unidad de presupuesto asignada al nodo $j$ en la solución voraz $\mathbf{x}$. Esta unidad correspondió a incrementar su asignación desde $x_j - 1$ hasta $x_j$, aportando una ganancia marginal:
$$\Delta_{\text{voraz}} = u_j(x_j) - u_j(x_j - 1)$$

Por la regla de selección voraz, el algoritmo asignó esta unidad a $j$ en lugar de a cualquier otro nodo disponible en ese momento. En particular, en ese instante el nodo $k$ tenía una asignación $\le x_k$. Por la propiedad de rendimientos decrecientes (concavidad):
$$\Delta_{\text{voraz}} \ge u_k(x_k + 1) - u_k(x_k)$$

Ahora, examinemos la asignación óptima $\mathbf{x}^*$. Como $x_k^* > x_k$, el nodo $k$ tiene en $\mathbf{x}^*$ al menos $x_k + 1$ unidades. Por concavidad de $u_k$, su última unidad asignada en $\mathbf{x}^*$ aporta una ganancia marginal de a lo sumo:
$$u_k(x_k^*) - u_k(x_k^* - 1) \le u_k(x_k + 1) - u_k(x_k)$$

De igual manera, como $x_j^* < x_j$, en $\mathbf{x}^*$ el nodo $j$ tiene a lo sumo $x_j - 1$ unidades. Si le agregáramos una unidad más a $j$ en $\mathbf{x}^*$, su ganancia marginal sería:
$$u_j(x_j^* + 1) - u_j(x_j^*) \ge u_j(x_j) - u_j(x_j - 1) = \Delta_{\text{voraz}}$$

Construyamos una nueva asignación $\mathbf{x}'$ transfiriendo una unidad del nodo $k$ al nodo $j$ en la solución óptima $\mathbf{x}^*$:
$$x_k' = x_k^* - 1, \quad x_j' = x_j^* + 1, \quad x_i' = x_i^* \quad (\forall i \notin \{j, k\})$$

La nueva solución $\mathbf{x}'$ sigue siendo factible ($\sum_i x_i' = B$ y $x_i' \ge 0$). El cambio en la utilidad total es:
$$\Delta U = U(\mathbf{x}') - U(\mathbf{x}^*) = [u_j(x_j^* + 1) - u_j(x_j^*)] - [u_k(x_k^*) - u_k(x_k^* - 1)]$$

Sustituyendo las cotas de concavidad:
$$[u_j(x_j^* + 1) - u_j(x_j^*)] \ge \Delta_{\text{voraz}} \ge [u_k(x_k^*) - u_k(x_k^* - 1)]$$
$$\implies \Delta U \ge 0 \implies U(\mathbf{x}') \ge U(\mathbf{x}^*)$$

Como $\mathbf{x}^*$ es óptima, no puede ser estrictamente menor, por lo que $U(\mathbf{x}') = U(\mathbf{x}^*)$, lo que demuestra que $\mathbf{x}'$ es también óptima.
Además, la distancia de Hamming discreta $\sum_{i=1}^N |x_i - x_i'| = \sum_{i=1}^N |x_i - x_i^*| - 2$ ha disminuido estrictamente. Aplicando este intercambio un número finito de veces (a lo sumo $\frac{1}{2} \sum_i |x_i - x_i^*|$ pasos), transformamos $\mathbf{x}^*$ en $\mathbf{x}$ preservando la optimalidad en cada paso. Por ende, la solución voraz $\mathbf{x}$ es estrictamente óptima. $\blacksquare$

---

### 2.4 Comparación con el Caso Continuo (*Water-Filling*)
Si las asignaciones $x_i$ pudieran tomar valores reales continuos ($x_i \in \mathbb{R}_{\ge 0}$), el problema se convierte en un problema de optimización convexa separable:
$$\max_{\mathbf{x}} \sum_{i=1}^N u_i(x_i) \quad \text{s.a.} \quad \sum_{i=1}^N x_i = B, \quad x_i \ge 0$$
Por las condiciones de Karush-Kuhn-Tucker (KKT), existe un multiplicador de Lagrange $\lambda > 0$ tal que para cada nodo $i$:
$$u_i'(x_i) = \lambda \quad \text{si } x_i > 0, \qquad u_i'(0) \le \lambda \quad \text{si } x_i = 0$$
Esto se resuelve mediante el algoritmo clásico de **Water-Filling (Nivelación de Derivadas Marginales)**: se ordenan las derivadas iniciales $u_i'(0)$ en $O(N \log N)$ y se "vierte agua" (presupuesto continuo) elevando el nivel de derivada hasta agotar $B$. La versión discreta analizada en nuestro proyecto es la cuantización canónica exacta de dicho proceso.

---

## 3. Parte 2: Selección de Nodos Participantes (Submodularidad y NP-Dureza)

### 3.1 Demostración Formal de NP-Dureza mediante Reducción Polinomial

Para demostrar formalmente que la selección óptima de participantes es NP-difícil, realizaremos una reducción polinomial desde el problema de **Cobertura Máxima (Maximum Coverage)**, conocido como NP-difícil por reducción clásica desde **Set Cover** (Karp, 1972).

#### Formulación del Problema de Cobertura Máxima (Instancia de Origen)
- **Instancia:** Un universo de elementos $U = \{e_1, e_2, \dots, e_m\}$, una familia de subconjuntos $\mathcal{S} = \{S_1, S_2, \dots, S_N\}$ tales que $S_i \subseteq U$, y dos enteros positivos $k \le N$ y $t \le m$.
- **Pregunta de Decisión:** ¿Existe una subcolección $\mathcal{S}' \subseteq \mathcal{S}$ con $|\mathcal{S}'| \le k$ tal que la cantidad de elementos cubiertos sea al menos $t$, es decir:
  $$\left| \bigcup_{S_i \in \mathcal{S}'} S_i \right| \ge t ?$$

#### Formulación de la Decisión de Selección de Nodos (Instancia Destino)
- **Instancia:** Un conjunto de nodos candidatos $V = \{1, 2, \dots, N\}$, una función de utilidad conjunta monótona y submodular $f: 2^V \to \mathbb{R}_{\ge 0}$, y enteros $k$ y $t$.
- **Pregunta de Decisión:** ¿Existe un subconjunto $A \subseteq V$ con $|A| \le k$ tal que $f(A) \ge t$?

#### Construcción de la Reducción en Tiempo Polinomial
Dada cualquier instancia de Cobertura Máxima $(U, \mathcal{S}, k, t)$:
1. Creamos un nodo $i \in V$ por cada subconjunto $S_i \in \mathcal{S}$, fijando $|V| = N$.
2. Definimos la función de utilidad conjunta $f(A)$ para cualquier subconjunto de nodos $A \subseteq V$ como la cardinalidad de la unión de sus conjuntos asociados:
   $$f(A) = \left| \bigcup_{i \in A} S_i \right|$$
3. Mantenemos el mismo cupo $k$ y el mismo umbral de utilidad $t$.

*Costo de la Construcción:*
La transformación únicamente define la correspondencia uno a uno entre conjuntos y nodos. Mapear los índices toma tiempo $O(N \cdot |U|)$, el cual es estrictamente polinomial en el tamaño de la entrada original.

#### Lema: $f(A)$ es Monótona y Submodular
1. **Monotonía:** Si $A \subseteq B$, entonces $\bigcup_{i \in A} S_i \subseteq \bigcup_{j \in B} S_j$. La cardinalidad de conjuntos es monótona bajo inclusión, luego $f(A) \le f(B)$.
2. **Submodularidad:** Sean $A \subseteq B \subseteq V$ y $v \notin B$. La ganancia marginal de añadir $v$ es el número de elementos nuevos que aporta $S_v$:
   $$f(A \cup \{v\}) - f(A) = \left| S_v \setminus \bigcup_{i \in A} S_i \right|$$
   $$f(B \cup \{v\}) - f(B) = \left| S_v \setminus \bigcup_{j \in B} S_j \right|$$
   Dado que $A \subseteq B \implies \bigcup_{i \in A} S_i \subseteq \bigcup_{j \in B} S_j$, el conjunto que se resta en $B$ es mayor o igual que en $A$:
   $$\left( S_v \setminus \bigcup_{j \in B} S_j \right) \subseteq \left( S_v \setminus \bigcup_{i \in A} S_i \right)$$
   Tomando cardinalidades:
   $$\left| S_v \setminus \bigcup_{j \in B} S_j \right| \le \left| S_v \setminus \bigcup_{i \in A} S_i \right| \implies f(B \cup \{v\}) - f(B) \le f(A \cup \{v\}) - f(A)$$
   Por lo tanto, $f$ es submodular.

#### Demostración de Equivalencia Bicondicional ($\iff$)
- $(\implies)$ Si la respuesta a Cobertura Máxima es **SÍ**: Existe una selección de subconjuntos $\mathcal{S}' \subseteq \mathcal{S}$ con $|\mathcal{S}'| \le k$ tal que $|\bigcup_{S_i \in \mathcal{S}'} S_i| \ge t$. Tomando el conjunto de nodos $A = \{i : S_i \in \mathcal{S}'\}$, tenemos $|A| = |\mathcal{S}'| \le k$ y $f(A) = |\bigcup_{S_i \in \mathcal{S}'} S_i| \ge t$. Por lo tanto, la respuesta a la Selección de Nodos es **SÍ**.
- $(\impliedby)$ Si la respuesta a Selección de Nodos es **SÍ**: Existe $A \subseteq V$ con $|A| \le k$ tal que $f(A) \ge t$. Tomando los subconjuntos $\mathcal{S}' = \{S_i : i \in A\}$, su cardinalidad es $|\mathcal{S}'| \le k$ y cubren $|\bigcup_{i \in A} S_i| = f(A) \ge t$ elementos. Luego la respuesta a Cobertura Máxima es **SÍ**.

*Conclusión:* Como la reducción se realiza en tiempo polinomial y Cobertura Máxima es NP-difícil, el problema de selección óptima de participantes bajo utilidad submodular es **NP-difícil**. $\blacksquare$

---

### 3.2 El Algoritmo Voraz Submodular y la Cota Demostrable $(1 - 1/e)$

#### Especificación del Algoritmo
```
Algoritmo 2: Selección Voraz Submodular
Entrada: Nodos V = {1, ..., N}, función submodular f, cupo k
Salida: Subconjunto seleccionado A con |A| = k

1. A_0 <- vacio
2. Para j = 1 hasta k:
3.     v_j <- argmax_{v in V \ A_{j-1}} [ f(A_{j-1} union {v}) - f(A_{j-1}) ]
4.     A_j <- A_{j-1} union {v_j}
5. Retornar A_k
```

---

### 3.3 Demostración Formal de la Cota de Aproximación $(1 - 1/e)$ (Nemhauser, Wolsey y Fisher, 1978)

**Teorema 2.**
*Sea $f: 2^V \to \mathbb{R}_{\ge 0}$ una función monótona no decreciente y submodular con $f(\emptyset) = 0$. Sea $A^*$ un subconjunto óptimo de tamaño $k$, y sea $A_k$ el subconjunto obtenido tras $k$ pasos del algoritmo voraz. Entonces:*
$$f(A_k) \ge \left( 1 - \frac{1}{e} \right) f(A^*) \approx 0.63212 \cdot f(A^*)$$

*Demostración Paso a Paso.*
1. Sea $A^*$ la solución óptima ($|A^*| = k$) y sea $A_{j-1}$ el conjunto voraz tras $j-1$ pasos.
2. Por monotonía de $f$:
   $$f(A^*) \le f(A^* \cup A_{j-1})$$
3. Escribamos los elementos de $A^* \setminus A_{j-1}$ como $\{w_1, w_2, \dots, w_p\}$, donde $p \le k$.
   Podemos descomponer la diferencia mediante una suma telescópica:
   $$f(A^* \cup A_{j-1}) - f(A_{j-1}) = \sum_{r=1}^p [ f(A_{j-1} \cup \{w_1, \dots, w_r\}) - f(A_{j-1} \cup \{w_1, \dots, w_{r-1}\}) ]$$
4. Por submodularidad, la ganancia marginal de agregar $w_r$ a un conjunto más grande está acotada por su ganancia al agregarlo a $A_{j-1}$:
   $$f(A_{j-1} \cup \{w_1, \dots, w_r\}) - f(A_{j-1} \cup \{w_1, \dots, w_{r-1}\}) \le f(A_{j-1} \cup \{w_r\}) - f(A_{j-1})$$
   Sumando sobre todos los elementos de $A^*$:
   $$f(A^*) - f(A_{j-1}) \le \sum_{w \in A^*} [ f(A_{j-1} \cup \{w\}) - f(A_{j-1}) ]$$
5. Por la regla de selección voraz, el elemento elegido en el paso $j$, denotado $v_j$, maximiza la ganancia marginal sobre todos los elementos disponibles. En particular, para cada $w \in A^*$:
   $$f(A_j) - f(A_{j-1}) = f(A_{j-1} \cup \{v_j\}) - f(A_{j-1}) \ge f(A_{j-1} \cup \{w\}) - f(A_{j-1})$$
6. Como hay a lo sumo $k$ elementos en $A^*$:
   $$\sum_{w \in A^*} [ f(A_{j-1} \cup \{w\}) - f(A_{j-1}) ] \le k [ f(A_j) - f(A_{j-1}) ]$$
7. Combinando las desigualdades (4) y (6):
   $$f(A^*) - f(A_{j-1}) \le k [ f(A_j) - f(A_{j-1}) ]$$
8. Reordenando en términos de la brecha residual $r_j = f(A^*) - f(A_j)$:
   $$r_j = f(A^*) - f(A_j) = [f(A^*) - f(A_{j-1})] - [f(A_j) - f(A_{j-1})]$$
   De la desigualdad anterior, $f(A_j) - f(A_{j-1}) \ge \frac{1}{k} [f(A^*) - f(A_{j-1})] = \frac{1}{k} r_{j-1}$.
   Sustituyendo:
   $$r_j \le r_{j-1} - \frac{1}{k} r_{j-1} = \left( 1 - \frac{1}{k} \right) r_{j-1}$$
9. Aplicando la recurrencia sucesivamente desde $j = 1$ hasta $k$:
   $$r_k \le \left( 1 - \frac{1}{k} \right)^k r_0$$
   Dado que $A_0 = \emptyset$ y $f(\emptyset) = 0$, la brecha inicial es $r_0 = f(A^*) - f(\emptyset) = f(A^*)$.
10. Usando la desigualdad analítica clásica $(1 - \frac{1}{k})^k < e^{-1} = \frac{1}{e}$ para todo $k \ge 1$:
    $$f(A^*) - f(A_k) = r_k \le e^{-1} f(A^*) = \frac{1}{e} f(A^*)$$
    Despejando $f(A_k)$:
    $$f(A_k) \ge \left( 1 - \frac{1}{e} \right) f(A^*) \approx 0.63212 \cdot f(A^*) \quad \blacksquare$$

---

### 3.4 Función de Eficiencia de la Selección Voraz

- En cada uno de los $k$ pasos, el algoritmo debe considerar todos los nodos candidatos restantes ($N - j + 1 \le N$).
- Para cada candidato, evalúa la ganancia marginal $f(A \cup \{v\}) - f(A)$, lo cual requiere una evaluación de la función $f$.
- Total de evaluaciones de $f$: $\sum_{j=1}^k (N - j + 1) = k \cdot N - \frac{k(k-1)}{2} = O(N \cdot k)$.
- Sea $\tau$ el costo computacional de una evaluación de $f$:
  $$T(N, k) = O(N \cdot k \cdot \tau)$$

#### Precisión Formal del Parámetro $\tau$ en Nuestra Implementación
Para la función de cobertura $f(A) = |\bigcup_{i \in A} S_i|$ con universo $|U| = m$:
- Si los conjuntos $S_i$ se representan mediante arreglos o tablas hash ordinarias, la unión toma tiempo $O(m)$ por candidato $\implies \tau = O(m)$.
- En nuestra arquitectura optimizada implementamos vectores de bits (**Bitsets** / enteros de 64 bits en Python):
  $$\tau = O\left( \left\lceil \frac{m}{64} \right\rceil \right) = O(1) \quad \text{para instancias de hasta 64 elementos, y } O(m/64) \text{ en general.}$$
Por consiguiente:
$$T(N, k, m) = O\left( N \cdot k \cdot \frac{m}{64} \right)$$

---

## 4. Variantes Obligatorias (Marco Teórico y Formalización)

### 4.1 Variante 1 — Nodos con Costos Heterogéneos de Participación (Khuller et al., 1999)

#### Planteamiento y Falla del Voraz Clásico
En la práctica, cada nodo $i$ tiene un costo de participación propio $c_i > 0$ (consumo de batería, ancho de banda, hardware heterogéneo), y se dispone de un presupuesto financiero/operativo total $L$.
$$\max_{A \subseteq V} f(A) \quad \text{s.a.} \quad \sum_{i \in A} c_i \le L$$
Si se aplica el voraz simple por ganancia marginal $f(A \cup \{v\}) - f(A)$, puede seleccionar un nodo con ganancia ligeramente mayor pero costo enorme, agotando todo el presupuesto y dando una razón de aproximación arbitrariamente mala.
Si se aplica únicamente el voraz por densidad $\frac{\Delta f(v)}{c_v}$, también puede fallar drásticamente (e.g., elegir muchos elementos de costo 1 con ganancia diminuta y dejar fuera un elemento que llena el presupuesto con ganancia enorme).

#### Algoritmo de Khuller, Moss y Naor (1999)
Para restaurar una garantía demostrable, Khuller et al. demostraron que el siguiente algoritmo voraz modificado garantiza al menos $\frac{1}{2}(1 - 1/e) \approx 31.6\%$ del óptimo:
1. **Paso 1 (Voraz por Densidad):** Inicializar $S_{\text{ratio}} = \emptyset$, costo residual $L_{\text{rem}} = L$. En cada paso, elegir el nodo no seleccionado $v$ que maximice $\frac{f(S_{\text{ratio}} \cup \{v\}) - f(S_{\text{ratio}})}{c_v}$ tal que $c_v \le L_{\text{rem}}$. Agregar $v$ y actualizar $L_{\text{rem}} \leftarrow L_{\text{rem}} - c_v$, hasta que ningún nodo restante quepa.
2. **Paso 2 (Mejor Singleton):** Encontrar el mejor nodo individual factible:
   $$v_{\text{best}} = \arg\max_{i \in V, c_i \le L} f(\{i\})$$
3. **Paso 3 (Selección Final):** Retornar la mejor entre ambas soluciones:
   $$A_{\text{final}} = \arg\max \{ f(S_{\text{ratio}}), f(\{v_{\text{best}}\}) \}$$

#### Teorema de Garantía de Khuller
$$f(A_{\text{final}}) \ge \frac{1}{2} \left( 1 - \frac{1}{e} \right) f(A^*) \approx 0.316 \cdot f(A^*)$$
*Complejidad:* Evalúa a lo sumo $N$ pasos, revisando los $N$ nodos candidatos en cada uno $\implies T(N, L, \tau) = O(N^2 \cdot \tau)$.

*(Nota: La versión con enumeración de tríos iniciales de tamaño $\le 3$ combinada con densidad alcanza la cota plena $1 - 1/e$, con complejidad $O(N^4 \cdot \tau)$).*

---

### 4.2 Variante 2 — Repetición en $T$ Rondas con Fallas Estocásticas Independientes

#### Escenario y Modelado de Fallas
En cada ronda $t \in \{1, \dots, T\}$, cada nodo $i \in V$ sufre fallas de comunicación o desconexión temporal de manera independiente con probabilidad $q \in [0, 1)$ (modelo Bernoulli $X_{i,t} \sim \text{Bernoulli}(1-q)$).
Si un nodo falla en la ronda $t$, no puede participar ni aportar utilidad, pero su presupuesto de ruido no se desperdicia si la decisión se toma sobre los nodos disponibles.

Adicionalmente, cada nodo $i$ tiene un presupuesto global de ruido acumulado $B_i^{\text{total}}$ para las $T$ rondas.

#### Derivación de la Complejidad Temporal del Flujo Completo
En cada una de las $T$ rondas:
1. Filtro de disponibilidad: $O(N)$.
2. Selección voraz submodular de $k$ nodos entre los sobrevivientes: $O(N \cdot k \cdot \tau)$.
3. Reparto óptimo del presupuesto de la ronda $B_t$ entre los $k$ nodos seleccionados usando Max-Heap: $O(k + B_t \log k) \subseteq O(N + B \log N)$.
Multiplicando por las $T$ rondas:
$$T_{\text{multi-ronda}} = O\left( T \cdot (N \cdot k \cdot \tau + N + B \log N) \right)$$

#### Comparación de Políticas de Gasto de Presupuesto
1. **Política Uniforme:** Repartir el presupuesto equitativamente en cada ronda $B_t = \lfloor B_{\text{total}} / T \rfloor$.
2. **Política Concentrada al Inicio (Front-Loaded / Decay):** Asignar mayor presupuesto en las primeras rondas (cuando el modelo base está frío y los gradientes aportan mayores saltos de convergencia) mediante una regla de decaimiento geométrico o armónico:
   $$B_t \propto \frac{1}{\sqrt{t}} \quad \text{o} \quad B_t = B_{\max} \cdot \alpha^t$$

---

### 4.3 Variante 3 — Nodos Relacionados en Grafo: Efectos Aditivos vs Competitivos

Los nodos de la red no operan aislados, sino que forman una topología de grafo no dirigido $G = (V, E)$, donde $N(i) = \{j \in V : (i, j) \in E\}$ representa el vecindario del nodo $i$.

#### Caso Aditivo (Sinergias y Cooperación Vecinal)
La utilidad percibida por el nodo $i$ cuando se asigna el vector de presupuesto $\mathbf{x}$ es:
$$\tilde{u}_i(x_i, \mathbf{x}_{N(i)}) = u_i(x_i) + \gamma \sum_{j \in N(i)} h(x_j)$$
donde $\gamma \ge 0$ es el coeficiente de sinergia, y $h(x)$ es una función cóncava y monótona creciente.

**Demostración de que el Voraz de la Parte 1 sigue siendo Óptimo:**
Calculamos la utilidad total del sistema sumando sobre todos los nodos $i \in V$:
$$U_{\text{total}}(\mathbf{x}) = \sum_{i=1}^N \tilde{u}_i(x_i, \mathbf{x}_{N(i)}) = \sum_{i=1}^N \left( u_i(x_i) + \gamma \sum_{j \in N(i)} h(x_j) \right)$$
Intercambiando el orden de sumatoria en el segundo término:
$$\sum_{i=1}^N \sum_{j \in N(i)} h(x_j) = \sum_{j=1}^N \sum_{i \in N(j)} h(x_j) = \sum_{j=1}^N \deg(j) \cdot h(x_j)$$
Renombrando el índice mudo $j$ como $i$:
$$U_{\text{total}}(\mathbf{x}) = \sum_{i=1}^N \left[ u_i(x_i) + \gamma \cdot \deg(i) \cdot h(x_i) \right]$$
Definimos la función de utilidad efectiva del nodo $i$:
$$w_i(x_i) \equiv u_i(x_i) + \gamma \cdot \deg(i) \cdot h(x_i)$$
Como $u_i$ y $h$ son funciones cóncavas y monótonas crecientes, y $\gamma \cdot \deg(i) \ge 0$, la combinación lineal cónica $w_i(x_i)$ es **estrictamente monótona creciente y cóncava**.
Dado que $U_{\text{total}}(\mathbf{x}) = \sum_{i=1}^N w_i(x_i)$ es completamente **separable nodo por nodo**, el problema se reduce exactamente a la Parte 1 sustituyendo $u_i$ por $w_i$.
*Conclusión:* El algoritmo voraz por ganancia marginal con Max-Heap sobre las ganancias marginales $\Delta w_i(x) = \Delta u_i(x) + \gamma \deg(i) \Delta h(x)$ **es matemáticamente óptimo**. $\blacksquare$

---

#### Caso Competitivo (Interferencia y Congestión de Canal)
Cuando los nodos vecinos saturan canales de comunicación compartidos o causan interferencia, la utilidad de $i$ decrece con el gasto de sus vecinos:
$$\tilde{u}_i(\mathbf{x}) = u_i(x_i) \left( 1 - \gamma \sum_{j \in N(i)} \frac{x_j}{B} \right)$$
con $\gamma \in (0, 1]$. La utilidad total es:
$$U_{\text{total}}(\mathbf{x}) = \sum_{i=1}^N u_i(x_i) - \frac{\gamma}{B} \sum_{i=1}^N \sum_{j \in N(i)} u_i(x_i) x_j$$

**Contraejemplo Formal: Por qué el Voraz Falla**
Consideremos 2 nodos conectados por una arista ($N=2$, $E=\{(1, 2)\}$), presupuesto $B = 2$, $\gamma = 0.5$.
- Utilidades individuales idénticas cóncavas: $u_1(0) = u_2(0) = 0$, $u(1) = 10$, $u(2) = 12$.
  - Ganancias marginales individuales: $\Delta u(0) = 10$, $\Delta u(1) = 2$.
- Si un algoritmo voraz miope asigna unidades basándose en la ganancia marginal aislada:
  - Paso 1: Nodo 1 recibe 1 unidad. $\Delta = 10$.
  - Paso 2: Sin penalización cruzada actualizada o con decisión miope, el nodo 2 ofrece ganancia individual 10 vs ganancia 2 del nodo 1. Asigna 1 unidad al nodo 2.
    Asignación voraz: $\mathbf{x}_{\text{voraz}} = (1, 1)$.
    Utilidad total voraz:
    $$\tilde{u}_1 = 10 \left(1 - 0.5 \cdot \frac{1}{2}\right) = 10 \cdot 0.75 = 7.5$$
    $$\tilde{u}_2 = 10 \left(1 - 0.5 \cdot \frac{1}{2}\right) = 7.5 \implies U_{\text{total}}(1, 1) = 15.0$$
- Consideremos la asignación concentrada $\mathbf{x}_{\text{alt}} = (2, 0)$:
    El nodo 2 tiene 0 unidades, por lo que no causa congestión sobre el nodo 1:
    $$\tilde{u}_1 = 12 \left(1 - 0.5 \cdot \frac{0}{2}\right) = 12.0$$
    $$\tilde{u}_2 = 0 \implies U_{\text{total}}(2, 0) = 12.0$$
- Ahora consideremos una función con fuerte congestión: sean 3 nodos en estrella, centro $C$, hojas $H_1, H_2$, con $\gamma = 0.9$, $B = 2$.
  El nodo centro tiene $\Delta u(0) = 15$, las hojas tienen $\Delta u(0) = 14$.
  El voraz elige al centro en el paso 1. Al asignar al centro, genera interferencia sobre ambas hojas, destruyendo su utilidad. Una asignación a las dos hojas $(0, 1, 1)$ logra utilidad total superior a $(1, 1, 0)$ o $(2, 0, 0)$.

*Conclusión Matemática:* La función objetivo contiene términos bilineales cruzados $-x_i x_j$ que rompen la separabilidad y la concavidad del sistema conjunto. La ganancia marginal de asignar a un nodo depende negativamente de las asignaciones de sus vecinos, invalidando el argumento de intercambio.

#### Heurística Propuesta: Voraz Penalizado por Impacto de Congestión Marginal
En lugar de evaluar la ganancia aislada $\Delta u_i(x_i)$, calculamos el impacto global neto sobre el sistema al incrementar $x_i$ en 1 unidad:
$$\Delta_{\text{neto}}(i) = U_{\text{total}}(\mathbf{x} + \mathbf{e}_i) - U_{\text{total}}(\mathbf{x})$$
$$\Delta_{\text{neto}}(i) = [u_i(x_i + 1) - u_i(x_i)] \left(1 - \frac{\gamma}{B}\sum_{j \in N(i)} x_j\right) - \frac{\gamma}{B} \sum_{j \in N(i)} u_j(x_j)$$
*Complejidad de la Heurística:* En cada uno de los $B$ pasos, evaluar el impacto neto de los $N$ nodos candidatos toma $O(N \cdot \bar{d})$, donde $\bar{d}$ es el grado promedio del grafo. Complejidad total: $T(N, B) = O(B \cdot (N + |E|))$.

---

## 5. Referencias Bibliográficas

1. **Nemhauser, G. L., Wolsey, L. A., & Fisher, M. L. (1978).** An analysis of approximations for maximizing submodular set functions—I. *Mathematical Programming*, 14(1), 265–294.
2. **Khuller, S., Moss, A., & Naor, J. (1999).** The budgeted maximum coverage problem. *Information Processing Letters*, 70(1), 39–45.
3. **Karp, R. M. (1972).** Reducibility among combinatorial problems. In *Complexity of Computer Computations* (pp. 85–103). Springer, Boston, MA.
4. **Boyd, S., & Vandenberghe, L. (2004).** *Convex Optimization* (Capítulo sobre Water-Filling y condiciones KKT). Cambridge University Press.
5. **Garey, M. R., & Johnson, D. S. (1979).** *Computers and Intractability: A Guide to the Theory of NP-Completeness*. W. H. Freeman and Co.

