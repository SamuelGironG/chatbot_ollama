# Análisis de rendimiento de modelos Ollama

Este documento registra la comparación de tiempos de respuesta entre `gemma2:2b`, `llama3.2:3b` y `llama3.1:8b`.

> Reemplaza los valores de ejemplo por los tiempos que muestre la aplicación. Para una comparación más fiable, realiza varias pruebas por cada tipo de prompt y usa el promedio en segundos.

## Datos recolectados

| Modelo | Parámetros aproximados | Prompt simple (s) | Prompt medio (s) | Prompt complejo (s) |
|---|---:|---:|---:|---:|
| gemma2:2b | 2 | — | — | — |
| llama3.2:3b | 3 | — | — | — |
| llama3.1:8b | 8 | — | — | — |

### Criterios de los prompts

- **Simple:** pregunta breve y directa.
- **Medio:** petición de explicación con varios requisitos.
- **Complejo:** tarea extensa con contexto, restricciones o varios pasos.

## 1. Gráfica de barras: tiempo de respuesta vs. modelo

La siguiente gráfica compara el tiempo de respuesta de cada modelo para los tres niveles de complejidad. Sustituye los arreglos `t_simple`, `t_medio` y `t_complejo` con tus promedios reales.

```python
import matplotlib.pyplot as plt
import numpy as np

modelos = ["gemma2:2b", "llama3.2:3b", "llama3.1:8b"]

# Reemplaza estos valores de ejemplo por tus datos reales (segundos).
t_simple = [2.98, 18.6, 6.3]
t_medio = [4.17, 7.3, 9.0]
t_complejo = [5.9, 8.61, 9.6]

x = np.arange(len(modelos))
ancho = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - ancho, t_simple, ancho, label="Prompt simple")
ax.bar(x, t_medio, ancho, label="Prompt medio")
ax.bar(x + ancho, t_complejo, ancho, label="Prompt complejo")

ax.set_xlabel("Modelo")
ax.set_ylabel("Tiempo de respuesta (s)")
ax.set_title("Tiempo de respuesta vs. modelo y complejidad")
ax.set_xticks(x)
ax.set_xticklabels(modelos)
ax.legend()
plt.tight_layout()
plt.savefig("grafica_tiempos.png", dpi=150)
plt.show()
```

Cuando generes la imagen, puedes insertarla aquí:

```markdown
![Gráfica de tiempos](grafica_tiempos.png)
```

## 2. Gráfica de dispersión: parámetros vs. tiempo promedio

Esta gráfica permite observar si existe una relación entre el número de parámetros del modelo y su tiempo promedio de respuesta. Reemplaza `tiempo_promedio` por tus datos.

```python
import matplotlib.pyplot as plt

modelos = ["gemma2:2b", "llama3.2:3b", "llama3.1:8b"]
parametros = [2, 3, 8]  # Miles de millones de parámetros, aproximadamente.

# Reemplaza estos valores de ejemplo por tus promedios reales (segundos).
tiempo_promedio = [4.35,11,50 , 8.3]

plt.figure(figsize=(9, 6))
plt.scatter(parametros, tiempo_promedio, s=110, color="#6c8cff")

for modelo, x, y in zip(modelos, parametros, tiempo_promedio):
    plt.annotate(modelo, (x, y), xytext=(6, 6), textcoords="offset points")

plt.xlabel("Número de parámetros (miles de millones)")
plt.ylabel("Tiempo promedio de respuesta (s)")
plt.title("Parámetros del modelo vs. tiempo promedio de respuesta")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("grafica_parametros.png", dpi=150)
plt.show()
```

Inserta la imagen generada:

```markdown
![Gráfica de parámetros](grafica_parametros.png)
```

## Interpretación

Completa este apartado tras obtener tus resultados:

- El modelo con menor tiempo promedio fue: **[completar]**.
- El modelo con mayor tiempo promedio fue: **[completar]**.
- El tipo de prompt que más afectó los tiempos fue: **[completar]**.
- La relación entre cantidad de parámetros y tiempo de respuesta fue: **[completar]**.

## Dependencias para generar las gráficas

Estas librerías se usan solo para el análisis, no para ejecutar la aplicación de chat:

```powershell
pip install matplotlib numpy
```
