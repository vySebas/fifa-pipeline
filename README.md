# Pipeline de Ingeniería de Datos: FIFA World Cup 2026 ⚽📊

Proyecto de Big Data que implementa una solución de **Modern Data Stack** contenerizada en **Docker** para la ingesta, transformación, modelado multidimensional y visualización interactiva del rendimiento de jugadores del Mundial 2026.

**Asignatura:** Big Data | Ingeniería en Informática
**Integrantes:** Benjamín Azócar, Omar López, Pohla López, Sebastián Yucra

---

## 🛠️ Arquitectura del Modern Data Stack (ELT)

* **Ingesta (Extract):** `Polars` lee el CSV de origen, selecciona las 10 columnas requeridas, valida tipos de dato, elimina duplicados/nulos y limita el procesamiento a 5.000 registros.
* **Carga (Load):** Los datos crudos y validados se escriben directamente en `DuckDB`, en la tabla `raw_player_performance`, dentro de una tarea orquestada por `Prefect`.
* **Transformación (Transform):** `dbt Core` toma la tabla cruda y construye un **Modelo Estrella** (staging → dimensiones → tabla de hechos), aplicando `dbt tests` de calidad.
* **Orquestación:** `Prefect` encadena ingesta → `dbt run` → `dbt test` → activación del dashboard, en un único flow ejecutable.
* **Visualización:** `Dash` y `Plotly Express` consumen directamente las tablas del modelo estrella en DuckDB, con interactividad (roll-up / drill-down por país).

---

## 📊 Modelo Multidimensional

El proyecto implementa un **Esquema Estrella (Star Schema)** en dbt, compuesto por una tabla de hechos y tres tablas de dimensiones, todas relacionadas mediante llaves de negocio (`player_id`, `nationality`, `position`).

### Tabla de hechos
**`fct_player_performance`**
Contiene las métricas cuantitativas de rendimiento de cada jugador, junto a las llaves foráneas hacia las dimensiones.

| Columna | Tipo | Descripción |
|---|---|---|
| player_id | FK → dim_players | Identificador del jugador |
| nationality | FK → dim_teams | Selección nacional |
| position | FK → dim_positions | Posición táctica |
| goals | Medida | Goles anotados |
| shots_on_target | Medida | Tiros al arco |
| expected_goals_xg | Medida | Goles esperados (xG) |
| yellow_cards | Medida | Tarjetas amarillas |

### Dimensiones

* **`dim_players`**: atributos descriptivos y físicos del jugador (`player_id`, `player_name`, `age`, `height_cm`).
* **`dim_teams`**: selección nacional del jugador (`nationality`).
* **`dim_positions`**: posición táctica en el campo (`position`).

### Medidas (métricas cuantitativas)
`goals`, `shots_on_target`, `expected_goals_xg`, `yellow_cards`.

Todas las relaciones y la integridad del modelo están validadas mediante `dbt tests` (`unique`, `not_null`, `relationships`) definidos en `dbt_project/models/marts/schema.yml`.

---

## 🚀 Instrucciones de Ejecución (Para el Evaluador)

### 1. Clonar el repositorio
```bash
git clone https://github.com/whoiswasd/fifa-pipelinefinal.git
cd fifa-pipelinefinal
```

### 2. Levantar el proyecto completo
```bash
docker compose up --build
```

Este único comando levanta automáticamente:
- El servidor de Prefect (UI en `http://localhost:4200`)
- La ingesta de datos con Polars → DuckDB
- Las transformaciones de dbt (`dbt run` + `dbt test`)
- El dashboard interactivo en `http://localhost:8050`

No se requiere ninguna intervención manual adicional.

### 3. Dataset
El repositorio incluye un archivo de muestra (`data/raw/fifa_sample.csv`) para que el sistema funcione de inmediato al clonar. Si se desea usar el dataset completo, basta con colocarlo en `data/raw/fifa_data.csv`; el script de ingesta lo detecta automáticamente.

---

## 📁 Estructura del proyecto
