# GUION TÉCNICO Y ESPECIFICACIÓN AUDIOVISUAL PARA KLM
## Proyecto Semestral 2026-B: Análisis y Diseño de Algoritmos (ADA)
### Video de Sustentación: Subproyecto 2 — Reparto de Presupuesto y Selección de Participantes

---

## 1. Ficha Técnica del Video

- **Duración Estimada:** 8 a 10 minutos (dividido en 7 escenas clave).
- **Audiencia Objetivo:** Docentes evaluadores y jurado del curso de Análisis y Diseño de Algoritmos.
- **Tono:** Académico, formal, riguroso, fluido y convincente.
- **Formato Visual:** Presentación dinámica con avatar/presentador en esquina inferior (estilo PiP), animaciones de grafos, montículos binarios, ecuaciones LaTeX y ejecución de terminal.

---

## 2. Estructura Escena por Escena

---

### ESCENA 1: Introducción y Contexto del Escenario Federado
- **Duración:** 60 segundos
- **Título de Escena:** `SCENE_01_INTRO_SCENARIO`
- **Prompt Visual para KLM / Generador de Video:**
  > *Ultra-realistic presentation room with dark tech background. The screen displays an animated network graph of N distributed nodes sending encrypted gradient updates with noise to a central server. Infographics illustrate the privacy-utility tradeoff: higher noise means more privacy but less utility. The presenter introduces the project.*
- **Texto en Pantalla (Overlay Text):**
  - Proyecto Semestral 2026-B | Análisis y Diseño de Algoritmos
  - Subproyecto 2: Reparto de Presupuesto y Selección de Participantes
  - Dos niveles acoplados: Macro-selección Submodular + Micro-reparto Cóncavo
- **Locución (Voiceover Script):**
  > *"Bienvenidos a la presentación formal de nuestro proyecto semestral de Análisis y Diseño de Algoritmos. A nuestro equipo le fue asignado el Subproyecto 2: Reparto de un presupuesto limitado y selección de participantes en una red colaborativa.*
  >
  > *En este escenario, $N$ nodos entrenan conjuntamente un modelo global a lo largo de $T$ rondas mediante Aprendizaje Federado con Privacidad Diferencial. Cada participante debe inyectar ruido para proteger sus datos locales. Esto crea una tensión computacional y matemática: el ruido protege la privacidad pero degrada la utilidad.*
  >
  > *Para optimizar el sistema, enfrentamos dos problemas jerárquicos: primero, seleccionar el mejor subconjunto de $k$ nodos participantes —un problema NP-difícil que resolveremos con garantías submodulares—; y segundo, repartir de forma óptima un presupuesto de ruido $B$ entre ellos, el cual resolveremos exactamente en tiempo polinomial usando propiedades de concavidad."*

---

### ESCENA 2: Parte 1 — Reparto Óptimo con Max-Heap y Demostración por Intercambio
- **Duración:** 90 segundos
- **Título de Escena:** `SCENE_02_PARTE1_GREEDY_OPTIMAL`
- **Prompt Visual para KLM / Generador de Video:**
  > *Clean split-screen. On the left: a dynamic visual animation of a Max-Heap data structure with nodes holding marginal gains $\Delta u_i(x_i)$. Each step highlights the root being extracted, $x_i$ incremented, and reinserted. On the right: a sleek card showing the formal Exchange Argument proof step by step.*
- **Texto en Pantalla (Overlay Text):**
  - **Parte 1:** $\max \sum_{i=1}^N u_i(x_i)$ s.a. $\sum x_i \le B, \quad x_i \in \mathbb{N}_0$
  - **Algoritmo:** Voraz por Ganancia Marginal con Max-Heap
  - **Complejidad:** $T(N, B) = O(N + B \log N)$ (Pseudo-polinomial)
  - **Teorema:** Demostración por Argumento de Intercambio (Exchange Argument)
- **Locución (Voiceover Script):**
  > *"Iniciemos con la Parte 1. Disponemos de $N$ nodos seleccionados y un presupuesto entero $B$. Cada nodo posee una función de utilidad cóncava y monótona $u_i(x)$. La concavidad implica rendimientos marginales decrecientes: la ganancia marginal $\Delta u_i(x) = u_i(x+1) - u_i(x)$ nunca aumenta.*
  >
  > *El algoritmo voraz asigna cada una de las $B$ unidades al nodo con mayor ganancia marginal en ese instante. Implementamos esto de manera óptima utilizando una cola de prioridad basada en un montículo binario de máximos (Max-Heap). Construir el heap inicial toma $O(N)$ mediante heapify, y cada una de las $B$ asignaciones requiere extraer el máximo y reinsertar con la nueva ganancia marginal en $O(\log N)$. Esto nos da una función de eficiencia analítica de $T(N, B) = O(N + B \log N)$.*
  >
  > *¿Por qué es estrictamente óptimo? Lo demostramos formalmente mediante un argumento de intercambio: si existiera una solución óptima distinta que no asigne en orden decreciente de ganancia marginal, existiría un nodo $k$ con exceso de asignación y un nodo $j$ con defecto. Al transferir una unidad de $k$ a $j$, la concavidad nos asegura que la ganancia de $j$ es mayor o igual a la pérdida de $k$, manteniendo o mejorando la utilidad total. Repitiendo este intercambio, convergemos a la solución voraz sin perder valor, probando que el voraz es óptimo."*

---

### ESCENA 3: Parte 2 — Demostración Formal de NP-Dureza (Reducción Polinomial)
- **Duración:** 90 segundos
- **Título de Escena:** `SCENE_03_NP_HARDNESS_REDUCTION`
- **Prompt Visual para KLM / Generador de Video:**
  > *Blackboard style presentation with crisp neon mathematical annotations. Diagram shows the polynomial reduction mapping: on the left, an arbitrary instance of Maximum Coverage $(U, \mathcal{S}, k, t)$; on the right, the constructed Federated Node Selection problem with submodular utility $f(A) = |\bigcup_{i \in A} S_i|$. Bidirectional implication arrows flash.*
- **Texto en Pantalla (Overlay Text):**
  - **Reducción:** Maximum Coverage $\le_P$ Selección de Participantes
  - **Instancia:** $S_i \subseteq U \to \text{Nodo } i$ con cobertura $S_i$
  - **Utilidad:** $f(A) = |\bigcup_{i \in A} S_i|$ (Monótona y Submodular)
  - **Equivalencia:** $\exists \mathcal{S}' \text{ cubre } \ge t \iff \exists A \text{ con } f(A) \ge t$
  - **Conclusión:** NP-difícil
- **Locución (Voiceover Script):**
  > *"Pasamos a la Parte 2: la selección de los $k$ nodos participantes. Aquí la función de utilidad conjunta $f(A)$ es submodular: incorporar un nodo a un grupo grande genera menor ganancia marginal que incorporarlo a un grupo pequeño por redundancia de información.*
  >
  > *Como exige el enunciado, demostramos formalmente que este problema es NP-difícil mediante una reducción polinomial desde Cobertura Máxima (Maximum Coverage), un problema NP-difícil clásico.*
  >
  > *Dada una instancia de Cobertura Máxima con un universo $U$ y subconjuntos $S_1$ a $S_N$, construimos en tiempo $O(N \cdot |U|)$ un nodo por cada conjunto $S_i$, definiendo la función de utilidad conjunta como el cardinal de la unión. Demostramos algebraicamente que esta función es estrictamente monótona y submodular. Finalmente, probamos la equivalencia en ambas direcciones: existe una familia de $k$ conjuntos que cubre al menos $t$ elementos si y solo si existe una selección de $k$ nodos con utilidad mayor o igual a $t$. Al ser una reducción válida y polinomial, queda rigurosamente demostrado que el problema es NP-difícil."*

---

### ESCENA 4: Algoritmo Aproximado y Demostración de la Cota $(1 - 1/e)$
- **Duración:** 90 segundos
- **Título de Escena:** `SCENE_04_SUBMODULAR_BOUND`
- **Prompt Visual para KLM / Generador de Video:**
  > *Mathematical slide showing the recurrence of the residual gap $r_j \le (1 - 1/k) r_{j-1}$. A graph reveals how the ratio converges asymptotically to $1 - 1/e \approx 0.632$. Code view shows the Python implementation using 64-bit integer bitsets for $O(1)$ fast union operations.*
- **Texto en Pantalla (Overlay Text):**
  - **Algoritmo:** Voraz Submodular (Nemhauser, Wolsey y Fisher, 1978)
  - **Recurrencia de la Brecha:** $r_j \le (1 - 1/k) r_{j-1}$
  - **Cota Teórica:** $f(A_k) \ge (1 - 1/e) f(A^*) \approx 63.2\%$
  - **Complejidad:** $T(N, k, \tau) = O(N \cdot k \cdot \tau)$ con $\tau = O(\lceil m/64 \rceil)$
- **Locución (Voiceover Script):**
  > *"Frente a la NP-dureza, aplicamos el algoritmo voraz submodular propuesto por Nemhauser, Wolsey y Fisher en 1978. En cada uno de los $k$ pasos, el algoritmo incorpora el nodo que maximiza la ganancia marginal sobre los nodos ya seleccionados.*
  >
  > *Este algoritmo cuenta con una garantía matemática célebre: alcanza al menos $(1 - 1/e) \approx 63.2\%$ de la utilidad óptima. La demostración se basa en analizar la brecha residual $r_j = f(A^*) - f(A_j)$. Por submodularidad, la ganancia del mejor elemento voraz es de al menos un $k$-ésimo de la brecha pendiente, lo que induce la recurrencia $r_j \le (1 - 1/k) r_{j-1}$. Al cabo de $k$ pasos, la brecha final satisface $r_k \le (1 - 1/k)^k r_0 \le e^{-1} f(A^*)$, asegurando la cota del 63.2%.*
  >
  > *En nuestra implementación, optimizamos el costo de evaluación $\tau$ utilizando operaciones a nivel de bits (Bitsets), logrando un tiempo de ejecución de $O(N \cdot k \cdot \lceil m/64 \rceil)$, lo cual es órdenes de magnitud más rápido que una representación ingenua con conjuntos."*

---

### ESCENA 5: Las 3 Variantes Obligatorias Implementadas
- **Duración:** 120 segundos
- **Título de Escena:** `SCENE_05_OBLIGATORY_VARIANTS`
- **Prompt Visual para KLM / Generador de Video:**
  > *Triptych 3-column layout showcasing the three mandatory variants: (1) Budgeted Coverage with cost tags and Khuller's formula; (2) Time series simulation of T rounds with red failure crosses and allocation curves; (3) Graph network with green synergy links (additive) and red dashed interference lines (competitive).*
- **Texto en Pantalla (Overlay Text):**
  - **Variante 1:** Costos heterogéneos | Khuller et al. (1999) | Garantía $\frac{1}{2}(1 - 1/e)$
  - **Variante 2:** $T$ rondas con fallas Bernoulli ($q$) | Políticas Uniforme vs Front-Loaded
  - **Variante 3:** Grafo de Nodos | Caso Aditivo (Voraz Óptimo) vs Competitivo (Heurística Penalizada)
- **Locución (Voiceover Script):**
  > *"El proyecto exige el análisis y desarrollo obligatorio de tres variantes realistas:
  >
  > *En la Variante 1, los nodos tienen costos de participación $c_i$ heterogéneos y un presupuesto de costo $L$. El voraz simple pierde su garantía. Implementamos el algoritmo de Khuller, Moss y Naor de 1999, que selecciona el mejor entre el voraz por densidad costo-beneficio y el mejor nodo individual, demostrando una garantía de $\frac{1}{2}(1 - 1/e) \approx 31.6\%$ con complejidad $O(N^2 \cdot \tau)$.*
  >
  > *En la Variante 2, modelamos la dinámica a lo largo de $T$ rondas con nodos que fallan de manera independiente con probabilidad $q$. Derivamos el costo total del sistema en $O(T \cdot (N k \tau + N + B \log N))$ y comparamos experimentalmente dos políticas de gasto: una política uniforme versus una concentrada al inicio con decaimiento, mostrando cómo esta última captura mayores ganancias tempranas antes del agotamiento o fallo de nodos.*
  >
  > *En la Variante 3, los nodos forman un grafo. En el caso aditivo con sinergias, demostramos algebraicamente que al reagrupar términos, la utilidad total se preserva como una suma separable de funciones cóncavas con grado ponderado, por lo que el voraz de la Parte 1 sigue siendo estrictamente óptimo. En el caso competitivo con interferencia, demostramos mediante un contraejemplo que el voraz falla, y propusimos una heurística voraz penalizada por impacto marginal neto en tiempo $O(B(N + |E|))$."*

---

### ESCENA 6: Validación Experimental y Contraste Empírico vs Teórico
- **Duración:** 90 segundos
- **Título de Escena:** `SCENE_06_EXPERIMENTAL_VALIDATION`
- **Prompt Visual para KLM / Generador de Video:**
  > *High-tech charts showing experimental results. Left plot: Execution time vs theoretical curve $c \cdot (N + B \log N)$ with scatter data points and confidence intervals ($R^2 > 0.99$). Right plot: Submodular ratio $f(A_{greedy}) / f(A^*)$ consistently staying above the 0.632 red horizontal dashed line.*
- **Texto en Pantalla (Overlay Text):**
  - Validación en al menos 5 tamaños de entrada ($N \in [50, 800]$, $B \in [100, 2000]$)
  - Ajuste de Regresión: $T(N, B) \sim c \cdot (N + B \log N)$ ($R^2 = 0.994$)
  - Verificación de la Cota Nemhauser: Ratio experimental $> 0.85 \ge 0.632$
- **Locución (Voiceover Script):**
  > *"Cumpliendo con la Sección 1.2 del pliego, no nos limitamos a reportar que el código corre en ciertos segundos; realizamos una validación experimental rigurosa contrastada directamente contra las funciones teóricas $T(n)$.*
  >
  > *Generamos instancias sintéticas reproducibles con semillas fijas para más de 5 tamaños crecientes de $N$ y $B$. Medimos el tiempo real de ejecución con el cronómetro de alta precisión de Python promediando múltiples ejecuciones.*
  >
  > *Como pueden observar en la gráfica, la curva experimental de la Parte 1 coincide de manera exacta con el modelo analítico $O(N + B \log N)$, con un coeficiente de determinación $R^2$ superior al 99%. Asimismo, calculamos la solución exacta por fuerza bruta combinatoria $\binom{N}{k}$ para instancias pequeñas y comprobamos que el algoritmo voraz submodular superó holgadamente la cota teórica del $63.2\%$, alcanzando ratios empíricos superiores al $88\%$ de la utilidad óptima."*

---

### ESCENA 7: Conclusiones y Demostración en Código
- **Duración:** 45 segundos
- **Título de Escena:** `SCENE_07_CONCLUSION_DEMO`
- **Prompt Visual para KLM / Generador de Video:**
  > *Terminal execution of `python scripts/run_all.py` showing green passing checkmarks for all parts and variants. The presenter delivers closing remarks with a confident posture.*
- **Texto en Pantalla (Overlay Text):**
  - Arquitectura en capas limpia: Modelos, Algoritmos, Variantes, Experimentos
  - 100% Reproducible | Código documentado con Tipado y POO
  - ¡Gracias por su atención!
- **Locución (Voiceover Script):**
  > *"En conclusión, hemos entregado una solución integral, robusta y matemáticamente fundamentada. Nuestro código está estructurado en una arquitectura limpia por capas, orientado a objetos, completamente modular y documentado.*
  >
  > *El proyecto demuestra con total rigor el balance entre la optimalidad exacta de la Parte 1, la aproximación con garantías demostrables de la Parte 2 y el análisis profundo de sus tres variantes. Muchas gracias."*

---

## 3. Instrucciones de Renderizado para KLM

1. **Configuración de Voz:** Voz en español neutro, tono masculino o femenino institucional / docente. Ritmo aproximado de 135 a 145 palabras por minuto.
2. **Subtítulos:** Activar subtítulos automáticos sincronizados (estilo closed-captions) resaltando palabras clave (e.g. *NP-difícil*, *Max-Heap*, *Submodular*, *Cota de Nemhauser*).
3. **Recursos Gráficos:** Importar el diagrama `docs/arquitectura_problema.xml` en draw.io para exportar las ilustraciones vectoriales de fondo en alta resolución (PNG/SVG a 4K).

