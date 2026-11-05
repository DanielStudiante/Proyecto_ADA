# DESGLOSE DE ENTREGABLES Y PLAN DE PROYECTO
## Proyecto Semestral 2026-B: Análisis y Diseño de Algoritmos (ADA)
### Subproyecto 2: Reparto de un Presupuesto Limitado y Selección de Participantes (Proyecto Red)

---

## 1. Contexto del Subproblema y Resumen Ejecutivo

El **Subproyecto 2** modela un sistema colaborativo de inteligencia artificial distribuida (Aprendizaje Federado) compuesto por una red de $N$ nodos. Los nodos entrenan de forma conjunta un modelo a lo largo de $T$ rondas sin compartir datos crudos, protegiendo las actualizaciones con mecanismos de privacidad diferencial (ruido calibrado). 

El problema involucra una jerarquía de dos decisiones algorítmicas acopladas y 3 variantes obligatorias:
1. **Parte 2 (Macro-nivel):** ¿Qué subconjunto de $k$ nodos (de los $N$ disponibles) debe seleccionarse en una ronda para maximizar la cobertura/utilidad de información conjunta? Se modela como la maximización de una función submodular sujeta a restricción de cardinalidad ($k < N$). Es **NP-difícil**.
2. **Parte 1 (Micro-nivel):** Dado el subconjunto de nodos seleccionados, ¿cómo repartir de forma óptima un presupuesto total de ruido/privacidad $B$ entre ellos, considerando que cada nodo posee una función de utilidad cóncava y creciente $u_i(x)$? Tiene solución **exacta en tiempo polinomial/pseudo-polinomial** mediante un algoritmo voraz óptimo basado en cola de prioridad (*Max-Heap*).
3. **Variantes Obligatorias:**
   - **Variante 1:** Nodos con costos heterogéneos de participación y presupuesto de costo $L$ (*Budgeted Maximum Coverage*).
   - **Variante 2:** Ejecución dinámica en $T$ rondas con fallas independientes de nodos (probabilidad $q$) y presupuesto global de ruido, contrastando políticas de gasto.
   - **Variante 3:** Grafo de dependencias entre nodos con externalidades aditivas (sinergia) vs competitivas (interferencia/congestión).

---

## 2. Los 5 Requisitos Formales de Eficiencia (Sección 1.2 del Enunciado)

El enunciado establece explícitamente que no basta con programar código funcional. Cada equipo debe cumplir y defender formalmente:

| # | Requisito Formal Exigido | Cómo se aborda en el Subproyecto 2 | Criterio de Aceptación del Docente |
|---|--------------------------|-----------------------------------|------------------------------------|
| **1** | **Definición precisa del tamaño de entrada $n$** | - **Parte 1:** $N$ (número de nodos seleccionados) y $B$ (unidades discretas de presupuesto).<br>- **Parte 2:** $N$ (nodos candidatos), $k$ (cupo), $\|U\|$ (universo de datos/reglas cubiertas). | Justificación matemática formal de qué dimensión crece y por qué es la métrica adecuada de complejidad. |
| **2** | **Deducción explícita de $T(n)$ para el algoritmo exacto** | Deducción paso a paso de $T(N, B) = O(N + B \log N)$ contando operaciones elementales (construcción del montículo $O(N)$ y $B$ extracciones/actualizaciones $O(\log N)$). | Conteo explícito paso a paso, resolución de recurrencias/sumatorias y justificación de pseudo-polinomialidad. |
| **3** | **Prueba formal de NP-dureza por reducción** | Reducción polinomial formal desde **Maximum Coverage** hacia la selección de nodos participantes con utilidad submodular $f(A) = \|\bigcup_{i \in A} S_i\|$. | Reducción válida en la dirección correcta: instancia $\to$ transformación polinomial $\to$ demostración bicondicional ($x \in L \iff f(x) \in L'$). |
| **4** | **Algoritmo aproximado y garantía teórica** | Algoritmo voraz submodular con cota de aproximación demostrada de $(1 - 1/e) \approx 63.2\%$ (Nemhauser et al., 1978). Para Variante 1: Khuller et al. (1999) con cota $\frac{1}{2}(1 - 1/e)$. | Demostración matemática paso a paso de la cota por recurrencia de ganancia residual o aplicación rigurosa de teoremas citados. |
| **5** | **Validación experimental contrastada con la teoría** | Medición de tiempos de ejecución empíricos en al menos 5 tamaños crecientes de $N$ y $B$, contrastando la curva observada vs la curva teórica $O(f(n))$. | Gráficas con ajuste de regresión no lineal $c \cdot f(n)$, barras de dispersión y análisis de residuos. Prohibido reportar solo tablas planas de segundos. |

---

## 3. Matriz de Entregables del Proyecto

Para cumplir con la totalidad de los requerimientos y asegurar la calificación máxima, el proyecto se estructura en los siguientes entregables organizados en carpetas:

```
ADA/
├── docs/
│   ├── DESGLOSE_ENTREGABLES.md      # Este documento: desglose y planificación
│   ├── DOCUMENTACION_TEORICA.md     # Marco teórico, demostraciones y análisis formal
│   ├── arquitectura_problema.xml    # Diagrama gráfico en XML (compatible draw.io)
│   └── guion_video_klm.md           # Guion y prompts estructurados para video KLM
├── src/
│   ├── core/                        # Capa de dominio (modelos y generador de datos)
│   │   ├── models.py                # Clases de dominio (Node, UtilityFunction, Graph, etc.)
│   │   └── data_generator.py        # Generación sintética determinista con semillas
│   ├── parte1_reparto/              # Capa Parte 1: Reparto óptimo voraz
│   │   ├── greedy_budget.py         # Voraz óptimo con Max-Heap O(N + B log N)
│   │   └── brute_force_budget.py    # Validación exacta por DP / Fuerza bruta
│   ├── parte2_seleccion/            # Capa Parte 2: Selección submodular
│   │   ├── submodular_greedy.py     # Voraz submodular O(N * k * tau)
│   │   └── brute_force_selection.py # Fuerza bruta combinatoria C(N, k) para calcular óptimo
│   ├── variantes/                   # Carpetas independientes por variante
│   │   ├── v1_costos_distintos/     # Khuller et al. (1999) con costos de participación
│   │   │   ├── khuller_greedy.py
│   │   │   └── README.md
│   │   ├── v2_multi_ronda_fallas/   # T rondas con fallas independientes (probabilidad q)
│   │   │   ├── multi_round_sim.py
│   │   │   └── README.md
│   │   └── v3_nodos_relacionados/   # Red de nodos: efectos aditivos vs competitivos
│   │       ├── network_effects.py
│   │       └── README.md
│   └── experiments/                 # Benchmarks y curvas empíricas vs teóricas
│       ├── benchmark_runner.py
│       └── plot_generator.py
├── scripts/
│   └── run_all.py                   # Ejecutor integrado de pruebas, experimentos y gráficas
├── requirements.txt                 # Dependencias (numpy, matplotlib)
└── README.md                        # Guía de instalación y reproducción
```

---

## 4. Criterios de Evaluación y Ponderaciones Oficiales (Tabla 5.2)

| Componente | Peso | Aspectos Clave a Evaluar |
|------------|:----:|--------------------------|
| **Formalización del problema** | 10% | Definición limpia de tamaño de entrada, entrada, salida y función objetivo de ambas partes. |
| **Prueba de NP-dureza por reducción** | 10% | Reducción formal, paso a paso, correcta, completa y en la dirección canónica. |
| **Deducción formal de $T(n)$ exacto** | 10% | Conteo analítico de operaciones elementales de la cola de prioridad y justificación de pseudo-polinomialidad. |
| **Algoritmo aproximado / heurístico** | 15% | Diseño algorítmico, complejidad $T(N, k, \tau)$, demostración/aplicación rigurosa de la cota $(1 - 1/e)$. |
| **Validación experimental** | 10% | Mediciones reproducibles en $\ge 5$ tamaños de entrada, gráficas de tiempo vs $n$ y ajuste contra curva teórica. |
| **Sustentación oral (15 a 20 min)** | 45% | Defensa individual y grupal sin notas de la reducción NP y la deducción de $T(n)$. |
| **Total** | **100%** | Nota definitiva del proyecto semestral. |

---

## 5. Cronograma de Trabajo y Plan de Hitos (13 Semanas)

| Semanas | Hito del Cronograma | Entregables y Estado en este Repositorio |
|:-------:|---------------------|-----------------------------------------|
| **1 – 2** | Formalización del problema sin código | Cubierto en `docs/DOCUMENTACION_TEORICA.md` (Sección 1 y 2). |
| **3 – 4** | Prueba formal de NP-dureza por reducción | Cubierto en `docs/DOCUMENTACION_TEORICA.md` (Sección 4: Reducción desde Maximum Coverage). |
| **5 – 6** | Algoritmo exacto y deducción formal de $T(n)$ | Implementado en `src/parte1_reparto/` y deducido en `docs/DOCUMENTACION_TEORICA.md` (Sección 3). |
| **7 – 8** | Algoritmo aproximado, $T(n)$ y cota $(1 - 1/e)$ | Implementado en `src/parte2_seleccion/` y demostrado en `docs/DOCUMENTACION_TEORICA.md` (Sección 5). |
| **9 – 11**| Experimentación y las 3 variantes obligatorias | Implementadas en `src/variantes/` y `src/experiments/` con gráficas automáticas. |
| **12 – 13**| Informe final y preparación para la sustentación | Preparado mediante `docs/guion_video_klm.md` y `docs/arquitectura_problema.xml`. |

---

## 6. Lista de Chequeo (Checklist) para la Entrega Final

- [x] Documento de formalización teórica con definiciones de tamaño de entrada.
- [x] Demostración matemática del teorema de optimalidad por argumento de intercambio para Parte 1.
- [x] Deducción paso a paso de $T(N, B) = O(N + B \log N)$ y discusión de pseudo-polinomialidad vs water-filling.
- [x] Demostración formal de reducción polinomial desde Maximum Coverage (NP-dureza de Parte 2).
- [x] Deducción de la cota de aproximación $(1 - 1/e)$ de Nemhauser et al. y complejidad $O(N \cdot k \cdot \tau)$.
- [x] Implementación en capas con programación orientada a objetos (POO) y tipado estático en Python.
- [x] Solver por fuerza bruta $\binom{N}{k}$ para validar experimentalmente que el voraz respeta la cota del $63.2\%$.
- [x] Variante 1 codificada y documentada: Khuller et al. (1999) con cota $\frac{1}{2}(1 - 1/e)$.
- [x] Variante 2 codificada y documentada: $T$ rondas con fallas $q$ y comparativa de políticas de presupuesto.
- [x] Variante 3 codificada y documentada: Demostración algebraica del caso aditivo y contraejemplo del caso competitivo.
- [x] Generador de instancias sintéticas con semillas reproducibles (`random.seed`).
- [x] Benchmark automatizado para $\ge 5$ tamaños de $N$ y $B$, con exportación de gráficas tiempo vs teoría.
- [x] Diagrama arquitectural completo en formato estándar XML (draw.io).
- [x] Guion estructurado para KLM con indicaciones de audio, video y diapositivas para sustentación.

