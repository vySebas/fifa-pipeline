# Pipeline de Ingeniería de Datos: FIFA World Cup 2026 ⚽📊

Este proyecto implementa una solución completa de **Modern Data Stack** contenerizada en **Docker** para la ingesta, limpieza, transformación analítica y visualización interactiva del rendimiento de los jugadores para el Mundial 2026.

## 🛠️ Arquitectura del Modern Data Stack
* **Ingesta y Limpieza:** `Polars` (Manejo de nulos, eliminación de duplicados por ID y límite estricto de 5,000 registros).
* **Almacenamiento y Cómputo:** `DuckDB` (Base de datos analítica integrada local).
* **Transformación (ELT):** `dbt Core` (Capa de Staging con casts de tipos y Data Mart con la tabla de hechos resumida).
* **Calidad de Datos:** `dbt tests` (Validaciones automáticas de unicidad y no nulidad).
* **Orquestación:** `Prefect` (Secuenciación efímera local).
* **Dashboard Visual:** `Dash` & `Plotly Express` (Análisis multidimensional con operaciones interactivas de **Roll-up** y **Drill-down**).

---

## 🚀 Instrucciones de Ejecución (Para el Evaluador)

Siga estos tres sencillos pasos para levantar y probar la aplicación completa de forma 100% reproducible:

### 1. Clonar el repositorio
```bash
git clone <https://github.com/olopez27CL/fifa-pipeline-OmarLopez.git>
cd fifa-pipeline-OmarLopez# fifa-pipeline-OmarLopez
Evaluacion Pipeline UNIDAD 3 BIGDATA - BenjaminAzocar - Omar Lopez - Pohla Lopez - Sebastian Yucra

### 2. Colocar el Dataset (Opcional)
El repositorio ya incluye un archivo de muestra (`data/raw/fifa_sample.csv`) para que el sistema funcione de inmediato al ser clonado. 

Si desea probar la solución con el dataset completo de 75 columnas:
1. Reemplace el archivo o asegúrese de renombrarlo exactamente como: `data/raw/fifa_data.csv`
2. El script de `Polars` detectará automáticamente el archivo completo, aplicará la limpieza de duplicados y limitará el procesamiento a los 5,000 registros requeridos.
