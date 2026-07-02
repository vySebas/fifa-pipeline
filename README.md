# ⚽ Pipeline de Ingeniería de Datos: FIFA World Cup 2026

Proyecto de Big Data que implementa una solución de **Modern Data Stack** contenerizada en Docker para la ingesta, transformación, modelado multidimensional y visualización interactiva del rendimiento de jugadores del Mundial 2026.

**Institución:** Santo Tomás  
**Asignatura:** Big Data | Ingeniería en Informática  
**Integrantes:** Benjamín Azócar, Omar López, Pohla López, Sebastián Yucra

---

## 🛠️ Arquitectura del Modern Data Stack (ELT)

El proyecto utiliza un enfoque **ELT** (Extract, Load, Transform) optimizado:

* **Ingesta (Extract):** `Polars` lee el CSV de origen, selecciona las 10 columnas requeridas, valida tipos de dato, elimina duplicados/nulos y limita el procesamiento a 5.000 registros.
* **Carga (Load):** Los datos crudos y validados se escriben directamente en `DuckDB` (tabla `raw_player_performance`) mediante tareas orquestadas por `Prefect`.
* **Transformación (Transform):** `dbt Core` construye un Modelo Estrella (*staging* → *dimensiones* → *hechos*) aplicando pruebas de calidad (*dbt tests*).
* **Orquestación:** `Prefect` encadena todo el flujo: Ingesta → dbt run → dbt test → Activación del Dashboard.
* **Visualización:** `Dash` y `Plotly Express` consumen directamente las tablas del modelo estrella en `DuckDB`, permitiendo interactividad (roll-up / drill-down por país).

---

## 📊 Modelo Multidimensional (Star Schema)

El proyecto implementa un **Esquema Estrella** en `dbt`, validado mediante *tests* de integridad (`unique`, `not_null`, `relationships`).

### Tabla de Hechos: `fct_player_performance`
Contiene las métricas cuantitativas y llaves foráneas.

| Columna | Tipo | Descripción |
| :--- | :--- | :--- |
| `player_id` | FK | Identificador del jugador |
| `nationality` | FK | Selección nacional |
| `position` | FK | Posición táctica |
| `goals` | Medida | Goles anotados |
| `shots_on_target` | Medida | Tiros al arco |
| `expected_goals_xg`| Medida | Goles esperados (xG) |
| `yellow_cards` | Medida | Tarjetas amarillas |

### Dimensiones
* **dim_players:** Atributos descriptivos (player_id, nombre, edad, altura).
* **dim_teams:** Selección nacional (nationality).
* **dim_positions:** Posición táctica en el campo.

---

## 🚀 Instrucciones de Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/whoiswasd/fifa-pipelinefinal.git
cd fifa-pipelinefinal
```
### 2. Levantar el proyecto completo
Ejecuta el siguiente comando para desplegar toda la arquitectura (orquestador, base de datos, transformaciones y dashboard):

``` Bash
docker compose up
```
Al ejecutarlo, se despliega automáticamente la arquitectura completa, iniciando los siguientes procesos :
- El servidor de Prefect 
- La ingesta de datos con Polars → DuckDB
- Las transformaciones de dbt (dbt run + 
dbt test)
- El dashboard interactivo en Dash http://localhost:8050

### 3. Dataset
El repositorio incluye el dataset optimizado en data/raw/fifa_data.csv. 
**No se requiere ninguna configuración adicional.**

#### 📁 Estructura del Proyecto
``` Bash
fifa-pipelinefinal/
├── data/
│   ├── raw/                 # Dataset CSV origen
│   └── transformed/         # Base de datos local DuckDB
├── dbt_project/             # Modelos SQL, tests de calidad y macros
├── flows/                   # Scripts de Python (ingesta y orquestación)
├── docker-compose.yml       # Orquestador de contenedores
├── Dockerfile               # Receta de la imagen del entorno
├── dashboard.py             # Lógica de visualización Plotly/Dash
├── requirements.txt         # Dependencias de Python
└── README.md                # Documentación del proyecto
```
